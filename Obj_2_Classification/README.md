# Objective 2 — Classification: warehouse breakdown risk

**Serves Objective 2:** *build a model that estimates whether a warehouse will report a
breakdown*, so preventive maintenance can be planned rather than reacted to.

**Target:** `wh_breakdown_l3m`, banded into two risk classes (NB 21 §3.3).

| Class | `wh_breakdown_l3m` | Warehouses | Reading |
|---|---|---|---|
| Low | 0 – 1 | 2,944 (11.78%) — 908 of them unrated | at most one breakdown in three months |
| Medium | 2 – 3 | 10,082 (40.33%) | two or three |
| High | 4 – 6 | 11,974 (47.90%) | four or more — more than one a month; priority for preventive action |

**Why these boundaries.** An earlier design banded the count 0–2 / 3–4 / 5–6. NB 21 §3.2 found both of those
boundaries sat where warehouses do not differ on any related feature (η² 0.0003–0.0006), keeping only 50.3% of the
features' relationship with breakdowns among rated warehouses. The boundary now used sits on a real step. NB 22 re-checked it on the
training split alone and confirmed it: the boundary steps are 31–36 times larger than any step inside a class.

The source count column is dropped once the class label is derived, so the target cannot leak into the features.

**Status:** complete. NB 21–25 are written, executed and tied to the decision log.

### The split

**20,000 training / 5,000 test warehouses**, stratified by class (`random_state = 42`), fixed once in NB 22 and stored as
the `split` column of `data/processed/classification_base.csv`. **Every decision from NB 22 onward uses training
warehouses only**; the test set is first used in NB 25.

| Class | Train | Test |
|---|---|
| Low | 2,355 | 589 |
| Medium | 8,066 | 2,016 |
| High | 9,579 | 2,395 |

### What NB 22 established

- **The banding holds on training data, on a narrower claim than the rule as written.** The 3|4 boundary step is *not* the
  largest of the six adjacent steps — 0|1 and 1|2 are larger. Both track the 908 newly commissioned warehouses and
  keep **0% of the signal among rated warehouses**, so they measure commissioning status, not risk. Among the steps
  that separate operating warehouses, 3|4 leads by roughly 33–38 times (0.0266 / 0.0282 / 0.0384 against at most
  0.0008 / 0.0008 / 0.0010).
- **The filled year is kept** *with* its missing-flag. The flag says nothing alone, but separates 9,516 unknown years
  from 391 genuine 2009s — and genuine 2009s are 59.59% High Risk against 47.92% for unknown-year warehouses.
- **Encoding:** certificate grade and capacity are ordinal; location and ownership are 0/1; zone and regional zone are
  one-hot, with the most common training level as reference — **29 feature columns**.
- **Scaling** is used only inside PyCaret's screening step so LR/SVM are not disadvantaged by scale. The final
  AdaBoost model uses the encoded feature table without a manual scaler.
- **No shape transformation** (largest skew 1.610).

### What NB 23 established — on training warehouses, by rules fixed before the run

- **12 of 34 features carry information about risk alone.** The strong ones are storage issues (15.10% of class
  uncertainty), shipment weight, establishment year, and certificate status with its unrated flag. Temperature regulation
  and urban location carry a little.
- **Shipment weight removed.** It duplicates storage issues (0.9892), and removing it costs neither probe model.
- **The 19 features with no information alone are kept**, because removing them costs the random forest 0.0076
  macro-F1. A shuffled-column control shows that gain is **mechanical** (more columns to sample), so they are kept as a
  modelling aid, not as evidence those conditions matter.
- **No derived feature added.** Age and tons per worker re-express existing columns; storage issues per 1,000 t,
  shops per distributor and unprotected flood exposure add nothing.
- **Final set: 28 features** (characteristics-only subset: 24) → `data/processed/classification_model_input.csv`.

### What NB 24 established — PyCaret model screening on training rows only

- **PyCaret compared the standard classification models** named in the project scope:
  logistic regression, Gaussian Naive Bayes, decision tree, random forest, linear SVM, AdaBoost, XGBoost and CatBoost.
- **PyCaret selected AdaBoost** for the next notebook. An earlier screening on the three-class target had selected
  Gaussian Naive Bayes; that choice was superseded when the target became binary.
  - AdaBoost Macro F1: **0.6137**.
  - CatBoost Macro F1: **0.6117**; random forest **0.6103**; logistic regression **0.6086**.
  - Gaussian NB ranks **last of eight** at **0.3957** — on a binary target it collapses onto one class
    (recall 0.068 against precision 1.000).
  - The top four families sit within **0.005** macro-F1 of each other, so no family dominates.
- **No resampling** was applied to the selected model.
  - AdaBoost without resampling: macro-F1 **0.6127**.
  - Random oversampling: **0.6013**.
  - Random undersampling: **0.6013**.
  - AdaBoost does not expose a class-weight parameter directly.
- **Files written:** `pycaret_model_screening.csv`, `pycaret_selected_model.csv` and `imbalance_probe.csv`.

### What NB 25 established — Optuna tuning and final test-set evaluation

- **Optuna tuned only AdaBoost**, the model family selected by PyCaret.
  - Best CV macro-F1: **0.6197**.
  - Best parameters: `n_estimators = 298`, `learning_rate = 1.9348`.
- **Final all-feature AdaBoost:** accuracy **0.6122**, macro-F1 **0.6063**, weighted-F1 **0.6043**,
  macro ROC-AUC **0.6547**.
- **Characteristics-only AdaBoost:** macro-F1 **0.5807**, so current operating measures add useful signal.
- **Per class on the 5,000 held-out warehouses:**

  | Class | Precision | Recall | F1 | Warehouses |
  |---|---|---|---|---|
  | High Risk | 0.571 | **0.767** | 0.654 | 2,395 |
  | Not High Risk | 0.687 | 0.470 | 0.558 | 2,605 |

  - 1,836 of 2,395 high-risk warehouses are correctly flagged, at the cost of 1,380 false alarms.
  - The model leans towards predicting High Risk, which suits a prioritisation use but makes a flag only
    ~57% reliable on its own.
- **Most useful signals (permutation importance):** storage issues **0.0496**, establishment year **0.0100**,
  certificate grade **0.0025**. 21 of the 28 features score zero or below.
- **Outcome:** the 908 unrated warehouses are all Not High Risk and trivially correct; among rated
  warehouses Not High Risk is the harder of the two classes, at recall 0.470.

### What NB 21 established

- **Three numeric features differ most by class** — establishment year (η² 0.1002, recorded years), storage issues
  (0.0820) and shipment weight (0.0732), all *medium* effects. High-risk warehouses are older, ship more and log more
  storage issues.
- **Certificate status is the strongest categorical signal** (V 0.2049), closely followed by the unrated flag (V 0.1861).
  All 908 unrated warehouses are Not High Risk. Among rated warehouses alone the certificate falls to V 0.0873 —
  negligible — so most of that signal is the unrated group.
- **Every other feature is negligible** — refills, government checks, transport issues, staffing, distance, market,
  location, zone, capacity, ownership, flood exposure, electric back-up, temperature regulation, and whether the year was
  recorded.
- **Shipment weight and storage issues duplicate each other** (Spearman 0.989, VIF 67.47 / 62.38).
- **Filling the missing years halves the year's signal** (η² 0.1002 → 0.0525).
- **Expectation recorded before modelling:** the 908 unrated warehouses will be trivially correct; Not High Risk will be the harder class among
  rated warehouses.

### Decisions

| Decision | Status |
|---|---|
| Binary target: Not High Risk 0–3 / High Risk 4–6 | closed on review (NB 21 §3.3) |
| All 23 candidate features; best model refitted on characteristics only for comparison | closed on review |
| One stratified 80/20 split, made in NB 22 | closed on review |
| Target banding re-checked on the training split | confirmed on the narrower claim (NB 22 §3) |
| Filled establishment year kept with its missing-flag | closed (NB 22 §4) |
| Encoding; PyCaret screening normalization; no shape transform | closed (NB 22 §5–§6, NB 24) |
| Shipment weight removed; storage issues kept | closed (NB 23 §3) |
| 19 no-information features kept as a modelling aid | closed (NB 23 §4) |
| No derived feature added | closed (NB 23 §5) |
| No resampling for selected AdaBoost | closed (NB 24 §3) |
| ~~PyCaret selection: Gaussian Naive Bayes~~ | superseded |
| PyCaret selection: AdaBoost; Optuna tunes only that model | closed (NB 24 §2, NB 25 §2) |
| Expected: unrated trivially correct; Not High Risk harder | tested (NB 25 §3) |

---

## Notebooks

| # | Notebook | Purpose | Writes to |
|---|---|---|---|
| 21 | `21_eda_classification.ipynb` | Class balance; distribution of each numeric **by class**; **chi-square** for every categorical against the class and **ANOVA / Kruskal–Wallis** for every numeric, with effect sizes. Establishes which features actually discriminate between risk tiers. | — |
| 22 | `22_data_transformation.ipynb` | **The stratified 80/20 split** and the target re-check on training rows; year representation; encoding; scaling specification; shape. | `data/processed/classification_base.csv`, `feature_engine/feature_roles.csv`, `feature_engine/feature_spec.md` |
| 23 | `23_feature_engineering.ipynb` | Five derived candidates with business reasons; a mutual-information screen against shuffled-target baselines; cross-validated probe models (logistic regression, random forest, 25 training folds) deciding feature removal, retention and derived candidates by rules fixed in advance; a shuffled-column control. | `data/processed/classification_model_input.csv`, `feature_engine/model_features.csv`, `candidate_features.csv`, `information_screen.csv`, `probe_comparisons.csv` |
| 24 | `24_data_split_and_model_building.ipynb` | PyCaret model-family screening on training rows only; custom Macro F1; selected-model imbalance check. Chooses AdaBoost for NB 25. | `training_and_evaluation/pycaret_model_screening.csv`, `pycaret_selected_model.csv`, `imbalance_probe.csv` |
| 25 | `25_model_evaluation.ipynb` | Optuna tunes only AdaBoost; final held-out evaluation; all-features vs characteristics-only comparison using the same model family; confusion matrix, ROC/PR curves, permutation importance and test predictions. | `training_and_evaluation/`, `model/` |

---

## Folders

| Folder | Holds |
|---|---|
| `data/processed/` | the objective's transformed dataset |
| `feature_engine/` | fitted encoders and scalers (`.pkl`) and `feature_spec.md` |
| `training_and_evaluation/` | train/test splits, CV results, metric tables, plots |
| `model/` | fitted and tuned models (`.pkl`) |
| `notebooks/` | the five notebooks above |

Reads from `data/preprocessed/warehouse_preprocessed.csv` only. Never from another objective.

---

## Evaluation metrics

Accuracy, precision, recall, F1 score, ROC-AUC and PR-AUC. With two classes these are reported
per class and as macro and weighted averages; ROC-AUC and PR-AUC are computed one-vs-rest.

---

## Findings

- The classification model is suitable as a **simple risk-prioritisation aid**, not as an automatic maintenance decision.
- Warehouses with more storage issues and older establishment years tend to fall into higher breakdown-risk tiers.
- The unrated group must be interpreted separately: all 908 are Not High Risk by construction, though at 6.97% of that
  class they no longer dominate it as they did under the old three-class banding.
- Same-period operating measures improve prediction, so the model is partly reading current operating condition, not only
  warning signs available before a breakdown.
- The final score is modest: macro-F1 **0.6063**. The usable result is recall — **76.7% of high-risk warehouses are
  flagged** — rather than accuracy, since a flag is only ~57% reliable on its own.
- Seven of the eight screened families landed within 0.04 macro-F1 of one another, which suggests the ceiling is the
  information in a single snapshot rather than the choice of algorithm.
- Because the dataset is one snapshot, the result shows **association, not cause**.
