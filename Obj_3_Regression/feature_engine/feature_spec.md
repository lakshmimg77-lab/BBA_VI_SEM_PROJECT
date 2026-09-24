# Objective 3 — regression feature specification

Written by `notebooks/32_data_transformation.ipynb`.

## Rows and target
- 25,000 warehouses, all kept.
- Target: `product_wg_ton`, kept in recorded tons.
- Split: 20,000 train / 5,000 test, `random_state = 42`.

## Features
- 29 encoded predictors.
- Period measures are kept because Objective 3 models shipment weight as an operational outcome in the same snapshot.
- PyCaret screening in NB 34 uses normalization so scale-sensitive models are compared fairly.
- The final CatBoost model in NB 35 uses the encoded feature table without a manual scaler.

## Encoding
- Certificate: Unrated 0, C 1, B 2, B+ 3, A 4, A+ 5.
- Capacity: Small 1, Mid 2, Large 3.
- Binary columns: `Location_type_Urban`, `wh_owner_type_Rented`.
- One-hot columns: `zone_East`, `zone_South`, `zone_West`, and `WH_regional_zone_Zone_1` through `_Zone_5`.
