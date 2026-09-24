"""
Shared plumbing for the SupplyFlow FMCG notebooks.

Deliberately limited to paths, file loading/saving and plot styling.

There is NO analysis code here on purpose. Every calculation that produces a
finding — missingness, outliers, encoding, imputation, metrics — belongs in the
notebook where it is interpreted, visible to the reader. Hiding an analytical
step in a helper function hides the reasoning the project is assessed on.

Usage at the top of any notebook, at any folder depth:

    import sys, pathlib
    ROOT = next(p for p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]
                if (p / "src" / "common.py").exists())
    sys.path.insert(0, str(ROOT))
    from src.common import *
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCS_DIR = PROJECT_ROOT / "docs"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PREPROCESSED_DIR = PROJECT_ROOT / "data" / "preprocessed"

RAW_FILE = RAW_DIR / "SupplyFlow FMCG Solutions.xlsx"
PREPROCESSED_FILE = PREPROCESSED_DIR / "warehouse_preprocessed.csv"

OBJ_DIRS = {
    1: PROJECT_ROOT / "Obj_1_Clustering",
    2: PROJECT_ROOT / "Obj_2_Classification",
    3: PROJECT_ROOT / "Obj_3_Regression",
}


def obj_paths(objective: int) -> dict:
    """Return the four working folders for an objective (1, 2 or 3).

    >>> p = obj_paths(2)
    >>> p["model"].name
    'model'
    """
    base = OBJ_DIRS[objective]
    return {
        "base": base,
        "processed": base / "data" / "processed",
        "feature_engine": base / "feature_engine",
        "train_eval": base / "training_and_evaluation",
        "model": base / "model",
    }


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


def load_raw() -> pd.DataFrame:
    """Read the untouched source workbook.

    No cleaning, no dtype coercion, no na_values overrides — the notebook must
    see exactly what pandas sees, including anything odd.
    """
    return pd.read_excel(RAW_FILE, sheet_name="Data")


def load_preprocessed() -> pd.DataFrame:
    """Read the output of notebooks/01_global_preprocessing.ipynb."""
    if not PREPROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"{PREPROCESSED_FILE} not found. "
            "Run notebooks/01_global_preprocessing.ipynb first."
        )
    return pd.read_csv(PREPROCESSED_FILE)


# --------------------------------------------------------------------------
# Saving
# --------------------------------------------------------------------------


def save_table(df: pd.DataFrame, path, index: bool = True) -> Path:
    """Write a results table to CSV, creating the folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)
    print(f"saved  {path.relative_to(PROJECT_ROOT)}  {df.shape}")
    return path


def save_fig(path, dpi: int = 150) -> Path:
    """Save the current matplotlib figure."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"saved  {path.relative_to(PROJECT_ROOT)}")
    return path


# --------------------------------------------------------------------------
# Presentation
# --------------------------------------------------------------------------


def set_style() -> None:
    """One consistent look for every chart in the project."""
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams["figure.figsize"] = (10, 5)
    plt.rcParams["figure.dpi"] = 110
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 10

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.width", 160)
    pd.set_option("display.float_format", lambda v: f"{v:,.4f}")


RANDOM_STATE = 42
