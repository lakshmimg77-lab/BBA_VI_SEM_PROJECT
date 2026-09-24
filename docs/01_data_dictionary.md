# 01 — Data Dictionary

Source: `Data Description.docx`, provided with the dataset. The **Business definition** column is
quoted from that document. Everything else in this file is a *design intention* recorded before
analysis — it says how we expect to treat each field, not what the data actually contains.

> **Nothing in this file has been verified against the data yet.** Actual dtypes, missingness,
> cardinality and distributions are measured in `notebooks/00_preliminary_analysis.ipynb` and
> written up in [`02_data_quality_report.md`](02_data_quality_report.md). Where reality differs
> from the "Expected" column below, the report wins and this file gets corrected.

Dataset: `data/raw/SupplyFlow FMCG Solutions.xlsx` — one row per warehouse, 24 columns.

---

## Columns

| # | Variable | Business definition (as supplied) | Expected type | Intended role |
|---|---|---|---|---|
| 1 | `Ware_house_ID` | Product warehouse ID | identifier | drop — row identifier |
| 2 | `WH_Manager_ID` | Employee ID of warehouse manager | identifier | drop — row identifier |
| 3 | `Location_type` | Location of warehouse like in city or village | nominal | predictor (all 3 objectives) |
| 4 | `WH_capacity_size` | Storage capacity size of the warehouse | **ordinal** | predictor — has a natural size order |
| 5 | `zone` | Zone of the warehouse | nominal | predictor; also the grouping variable for the Objective 3 zone comparison |
| 6 | `WH_regional_zone` | Regional zone of the warehouse under each zone | nominal | predictor; second grouping variable for the Objective 3 comparison |
| 7 | `num_refill_req_l3m` | Number of times refilling has been done in last 3 months | count | predictor — operational activity |
| 8 | `transport_issue_l1y` | Any transport issue like accident or goods stolen reported in last one year | count | predictor — operational problem |
| 9 | `Competitor_in_mkt` | Number of instant noodles competitor in the market | count | predictor — market context |
| 10 | `retail_shop_num` | Number of retail shops who sell the product under the warehouse area | count | predictor — demand catchment |
| 11 | `wh_owner_type` | Company is owning the warehouse or they have got the warehouse on rent | nominal | predictor — ownership |
| 12 | `distributor_num` | Number of distributors working between warehouse and retail shops | count | predictor — distribution network |
| 13 | `flood_impacted` | Warehouse is in the flood impacted area indicator | binary | predictor — location risk |
| 14 | `flood_proof` | The warehouse has flood proof indicators, e.g. storage raised off the ground | binary | predictor — infrastructure |
| 15 | `electric_supply` | Warehouse has electric back-up like a generator, so they can run the [operation] | binary | predictor — infrastructure |
| 16 | `dist_from_hub` | *(see note below)* — distance of the warehouse from the hub | continuous | predictor — logistics |
| 17 | `workers_num` | Number of workers working in the warehouse | count | predictor — staffing |
| 18 | `wh_est_year` | Warehouse established year | year | predictor; source for a derived **warehouse age** |
| 19 | `storage_issue_reported_l3m` | Warehouse reported storage issues to the corporate office in the last 3 months, e.g. rats, fungus from moisture | count | predictor — operational problem |
| 20 | `temp_reg_mach` | Warehouse has temperature regulating machine indicator | binary | predictor — infrastructure |
| 21 | `approved_wh_govt_certificate` | What kind of standard certificate has been issued to the warehouse by the government regulatory body | **ordinal** | predictor — has a natural grade order |
| 22 | `wh_breakdown_l3m` | The number of times the warehouse faced a breakdown in the last 3 months, e.g. worker strike, flood, electrical failure | count | **Objective 2 target** (banded into risk classes); predictor elsewhere |
| 23 | `govt_check_l3m` | Number of times government officers visited the warehouse to check quality and expiry of stored food in the last 3 months | count | predictor — regulatory attention |
| 24 | `product_wg_ton` | Product shipped in the last 3 months, weight in tons | continuous | **Objective 3 target**; predictor elsewhere |

---

## Notes on the source document

**`dist_from_hub` has the wrong description.** `Data Description.docx` repeats the
`electric_supply` text verbatim ("Warehouse have electric back up like generator, so they can run
the") for `dist_from_hub`. This is a copy-paste error in the supplied document, not a data problem.
The variable name and modelling context indicate distance from the distribution hub, and
NB 00 checks whether the observed values are consistent with a distance measure.

**Two descriptions are truncated mid-sentence** (`electric_supply`, `dist_from_hub`) — again a
defect in the supplied document.

---

## Variable roles by objective

| Objective | Target | Notes on feature selection |
|---|---|---|
| 1 — Clustering | none | Unsupervised. Feature set is chosen in NB 13 from the redundancy evidence in NB 11 — a distance-based algorithm double-counts any group of features that measure the same thing. |
| 2 — Classification | `wh_breakdown_l3m` → 2 risk classes: **Not High Risk** `0–3`, **High Risk** `4–6` (defined in NB 21 §3.3, replacing an earlier three-class banding) | The source count column is dropped once the class label is derived, to prevent the target leaking into the features. |
| 3 — Regression | `product_wg_ton` | All other columns are candidate predictors. Multicollinearity is quantified by the VIF table in NB 31 and acted on in NB 32/33. |

**Fields that are targets in one objective and predictors in another** (`wh_breakdown_l3m`,
`product_wg_ton`) are contemporaneous measurements from the same three-month window, not lagged
values. They are legitimate predictors of association but cannot support a causal or forward-looking
claim — the single-snapshot caveat applies and must be restated in the closing
interpretation of any objective that uses them.

---

## Terms

- **l3m** — last 3 months.
- **l1y** — last 1 year.
- **wh / WH** — warehouse.
- **ton** — shipment weight unit for `product_wg_ton`.
