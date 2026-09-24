# Objective 2 — classification feature specification

Written by `notebooks/22_data_transformation.ipynb`. Updated by NB 23 if features are added or removed.

## Rows and target
- **25,000 warehouses**, all kept.
- **Target `breakdown_risk`**: Not High Risk 0–3 · High Risk 4–6 breakdowns in three months.
  The source count `wh_breakdown_l3m` is removed after the banding re-check on the training split (§3).
- **Split**: **20,000 train / 5,000 test**, stratified by class,
  `random_state = 42`. Stored in the `split` column. The test rows are not used for any decision.

## Features — 29 encoded columns from 23 candidates
| Group | Columns |
|---|---|
| period measures (same period as breakdowns) | `product_wg_ton`, `storage_issue_reported_l3m`, `num_refill_req_l3m`, `govt_check_l3m`, `transport_issue_l1y` |
| characteristics | `wh_est_year`, `workers_num`, `dist_from_hub`, `Competitor_in_mkt`, `retail_shop_num`, `distributor_num`, `electric_supply`, `temp_reg_mach`, `flood_proof`, `flood_impacted`, `is_unrated_warehouse`, `certificate_grade`, `capacity_size`, `Location_type_Urban`, `wh_owner_type_Rented`, `zone_East`, `zone_South`, `zone_West`, `WH_regional_zone_Zone_1`, `WH_regional_zone_Zone_2`, `WH_regional_zone_Zone_3`, `WH_regional_zone_Zone_4`, `WH_regional_zone_Zone_5` |
| recording flag | `wh_est_year_missing` |

`Ware_house_ID` is carried as the key only.

## Encoding — fixed rules, nothing learned from rows
- `approved_wh_govt_certificate` → `certificate_grade`: {'Unrated': 0, 'C': 1, 'B': 2, 'B+': 3, 'A': 4, 'A+': 5}. *Unrated* = 0 is read together with `is_unrated_warehouse`.
- `WH_capacity_size` → `capacity_size`: {'Small': 1, 'Mid': 2, 'Large': 3}.
- One 0/1 column per non-reference level; reference = most common level in the training split: {'Location_type': 'Rural', 'wh_owner_type': 'Company Owned', 'zone': 'North', 'WH_regional_zone': 'Zone 6'}.

## Establishment year
- `wh_est_year` as filled by NB 01, kept together with `wh_est_year_missing`.
- Mutual information with the risk class, training split: flag alone 0.00% of class uncertainty; filled year alone 7.61%; year with missing kept apart 7.68%.
- Judged together with the year, so not subject to NB 23's one-feature screen.

## Scaling
- PyCaret screening in NB 24 uses normalization so LR/SVM are not disadvantaged by scale.
- The final selected classifier is AdaBoost, fitted in NB 25 on the encoded feature table without a manual scaler.
- `RobustScaler` remains rejected: filled `wh_est_year` has IQR 1, which would leave it with spread 5.47 against 0.50–1.20 for the other scaled columns.

## Shape transformation
- None. Largest skew among scaled columns 1.605 (`transport_issue_l1y`); at most 1.390% of training warehouses beyond 3 standard deviations in any of them; extremes retained as real.

## Characteristics-only feature set
`feature_roles.csv`, column `characteristics_only_set`: 24 of 29
columns (all except the 5 period measures).

## NB 23 — feature engineering and selection

Written by `notebooks/23_feature_engineering.ipynb`, on the 20,000 training warehouses only.

- **Duplicate pair:** removed `product_wg_ton`.
- **No information alone:** removed 0 feature(s).
- **Derived features added:** none.
- **Final feature set: 28 features** — listed in `model_features.csv`; model-ready table
  `data/processed/classification_model_input.csv`.
- **Characteristics-only set: 24 features.**
- Evidence: `candidate_features.csv`, `information_screen.csv`, `probe_comparisons.csv`.
