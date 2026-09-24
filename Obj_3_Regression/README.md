# Objective 3 — Regression: suitable shipment weight

**Serves Objective 3:** *predict a suitable shipment weight for each warehouse, and
compare volumes across the four zones and six regional zones.*

**Target:** `product_wg_ton` — product shipped in the last 3 months, in tons.

A small set of standard regression models is compared, then one final selected model is used for
shipment-weight recommendations.

**Status:** complete. NB 31–35 are written, executed and tied to the decision log.

### What NB 31 established

- **Target shape:** shipment weight is usable in tons without a log or square-root transform.
  - Mean: **22,102.63 t**.
  - Median: **22,101 t**.
  - Skewness: **0.3316**.
  - Kurtosis: **-0.5020**.
- **Main relationships:** shipment weight moves most strongly with:
  - storage issues: Pearson **0.9868**, Spearman **0.9892**;
  - establishment year: Pearson **-0.6050**;
  - breakdowns: Pearson **0.3427**.
- **Location and ownership are weak:** their differences are small beside the spread within each group.
- **VIF check:** zone dummy columns are collinear with one another, but this is expected for one-hot encoded location fields.
  Storage issues and establishment year are not high-VIF problems.

### What NB 32 established

- **One 80/20 split** was made before feature engineering: **20,000 training** and **5,000 test** warehouses.
- **Categorical fields** were encoded simply:
  - certificate grade and capacity as ordinal columns;
  - location and ownership as 0/1;
  - zone and regional zone as one-hot columns.
- **Feature count:** 29 predictors were prepared for modelling.
- **Test set rule:** the 5,000 test warehouses stay untouched until NB 35.

### What NB 33 established

- **No derived feature was added.**
- Warehouse age, operating problem total and infrastructure score were exact re-expressions of existing columns.
- Shops per distributor and staff per distributor added complexity without a meaningful modelling gain.

### What NB 34 established

- **PyCaret compared the standard regression models** named in the project scope:
  linear regression, Ridge, Lasso, linear SVR, decision tree, random forest, AdaBoost, XGBoost and CatBoost.
- **PyCaret selected CatBoost** for the next notebook.
  - CatBoost R²: **0.9943**.
  - XGBoost R²: **0.9938**.
  - Random forest R²: **0.9936**.
- **NB 34 is only model-family screening.** It does not use the fixed test set and it does not tune every model.

### What NB 35 established

- **Optuna tuned only CatBoost**, the model family selected by PyCaret.
  - Best CV R²: **0.9945**.
  - Best parameters: 400 iterations, depth 6, learning rate **0.0405**, L2 leaf regularisation **1.7976**.
- **Final CatBoost test performance:** R² **0.9947**, adjusted R² **0.9947**, MAE **633.68 t**, RMSE **841.52 t**,
  MAPE **4.0003%**.
- **Dominant predictor:** storage issues. Permuting it destroys most of the model's explanatory power.
- **Other useful signals:** certificate grade, establishment year, temperature regulation and transport issues.
- **Zone differences are small compared with within-zone spread.**
  - East has the highest recommended mean: **22,689.25 t**.
  - South has the lowest recommended mean: **21,939.27 t**.
  - The gap between zones is much smaller than the 11,000+ t spread inside each zone.
- **Regional-zone differences are also modest.**
  - Zone 2 has the highest recommended mean: **22,484.46 t**.
  - Zone 1 has the lowest recommended mean: **21,742.83 t**.

---

## Notebooks

| # | Notebook | Purpose | Writes to |
|---|---|---|---|
| 31 | `31_eda_regression.ipynb` | Target distribution with skewness, kurtosis and a normality check — any transform decision follows from those numbers, not from reflex. Scatter plots against the strongest numeric predictors; correlation heatmap; distribution by each categorical; **VIF table** quantifying multicollinearity. | — |
| 32 | `32_data_transformation.ipynb` | Train/test split; no target transform; encoding and scaling note chosen from NB 31. PyCaret handles screening normalization in NB 34. | `data/processed/`, `feature_engine/` |
| 33 | `33_feature_engineering.ipynb` | Derived features proposed with a business rationale, then kept or dropped on measured contribution to explaining shipment weight. | `data/processed/`, `feature_engine/` |
| 34 | `34_data_split_and_model_building.ipynb` | PyCaret model-family screening on training rows only. Chooses CatBoost for NB 35. | `training_and_evaluation/pycaret_regression_model_screening.csv`, `pycaret_regression_selected_model.csv` |
| 35 | `35_model_evaluation.ipynb` | Optuna tunes only CatBoost; final held-out evaluation; residual plots; feature importance; all-warehouse shipment recommendations; zone and regional-zone comparisons. | `training_and_evaluation/`, `model/` |

---

## What NB 35 delivers

1. **The zone comparison.** Objective 3 explicitly requires comparing shipment volumes *"across the
   four zones and six regional zones"*. NB 35 writes:
   - `zone_comparison.csv`
   - `regional_zone_comparison.csv`
   - `zone_recommendation_comparison.png`
   - `regional_zone_recommendation_comparison.png`

2. **An honest reading of model strength.** NB 35 states:
   - the high R² is mainly driven by storage issues;
   - establishment year remains useful but much weaker than storage issues;
   - location and ownership are weak drivers;
   - the result supports the project expectation, with storage issues much stronger than age.

---

## Folders

| Folder | Holds |
|---|---|
| `data/processed/` | the objective's transformed dataset |
| `feature_engine/` | fitted encoders and scalers (`.pkl`) and `feature_spec.md` |
| `training_and_evaluation/` | train/test splits, CV results, metric tables, residual and comparison plots |
| `model/` | fitted and tuned models (`.pkl`) |
| `notebooks/` | the five notebooks above |

Reads from `data/preprocessed/warehouse_preprocessed.csv` only. Never from another objective.

---

## Evaluation metrics

R², adjusted R², MAE, MSE, RMSE and MAPE. Adjusted R² is not in scikit-learn — computed in NB 35
from R², the test-set row count and the number of predictors. MAPE is reported with a note on how
low-volume warehouses affect it, since percentage error inflates as the denominator shrinks.

---

## Findings

- Objective 3 is complete and remains a **simple supervised regression project**.
- The final output is one recommended shipment weight for every warehouse in
  `training_and_evaluation/shipment_weight_recommendations.csv`.
- The model is accurate on the held-out test set: MAE is about **634 tons**, or roughly **4.0%** average percentage error.
- Recommended shipment weight is driven mainly by current storage issues, with establishment year and certificate grade
  adding smaller signals.
- Zone and regional-zone averages are useful for reporting, but they should not be read as strong operational drivers.
- Because the data is one snapshot, the results show **association, not cause**.
