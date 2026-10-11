# Covid-19-Case_Study
Exploratory data analysis and time-series trend tracking of global COVID-19 confirmed, recovery, and mortality rates using Python (Pandas &amp; Matplotlib).

## Key Analytical Insights & Findings

- **Time-Series Epidemic Surges:** Evaluated daily incremental case spikes using first-order differencing (`diff()`) across European epicenters (Germany, France, and Italy), pinpointing single-day peak acceleration dates.
- **Recovery Rate Disparity (Dec 31, 2020):** Cross-compared benchmark resilience metrics between Canada and Australia ($Recoveries / Confirmed$), revealing operational differences in national case resolution.
- **Sub-National Mortality Variation:** Audited provincial mortality distribution ($Deaths / Confirmed$) across Canada, isolating the highest and lowest case-fatality ratios to measure geographic healthcare resilience.
- **Data Integrity & Imputation:** Addressed spatial and temporal missingness across latitude, longitude, and historical timestamps using localized centered moving averages (window = 3) alongside forward-fill imputation.

---

## Technical Toolchain & Methods
- **Language:** Python
- **Libraries:** Pandas, Matplotlib
- **Techniques:** Missing Value Imputation (Mode, Forward Fill, Moving Average), Time-Series Differencing, Aggregations & Pivot Analysis
