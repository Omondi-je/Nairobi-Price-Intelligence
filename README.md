# Nairobi-Price-Intelligence
# 🇰🇪 Nairobi Price Intelligence Dashboard

**Tracking fuel, food, and transport costs in Kenya's capital**

![Dashboard Screenshot](screenshot.png)

## Overview

Nairobi Price Intelligence is a real-time dashboard monitoring essential commodity prices 
across three critical categories: fuel, food staples, and public transport. Built with 
Python, Streamlit, and Plotly, it transforms raw price data into actionable insights 
for policymakers, researchers, and everyday Nairobians.

## Data Sources

| Category | Source | Quality | Coverage |
|----------|--------|---------|----------|
| Fuel | EPRA Monthly Pump Prices | Verified Primary | Nov 2025 - Apr 2026 |
| Food | KNBS CPI + Market Estimates | Mixed | Nov 2025 - Apr 2026 |
| Transport | Crowdsourced Matatu Fares | Estimated | Nov 2025 - Apr 2026 |

## Key Insights

1. **Fuel Volatility Drives Transport Inflation**: Petrol prices increased 8.7% over 6 months 
   (KES 160.50 → KES 174.50), while matatu fares rose 14.3% (KES 70 → KES 80). 
   Transport costs outpaced fuel, suggesting cartel pricing power in SACCO-operated routes.

2. **Food Price Resilience**: The essential food basket (maize flour, milk, rice, sugar, bread) 
   increased 9.6% over the same period, indicating stable agricultural supply chains despite 
   global commodity shocks.

3. **Data Quality Transparency**: 55% of data points come from verified primary sources 
   (EPRA/KNBS), 45% from estimated indices. All estimates are clearly flagged with 
   methodology notes for reproducibility.

## Methodology

### Fuel Prices
- Sourced directly from EPRA monthly petroleum pump price reviews
- Nairobi-specific prices extracted from PDF publications
- Updated monthly within 48 hours of EPRA release

### Food Prices
- Baseline verified from KNBS Consumer Price Index (CPI) publications
- Missing months interpolated using KNBS food sub-index trends
- All estimates flagged as `estimated_from_index` with source citations

### Transport Prices
- Route-specific fares collected via commuter reports
- Eastlands, Westlands, and Rongai routes tracked as representative samples
- Adjusted monthly based on fuel price correlation (0.87 Pearson coefficient)

## Tech Stack

- **Python 3.12** — Data processing
- **Pandas** — Data manipulation
- **Plotly** — Interactive visualizations
- **Streamlit** — Dashboard framework
- **SQLite** — Local data storage

## Running Locally

```bash
git clone https://github.com/yourusername/nairobi-price-intelligence.git
cd nairobi-price-intelligence
pip install pandas plotly streamlit
streamlit run scripts/dashboard.py
