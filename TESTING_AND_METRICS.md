# Testing Principle and Metric Definitions

## Testing Principles
1. **Syntax and build safety**: ensure every JS module can be parsed (`node --check`).
2. **Data integrity**: verify dataset JSON is valid (`python -m json.tool`).
3. **Runtime smoke test**: serve static site and verify browser can load app entrypoint and dataset.
4. **Visual sanity check**: capture screenshot after rendering to confirm layout and chart area are visible.

## Necessary Metrics Explained
- **Dating Pool Percentage**: Product of demographic probabilities after applying all selected filters.
- **Matching Population**: `relevant_population × dating_pool_percentage`.
- **Market Value Score**: Weighted sum of physical (50%), status (30%), and personality (20%) subscores.
- **Competition Ratio**: `female_population / eligible_men` where `eligible_men = male_population × target_male_percentage`.
- **Future Dating Probability**: Compounded meeting probability projected to age 40.

## Interpretation Notes
- Metrics are **probabilistic estimates**, not deterministic predictions.
- The model assumes partially independent filters and static rates.
- Use outputs for expectations calibration and scenario exploration.
