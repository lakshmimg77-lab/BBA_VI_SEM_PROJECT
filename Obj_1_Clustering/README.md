# Objective 1 — Clustering: warehouse performance segmentation

**Serves Objective 1:** *find which operational and infrastructure conditions explain the
differences in shipment weight and reported problems across the 25,000 warehouses.*

Unsupervised. There is no target variable. The question is whether the network divides into
distinguishable performance segments, and if so, what separates a strong warehouse from a weak one.

**Status: complete.** NB 11–15 run clean. All clustering decisions closed.

### Segments (NB 14, named in NB 15)

| Segment | Name | Share of network | Profile (NB 15 §5–§6) | Robust to method? (NB 14 §5) |
|---|---|---|---|---|
| 0 | **Newly commissioned, not yet rated** | 3.63% | 5,430 t; no storage issues or breakdowns; median year 2022 | by definition — assigned by rule |
| 1 | **Low volume, few breakdowns** | 25.00% | 12,648 t; 2.07 breakdowns; youngest rated (2017); most C grades | largely (76%) |
| 2 | **Transport-problem** | 16.07% | every warehouse 2–5 transport issues; 0.24 problems per 1,000 t — the most | yes (86%) |
| 3 | **High volume — rarely refilled** | 24.69% | 28,354 t; refills 0–3; 17.8% temperature regulated | tier yes; 3/4 split K-Means-specific |
| 4 | **High volume — frequently refilled** | 30.61% | 28,864 t; refills 4–8; 42.2% temperature regulated | tier yes; 3/4 split K-Means-specific |

Segments 3 and 4 are reported as **two sub-segments of one high-volume tier**.

**Evaluation (NB 15 §2–§3, all 24,092 rated warehouses):** silhouette **0.2405** · Dunn index **0.0004317** ·
Davies–Bouldin **1.298** · Calinski–Harabasz **7,661**. Against K-Means on column-shuffled data, the segments are better on
silhouette, Davies–Bouldin and Calinski–Harabasz, but only slightly (silhouette +0.021). The expectation recorded before modelling is confirmed: these
are tiers cut through a continuum, not natural groups.

---

## What NB 11 established

- **Scaling is required.** Unscaled, `product_wg_ton` holds 99.18% of the variance across all numeric and 0/1
  columns, so distances would be shipment weight alone.
- **Shipment weight and storage issues duplicate each other** (r = 0.987). Refill requests, transport issues and
  breakdowns each vary largely on their own.
- **Few conditions relate to performance.** Among rated warehouses: temperature regulation with refill requests
  (η² 7.12%), certificate grade with shipment weight (3.60%) and storage issues (2.12%), and establishment year
  (ρ −0.872 with storage issues). Location, zone, capacity, ownership and the rest are practically unrelated.
- **There are no natural groups.** Hopkins scores look high, but a column-shuffled control shows that comes from
  the count columns' grid and the shipment–storage line. The performance data is a continuum.

### Design decisions

| Decision | Status |
|---|---|
| Segments are defined by **performance measures only**; conditions profile them afterwards | closed |
| **`product_wg_ton`** is the input; `storage_issue_reported_l3m` is used for profiling | closed |
| **`StandardScaler`** — the only scaler giving the four inputs equal weight (25% each); fitted in NB 13 | closed (NB 12) |
| The **908 unrated warehouses** are a segment of their own, by rule; clustering runs on the **24,092 rated** warehouses | closed |
| **No encoding** — every input is numeric; no condition is an input | closed (NB 12) |
| **No shape transformation** — the only extremes are warehouses with five transport issues (3.51 SD) | closed (NB 12) |
| **No derived feature added** — five candidates tested; two re-express existing inputs exactly, three have extremes driven by small denominators or bring in a condition | closed (NB 13) |
| **k = 4** K-Means segments, plus segment 0 by rule | closed (NB 14) |
| K-Means `n_init=10`, `k-means++`, `random_state=42`; Ward linkage on 5,000 samples | closed (NB 14) |
| **Segment names**; segments 3 and 4 reported as sub-segments of one high-volume tier | closed (NB 15) |

**Clustering inputs:** `product_wg_ton`, `num_refill_req_l3m`, `transport_issue_l1y`, `wh_breakdown_l3m`.

| File | Contents |
|---|---|
| `data/processed/clustering_base.csv` | 24,092 rated warehouses, inputs unscaled (NB 12) |
| `data/processed/clustering_input_scaled.csv` | the same, standard-scaled — **input to NB 14** (NB 13) |
| `feature_engine/standard_scaler.pkl` | fitted scaler; converts cluster centres back to tons and counts (NB 13) |
| `feature_engine/candidate_features.csv` | the five tested features and why none was added (NB 13) |
| `feature_engine/feature_spec.md` | rows, inputs, exclusions and transformations, with decisions |

**Expectation recorded before modelling:** because the data is a continuum, silhouette and Dunn scores will be **modest**. Segments
will be tiers of warehouses, not naturally separate types — useful for describing the network, and to be judged
on how clearly they can be profiled, not on separation scores alone.

---

## Notebooks

| # | Notebook | Purpose | Writes to |
|---|---|---|---|
| 11 | `11_eda_clustering.ipynb` | Univariate, bivariate and multivariate EDA on the candidate operational and infrastructure features. Establishes which features carry independent information and which are redundant — a distance-based algorithm double-counts anything measured twice. | — |
| 12 | `12_data_transformation.ipynb` | Encoding (nominal vs ordinal, decided from NB 11) and scaling. Scaling is not optional here: K-Means uses Euclidean distance, so unscaled ranges would let a few columns dominate. | `data/processed/`, `feature_engine/` |
| 13 | `13_feature_engineering.ipynb` | Derived operational ratios and indices, each proposed with a business reason then kept or dropped on evidence. Redundant members of any collinear block found in NB 11 are removed here. | `data/processed/`, `feature_engine/` |
| 14 | `14_model_building.ipynb` | k selection via elbow and silhouette across a range of k; K-Means; hierarchical clustering (Ward) with a dendrogram; agreement between the two measured by Adjusted Rand Index. | `model/`, `training_and_evaluation/` |
| 15 | `15_evaluation_and_profiling.ipynb` | Silhouette, Dunn index, Davies–Bouldin, Calinski–Harabasz. Cluster profiling over the original un-scaled features, then each segment named in business language. | `training_and_evaluation/` |

---

## Folders

| Folder | Holds |
|---|---|
| `data/processed/` | the objective's transformed dataset |
| `feature_engine/` | fitted encoders and scalers (`.pkl`) and `feature_spec.md` — the record of which features entered the model and why |
| `training_and_evaluation/` | cluster labels, k-selection tables, validation metrics, profiling tables, plots |
| `model/` | fitted K-Means and hierarchical clustering artefacts |
| `notebooks/` | the five notebooks above |

Reads from `data/preprocessed/warehouse_preprocessed.csv` only. Never from another objective.

---

## Evaluation metrics

Silhouette score, **Dunn index**, and cluster profiling. Dunn is not in scikit-learn — a short
helper is defined in NB 15. Davies–Bouldin and Calinski–Harabasz are added as supporting evidence
for the choice of k.

---

## Findings

*Objective 1: which operational and infrastructure conditions explain the differences in shipment weight and reported
problems across the warehouses?* Full evidence: `notebooks/15_evaluation_and_profiling.ipynb` §5–§8.

**1. Strength depends on the measure, so it is stated both ways.** Per warehouse, low-volume warehouses break down least
(2.07 breakdowns) and high-volume ones most (4.25–4.33). **Per ton shipped, the high-volume tier is the strongest part of
the network (0.15 problems per 1,000 t) and the transport-problem segment the weakest (0.24).** High-volume warehouses
also ship the most per worker (978–1,001 t, against 434.73 t for low volume). Storage issues rise in exact step with
volume (0.78–0.80 per 1,000 t in every rated segment), so they mark size, not weakness. The newly commissioned warehouses
are not ranked: they are not yet fully operating.

**2. Three of seventeen recorded conditions go with the differences.**
- **Warehouse age — the clearest (η² 0.3658).** The higher the volume tier, the older the warehouses: median
  establishment year 2017 (low volume), 2009 (transport-problem), 2005 (both high-volume sub-segments).
- **Certificate grade — small and consistent.** The A+ share rises from 10.7% (low volume) to 21.1% (high volume,
  frequently refilled); the C share falls from 29.4% to 19.4%.
- **Temperature regulation — separates the two high-volume sub-segments.** 42.2% of frequently refilled warehouses are
  regulated, against 17.8% of rarely refilled ones.

Location, zone, regional zone, capacity size, ownership, electric back-up, flood exposure, staffing, distance from hub,
competitors, retail shops, distributors and government checks **do not differ between segments** — within about a
percentage point, or the same median, in every rated segment.

**3. The weakest segment is not explained by any recorded condition.** The transport-problem segment matches the network
on every condition. Whatever drives transport problems is not in this dataset, so these fields cannot be used to target
that segment.

**4. The stated expectation holds.** *"Shipment weight is driven mainly by reported storage issues and warehouse age,
while location and ownership appear weak"* — volume tiers align with age, storage issues move in lockstep with volume, and
location (V 0.0510) and ownership (V 0.0155) are negligible.

**Limits.**
- Separation is weak (silhouette 0.2405), so warehouses near a boundary could sit on either side — some are only 27 t
  apart.
- The split of the high-volume tier into rarely and frequently refilled is specific to K-Means.
- Age findings rest on recorded years: 52.5% of the network, and only warehouses with three or more refill requests.
- **The data is a single snapshot, so every finding is association, not cause.**

### NB 15 outputs (`training_and_evaluation/`)

| File | Contents |
|---|---|
| `evaluation_metrics.csv` | silhouette, Dunn index (with numerator and denominator), Davies–Bouldin, Calinski–Harabasz — final segments vs five shuffled baselines |
| `segment_separation.csv` | per-segment silhouette summary and second-nearest segment shares |
| `segment_performance_profile.csv` | five performance measures per segment in recorded units, plus problems and storage issues per 1,000 t and tons per worker from segment totals |
| `segment_condition_tests.csv` | chi-square / ANOVA / Kruskal–Wallis with η² or Cramér's V for all 17 conditions (segments 1–4) |
| `segment_condition_shares.csv` · `segment_numeric_conditions.csv` | condition shares and medians per segment, with recorded-year shares |
| `segment_names.csv` | name, tier, how assigned, robustness to method |
| `silhouette_by_segment.png` · `performance_by_segment.png` · `condition_differences_by_segment.png` · `establishment_year_by_segment.png` | figures |
