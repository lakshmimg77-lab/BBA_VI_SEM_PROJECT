# data/preprocessed — cleaned dataset

Produced by `notebooks/01_global_preprocessing.ipynb`. **This is the single input to all three
objectives.** Load it with:

```python
from src.common import load_preprocessed
df = load_preprocessed()
```

| File | Shape | Gaps | Types |
|---|---|---|---|
| `warehouse_preprocessed.csv` | 25,000 rows × 25 columns | none | 18 integer, 7 text |

---

## What changed from the raw file

Every change closes a decision logged in [`../../docs/03_decision_log.md`](../../docs/03_decision_log.md)
section B, with its evidence.

| Change | Column(s) | Decision |
|---|---|---|
| Removed | `WH_Manager_ID` | B1 |
| Kept as the **row key — never a model feature** | `Ware_house_ID` | B1 |
| `'NA'` relabelled `Unrated` (908 rows) | `approved_wh_govt_certificate` | B2 |
| **Added** — 1 for the 908 unrated warehouses | `is_unrated_warehouse` | B5 |
| 990 gaps filled with the median of the `electric_supply` group (24 / 30) | `workers_num` | B4 |
| 11,881 gaps filled with the median year, 2009 | `wh_est_year` | B3 |
| **Added** — 1 where the year was filled | `wh_est_year_missing` | B3 |
| `float64` → `int64` | `workers_num`, `wh_est_year` | B6 |
| Nothing — all outlier-flagged values retained | — | B7 |
| Nothing — all 25,000 rows retained, original order | — | B8 |

---

## Read before using this file

These cautions come from NB 01's own measurements. Ignoring them will produce wrong conclusions without
any error message.

1. **`Ware_house_ID` is a key.** Exclude it from every feature set. Use it to join results back to
   warehouses.
2. **Do not describe warehouse age from the filled `wh_est_year`.** Filling put 49.46% of all rows at
   2009 and cut the standard deviation from 7.528 to 5.457. For any distribution, average or plot of
   establishment year or age, use `wh_est_year_missing == 0` rows only. The same applies to any
   age feature derived from this column.
3. **The filled year understates its relationships.** Its correlation with storage issues is −0.859
   on recorded years but −0.629 after filling. Read correlations involving `wh_est_year` on recorded
   years only.
4. **Whether a year was recorded is not random.** It is missing for every warehouse with 0–2 refill
   requests and every warehouse with 5 transport issues. `wh_est_year_missing` therefore partly
   restates those columns.
5. **Three columns identify the 908 zero-breakdown warehouses with certainty** —
   `is_unrated_warehouse`, the `Unrated` certificate level, and `storage_issue_reported_l3m == 0`.
   Objective 2 should report its scores with and without these warehouses.
6. **Extreme values were kept.** That includes an unusually regular upper tail in `workers_num`
   (every value above 61 occurs exactly five times). Scaling choices for K-Means (Objective 1) and
   least-squares models (Objective 3) must account for it.

---

## Not done here, by design

Each depends on the algorithm, so it belongs to the objective that needs it:

- encoding categorical columns → `Obj_N_*/notebooks/*_data_transformation`
- scaling → same, fitted on the training split only
- derived features → `Obj_N_*/notebooks/*_feature_engineering`
- the Objective 2 risk-class target → `Obj_2_Classification`
- resampling for class imbalance → training split only, in the model-building notebook
- handling the collinear block (`storage_issue_reported_l3m`, `product_wg_ton`, `wh_est_year`) →
  each objective's EDA and feature-engineering notebooks
