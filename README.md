# Nairobi Price Intelligence Dashboard

**Real-time tracking of essential commodity prices in Nairobi, Kenya**

## Overview

Nairobi Price Intelligence monitors fuel, food staples, and public transport costs across Kenya's capital. Built with Python, Streamlit, and Plotly, it transforms raw price data into actionable insights for policymakers, researchers, and everyday consumers.

## Live Dashboard

Open in GitHub Codespaces: `Code → Codespaces → Create codespace on main`

Run: `streamlit run scripts/dashboard.py`

## Key Features

- **6-Month Price Trends**: Visualize inflation across fuel, food, and transport
- **Automated Insights**: Calculated inflation rates with methodology transparency
- **Price Spike Alerts**: Automatic detection of significant month-over-month increases
- **Personal Cost Calculator**: Estimate monthly essential costs based on consumption
- **Data Quality Flags**: Every row labeled as verified, estimated, or crowdsourced
- **CSV Export**: Download filtered data for external analysis

## Data Sources

| Category | Source | Quality | Coverage |
|----------|--------|---------|----------|
| Fuel | EPRA Monthly Pump Prices | Verified Primary | Nov 2025 – Apr 2026 |
| Food | KNBS CPI + Market Estimates | Mixed | Nov 2025 – Apr 2026 |
| Transport | Crowdsourced Matatu Fares | Estimated | Nov 2025 – Apr 2026 |

## Key Insights

1. **Fuel Volatility Drives Transport Inflation**: Petrol prices increased 8.7% over 6 months (KES 160.50 → KES 174.50), while matatu fares rose 14.3% (KES 70 → KES 80). Transport costs outpaced fuel, suggesting cartel pricing power in SACCO-operated routes.

2. **Food Price Resilience**: The essential food basket increased only 3.6% over the same period, indicating stable agricultural supply chains despite global commodity shocks.

3. **Data Quality Transparency**: 55% of data points come from verified primary sources (EPRA/KNBS), 45% from estimated indices. All estimates are clearly flagged with methodology notes.

## Methodology

### Fuel Prices
- Sourced directly from EPRA monthly petroleum pump price reviews
- Nairobi-specific prices extracted from official publications
- Updated manually within 48 hours of EPRA release

### Food Prices
- Baseline verified from KNBS Consumer Price Index (CPI) publications
- Missing months interpolated using KNBS food sub-index trends
- All estimates flagged as `estimated_from_index` with source citations

### Transport Prices
- Route-specific fares collected via commuter reports
- Eastlands, Westlands, and Rongai routes tracked as representative samples
- Adjusted monthly based on fuel price correlation

## Tech Stack

- Python 3.12
- Pandas (data manipulation)
- Plotly (interactive visualizations)
- Streamlit (dashboard framework)

## Running Locally

```bash
git clone https://github.com/Omondi-je/Nairobi-Price-Intelligence.git
cd Nairobi-Price-Intelligence
pip install pandas plotly streamlit
streamlit run scripts/dashboard.py
