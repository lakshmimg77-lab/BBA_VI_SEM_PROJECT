# data/raw — source data

**Do not edit anything in this folder. Do not write anything to it.**

| File | Description |
|---|---|
| `SupplyFlow FMCG Solutions.xlsx` | The dataset as supplied. 25,000 warehouse records, 24 columns, single sheet named `Data`. Copied unchanged from the project root. |

Provenance: secondary data collected by Supply Flow FMCG Solutions, supplied with the project
brief. Column definitions are in [`../../docs/01_data_dictionary.md`](../../docs/01_data_dictionary.md).

This is the only copy the notebooks read from. Load it with:

```python
from src.common import load_raw
df = load_raw()
```

`load_raw()` applies no cleaning and no dtype coercion — the audit in
`notebooks/00_preliminary_analysis.ipynb` must see exactly what pandas sees, including anything
irregular.

Cleaned data goes to [`../preprocessed/`](../preprocessed/), never back into this folder.
