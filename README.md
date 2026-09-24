# Analyzing Operational Efficiency and Predicting Breakdown Risk and Shipment Weight in the Warehouse Network of Supply Flow FMCG Solutions

**Student:** Lakshmi M G · **USN:** 232VBBR00036
**Elective:** Data Science and Analytics · **Institution:** JAIN (Deemed-to-be University), Online

---

## What this project does

Supply Flow FMCG Solutions distributes instant noodles through a network of 25,000 warehouses.
Performance across that network varies widely. This project applies three data science techniques
to a single snapshot of the company's warehouse records:

| # | Objective | Technique | Target variable |
|---|---|---|---|
| 1 | Identify the conditions that separate strong warehouses from weak ones | **Clustering** | none (unsupervised) |
| 2 | Estimate warehouse breakdown risk | **Classification** | `wh_breakdown_l3m` |
| 3 | Recommend a suitable shipment weight per warehouse, and compare volumes across zones | **Regression** | `product_wg_ton` |

Full statement of scope, objectives and exclusions: [`docs/00_project_brief.md`](docs/00_project_brief.md).

---

## How this project is built

Every analytical claim in this repository is produced by a notebook cell you can re-run. The
working rule, applied without exception:

> **compute → read the output → write the interpretation → then decide the treatment →
> then apply it, quoting the number that justified it.**

No missing-value strategy, outlier verdict, encoding choice or feature is applied because it is
conventional. It is applied because a specific result printed earlier in that notebook supports it,
and that result is cited in the markdown cell directly above the code.

---

## Setup

**Already done on this machine.** Python 3.12 is installed, `.venv312` is built, all packages are
installed, and the `SupplyFlow Python 3.12` Jupyter kernel is registered. To start working:

```bash
source .venv312/bin/activate
jupyter lab
```

In every notebook, select the **SupplyFlow Python 3.12** kernel before running.

<details>
<summary>To rebuild the environment from scratch</summary>

```powershell
winget install -e --id Python.Python.3.12
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name supplyflow --display-name "SupplyFlow Python 3.12"
```

Python 3.12 rather than the machine default 3.14, chosen for library compatibility. The full stack
was verified on 3.12.10; it was not tested on 3.14.
</details>

### Installed versions

| | | | |
|---|---|---|---|
| pandas 3.0.6 | numpy 2.5.3 | scipy 1.18.1 | statsmodels 0.15.0 |
| scikit-learn 1.9.1 | xgboost 3.4.1 | catboost 1.2.10 | imbalanced-learn 0.14.2 |
| optuna 5.0.0 | pycaret 4.0.0a8 | matplotlib 3.11.2 | seaborn 0.13.2 |
| plotly 7.1.0 | | | |

PyCaret is used only for model-family screening in Objective 2 NB 24 and Objective 3 NB 34. Optuna
then tunes only the selected model family in the next notebook.

---

## Run order

Notebooks are numbered and must be run in order — each stage reads the artefacts written by the
previous one.

```
notebooks/00_preliminary_analysis.ipynb      # data audit — reports only, changes nothing
notebooks/01_global_preprocessing.ipynb      # -> data/preprocessed/warehouse_preprocessed.csv
        |
        +-- Obj_1_Clustering/notebooks/      11 EDA -> 12 transform -> 13 features -> 14 model -> 15 evaluate
        +-- Obj_2_Classification/notebooks/  21 EDA -> 22 transform -> 23 features -> 24 PyCaret screen -> 25 Optuna tune + evaluate
        +-- Obj_3_Regression/notebooks/      31 EDA -> 32 transform -> 33 features -> 34 PyCaret screen -> 35 Optuna tune + evaluate
```

The three objectives are independent of each other. Each one reads only from
`data/preprocessed/` and writes only inside its own `Obj_*` folder.

## Completion status

| Objective | Status | Main output |
|---|---|---|
| 1 — Clustering | Complete | Five warehouse segments, including the unrated group |
| 2 — Classification | Complete | Breakdown-risk model and test-set evaluation |
| 3 — Regression | Complete | Shipment-weight recommendations and zone comparisons |

---

## Folder map

```
BBA Project/
├── docs/                        project brief, data dictionary, data quality report, decision log
├── src/common.py                paths, file loading, plot style — nothing analytical
├── data/
│   ├── raw/                     source .xlsx, never edited
│   └── preprocessed/            output of notebook 01, input to all three objectives
├── notebooks/                   shared stage (00, 01)
├── Obj_1_Clustering/
│   ├── data/processed/          objective-specific transformed data
│   ├── feature_engine/          fitted encoders and scalers (.pkl) + feature specification
│   ├── training_and_evaluation/ train/test splits, metric tables, plots
│   ├── model/                   fitted models
│   └── notebooks/
├── Obj_2_Classification/        same five sub-folders
└── Obj_3_Regression/            same five sub-folders
```

---

## Key documents

| File | What it holds |
|---|---|
| [`docs/00_project_brief.md`](docs/00_project_brief.md) | objectives, scope, methodology and exclusions, from the approved scope |
| [`docs/01_data_dictionary.md`](docs/01_data_dictionary.md) | all 24 source columns with business definitions |
| [`docs/02_data_quality_report.md`](docs/02_data_quality_report.md) | findings from notebook 00 — filled in as that notebook runs |
| [`docs/03_decision_log.md`](docs/03_decision_log.md) | every non-obvious decision, with the evidence behind it |

---

## Source files

| File | Role |
|---|---|
| Submitted project brief DOCX / PDF | approved project brief |
| `Data Description.docx` | business definition of each column |
| `SupplyFlow FMCG Solutions.xlsx` | the dataset (copied to `data/raw/`) |
