# Objective 1 — clustering feature specification

Written by `notebooks/12_data_transformation.ipynb`. Updated by the feature engineering notebook if the final inputs change.

## Rows
- **24,092 rated warehouses** (`is_unrated_warehouse == 0`) are clustered.
- **908 unrated warehouses** receive their own segment by rule, not by clustering.

## Inputs (unscaled in `data/processed/clustering_base.csv`)
| Input | Why |
|---|---|
| `product_wg_ton` | shipment volume; kept from the near-duplicate pair |
| `num_refill_req_l3m` | refill activity; unrelated to every other measure (as shown in the EDA) |
| `transport_issue_l1y` | reported transport problems (as defined in the EDA) |
| `wh_breakdown_l3m` | reported breakdowns (as defined in the EDA) |

`Ware_house_ID` is carried as the key only.

## Not inputs
| Column(s) | Why | Used for |
|---|---|---|
| `storage_issue_reported_l3m` | near-duplicate of `product_wg_ton`, r = 0.987 | profiling |
| every condition — numeric, 0/1 and categorical | segments are defined by performance only | profiling |
| `wh_est_year_missing` | describes how data was recorded, not the warehouse | restricting year-based profiles to recorded years |

## Transformation
- **Encoding:** none — every input is numeric; no condition is an input.
- **Shape transform:** none — only `transport_issue_l1y` has warehouses beyond 3 standard deviations
  (1.39%, furthest 3.51 SD); a log
  transform would compress the high end, which is the part that matters for segmentation.
- **Scaler:** `StandardScaler` — the only candidate giving each input equal weight
  (25.0% each). `RobustScaler` would give `transport_issue_l1y`
  54.66%; `MinMaxScaler` would give `num_refill_req_l3m`
  33.92% against 15.75% for
  `product_wg_ton`. Fitted in the feature engineering step, on the final inputs, over all rated warehouses (no train/test split in clustering).

## Feature engineering

Five derived candidates were tested against four fixed tests (business meaning; R² from the current inputs below 0.90;
extremes no stronger than the 3.51 SD / 1.39% accepted in the earlier step; no condition column in the segment definition).

| Candidate | R² from the 4 inputs | Furthest SD | Beyond 3 SD | Result |
|---|---|---|---|---|
| `problems_total` | 1.0 | 3.32 | 0.18% | not added |
| `transport_issue_3m` | 1.0 | 3.51 | 1.39% | not added |
| `problems_per_1000t` | 0.6742 | 8.83 | 2.08% | not added |
| `refills_per_1000t` | 0.669 | 6.17 | 2.83% | not added |
| `tons_per_worker` | 0.7365 | 6.28 | 1.02% | not added |

**Final clustering inputs (4):** `product_wg_ton`, `num_refill_req_l3m`, `transport_issue_l1y`, `wh_breakdown_l3m`.

**Model-ready file:** `data/processed/clustering_input_scaled.csv` (24,092 rows), scaled with
`feature_engine/standard_scaler.pkl` (`StandardScaler`, fitted on all rated warehouses).
