r"""
Main class of `decipher` package
"""

from copy import deepcopy
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc
import scipy.sparse as sps
import torch
import torch.nn.functional as F
import yaml
from addict import Dict
from anndata import AnnData
from loguru import logger
from sklearn.preprocessing import LabelEncoder

from .data.mnn_dataset import MNNDataset, MNNMixin
from .data.process import omics_data_process
from .ddp import DDPMixin
from .emb import sc_emb, spatial_emb
from .explain.gene.mixin import GeneSelectMixin
from .explain.regress.mixin import RegressMixin
from .graphic.build import build_graph
from .plot import plot_sc
from .utils import CFG, estimate_spot_size, global_seed, scanpy_viz, sync_config


class DECIPHER(RegressMixin, GeneSelectMixin, MNNMixin, DDPMixin):
    r"""
    Base class of model definition and training

    Parameters
    ----------
    work_dir
        working directory
    user_cfg
        user defined config dict, will be ignored if `recover` is True
    recover
        if recover from a previous run
    """

    def __init__(self, work_dir: str = "DECIPHER", user_cfg: Dict = None, recover: bool = False):
        self.work_dir = Path(work_dir)
        if self.work_dir.exists() and not recover:
            logger.warning(f"{self.work_dir} already exists but `recover` is False.")
        # init logger
        now = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        logger.add(self.work_dir / "logs" / f"run_{now}.log")
        # init config
        if not recover:
            cfg = deepcopy(CFG)
            if user_cfg is not None:
                cfg.update(user_cfg)
            cfg.work_dir = str(work_dir)
            sync_config(cfg)
            self.cfg = cfg
            with open(self.work_dir / "hyperparams.yaml", "w") as f:
                yaml.dump(cfg.to_dict(), f)
        else:
            with open(self.work_dir / "hyperparams.yaml") as f:
                self.cfg = Dict(yaml.safe_load(f))
            self.load(work_dir)
            logger.success("Recover from previous run.")
        global_seed(self.cfg.seed)
        sc._settings.ScanpyConfig.figdir = self.work_dir / "figures"

    def register_data(
        self,
        adata: list[AnnData] | AnnData,
        group_list: list[str] = None,
        batch_list: list[int] = None,
        split_by: str = None,
        cell_type: str = None,
        preprocess: bool = True,
        edge_index: np.ndarray = None,
    ) -> None:
        r"""
        Register spatial omics data

        Parameters
        ----------
        adatas: list[AnnData] | AnnData
            AnnData or list of slice, each is a spatial slice
        group_list
            Group list for each AnnData, must provided if run with more than one slice
        batch_list
            Batch list for each AnnData, must be **int** if provided, model will view each slice as a batch if not provided
        split_by:
            Split by column name in `obs` of each AnnData object
        cell_type
            Cell type column name in `obs` of each AnnData object
        preprocess:
            preprocess the adata object, only for advanced users
        edge_index
            use self-defined edge index, only for advanced users
        """
        # precess single cell data
        if preprocess:
            adata = omics_data_process(
                adata, cell_type, batch_list, group_list, split_by, self.cfg.omics
            )
            self.x = adata[:, adata.var["highly_variable"]].X.copy()
        else:
            logger.warning("Skip preprocessing, make sure the input data is ready.")
            self.x = adata.X.copy()
            if cell_type is not None:
                adata.obs["_celltype"] = adata.obs[cell_type].astype(str)
            if split_by is not None:
                adata.obs["_batch"] = LabelEncoder().fit_transform(adata.obs[split_by])
        self.x = self.x.toarray() if isinstance(self.x, sps.csr_matrix) else self.x
        np.save(self.work_dir / "x.npy", self.x)
        self.coords = adata.obsm["spatial"]
        self.meta = adata.obs
        if self.coords.shape[1] == 2:
            self.meta[["x", "y"]] = self.coords
        elif self.coords.shape[1] == 3:
            self.meta[["x", "y", "z"]] = self.coords
        else:
            raise ValueError("Spatial info must be 2D or 3D.")
        self.meta.to_csv(self.work_dir / "cell_meta.csv")

        # batch info
        self.batch = None
        if "_batch" in self.meta.columns:
            batch = self.meta["_batch"].astype(int).values
            if np.unique(batch).shape[0] > 1:
                self.batch = batch
                logger.info("Batch info detected.")
        torch.save(self.batch, self.work_dir / "batch.pt")
        if not self.cfg.omics.ignore_batch and self.batch is not None:
            self.initMNN()
            np.save(self.work_dir / "valid_cellidx.npy", self.valid_cellidx)
            torch.save(self.mnn_dict, self.work_dir / "mnn_dict.pt", pickle_protocol=4)

        # build spatial graph
        if edge_index is None:
            self.edge_index = build_graph(self.coords, self.batch, **self.cfg.omics.spatial_graph)
        else:
            logger.info("Use self-defined edge index.")
            self.edge_index = edge_index
        np.save(self.work_dir / "coords.npy", self.coords)
        np.save(self.work_dir / "edge_index.npy", self.edge_index.numpy())

    def fit_omics(self) -> None:
        r"""
        Fit model on spatial omics data, should run after `register_data`
        """
        # mnn dataset
        mnn_dataset = None
        if self.batch is not None and not self.cfg.omics.ignore_batch:
            mnn_dataset = MNNDataset(self.x, self.valid_cellidx, self.mnn_dict)
            logger.info(f"Using MNN with {len(np.unique(self.batch))} batches.")
        # train model
        sc_model, center_emb_pretrain = sc_emb(
            self.x, self.cfg.omics, mnn_dataset, self.meta, self.batch
        )
        center_emb, self.nbr_emb = spatial_emb(
            self.x,
            self.edge_index,
            self.cfg.omics,
            mnn_dataset,
            self.meta,
            sc_model,
            self.batch,
        )
        self.center_emb = center_emb_pretrain if center_emb_pretrain else center_emb
        # as float
        self.center_emb = self.center_emb.astype(np.float32)
        self.center_emb = self.center_emb.astype(np.float32)
        # save embeddings
        np.save(self.work_dir / "center_emb.npy", self.center_emb)
        np.save(self.work_dir / "nbr_emb.npy", self.nbr_emb)
        logger.info(f"Results saved to {self.work_dir}")

    def visualize(self, resolution: float = 0.5) -> None:
        r"""
        Visualize results, should run after `fit_omics`

        Parameters
        ----------
        resolution
            resolution for clustering
        """
        if (self.work_dir / "embedding.h5ad").exists():
            adata = sc.read_h5ad(self.work_dir / "embedding.h5ad")
        else:
            norm_center = F.normalize(torch.tensor(self.center_emb)).numpy()
            norm_nbr = F.normalize(torch.tensor(self.nbr_emb)).numpy()
            adata = sc.AnnData(
                X=np.zeros((self.center_emb.shape[0], 1)),
                obsm={
                    "X_center": self.center_emb,
                    "X_nbr": self.nbr_emb,
                    "X_merge": np.hstack([norm_center, norm_nbr]),
                    "spatial": self.coords,
                },
                obs=self.meta.astype(str),
            )
            adata.uns["spot_size"] = estimate_spot_size(adata.obsm["spatial"])
            adata = scanpy_viz(adata, resolution=resolution)
            adata.write_h5ad(self.work_dir / "embedding.h5ad")
        color_vars = ["leiden_center", "leiden_nbr"]
        for var in ["_celltype", "_batch"]:
            if var in adata.obs.columns:
                color_vars.append(var)
        plot_sc(adata, color_vars)

    def load(self, from_dir: str | Path = None) -> None:
        r"""
        Load saved results, should run after `register_data`

        Parameters
        ----------
        from_dir
            directory to load from
        """
        from_dir = self.work_dir if from_dir is None else Path(from_dir)
        assert from_dir.is_dir(), f"Directory {from_dir} not exists."
        logger.info(f"Loading from {from_dir}")
        self.work_dir = from_dir
        # load data
        self.coords = np.load(self.work_dir / "coords.npy")
        self.edge_index = torch.from_numpy(np.load(self.work_dir / "edge_index.npy"))
        self.x = np.load(self.work_dir / "x.npy").astype(np.float32)
        self.meta = pd.read_csv(self.work_dir / "cell_meta.csv")
        self.batch = torch.load(self.work_dir / "batch.pt")
        if self.batch is not None and not self.cfg.omics.ignore_batch:
            self.valid_cellidx = np.load(self.work_dir / "valid_cellidx.npy")
            self.mnn_dict = torch.load(self.work_dir / "mnn_dict.pt")
        for var in ["center_emb", "nbr_emb"]:
            if (self.work_dir / f"{var}.npy").exists():
                setattr(self, var, np.load(self.work_dir / f"{var}.npy").astype(np.float32))

    def update_config(self, user_cfg: Dict | dict) -> None:
        r"""
        Update config

        Parameters
        ----------
        user_cfg
            user defined config dict
        """
        user_cfg["work_dir"] = str(self.work_dir)
        self.cfg.update(user_cfg)
        sync_config(self.cfg)
        with open(self.work_dir / "hyperparams.yaml", "w") as f:
            yaml.dump(self.cfg.to_dict(), f)
        logger.info(f"Config updated: {user_cfg}")
