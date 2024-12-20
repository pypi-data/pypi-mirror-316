import importlib.metadata

from cellestial.single import (
    boxplot,
    boxplots,
    dim,
    dimensional,
    dimensionals,
    expression,
    expressions,
    pca,
    pcas,
    tsne,
    tsnes,
    umap,
    umaps,
    violin,
    violins,
)
from cellestial.util import _add_arrow_axis, interactive

__version__ = importlib.metadata.version("cellestial")

__all__ = [
    "interactive",
    "_add_arrow_axis",
    "dimensional",
    "dimensionals",
    "dim",
    "umap",
    "umaps",
    "pca",
    "pcas",
    "tsne",
    "tsnes",
    "expression",
    "expressions",
    "violin",
    "violins",
    "boxplot",
    "boxplots",
]
