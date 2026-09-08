# 🏙️ NYC Airbnb Market Intelligence — Real Estate Investor Portal

An end-to-end data analytics and market intelligence project analyzing NYC Airbnb data to provide data-driven property acquisition recommendations for prospective real estate investors.

📌 **Live Interactive Dashboards:**
* [Looker Studio Executive Dashboard](https://datastudio.google.com/reporting/4bb8f068-e5bf-4132-819f-49adf315f99e?hl=en)
* [Tableau Public Exploratory Dashboard](https://public.tableau.com/views/NYCAirbnbMarketIntelligenceExploration/Dashboard1?:language=en-US&:sid=&:redirect=auth&publish=yes&showOnboarding=true&:display_count=n&:origin=viz_share_link)

---

## 📌 Business Overview & Objective
Real estate investors often struggle to identify optimal Airbnb properties due to market saturation and varying revenue metrics across NYC neighborhoods. The goal of this project is to answer key investor questions:
1. **Which neighborhood** offers the highest return on investment?
2. **What price range** yields optimal booking conversion without sacrificing margins?
3. **What property type** drives maximum occupancy and annual yield?
4. **What expected occupancy rate & annual revenue** should investors model into financial projections?

---

## 🛠️ Tech Stack & Workflow
* **Python (Pandas, NumPy):** Data cleaning, missing value imputations, outlier removal, and feature engineering (Occupancy Rate & Estimated Annual Revenue calculations).
* **MySQL / SQL:** Relational database warehousing, structural schema definition, and aggregation queries for business insights.
* **Google Sheets & Looker Studio:** Automated pipeline integration for executive-level reporting and decision-making portals.
* **Tableau Public:** Deep-dive exploratory data visualization and spatial analysis for market distribution.

---

## 📊 Executive Summary & Business Recommendations

Based on empirical data analysis across 84,000+ listings:

### 1. Target Neighborhoods
* **Primary Focus:** **Bedford-Stuyvesant & Williamsburg (Brooklyn)** and **Harlem (Manhattan)**.
* **Insight:** While Core Manhattan commands higher average daily rates (ADR), Brooklyn neighborhoods offer superior occupancy rates (~62–68%) and significantly lower entry acquisition costs, delivering higher net yield per invested dollar.

### 2. Pricing Strategy
* **Optimal ADR Sweet Spot:** **$110 – $160 / night**.
* **Insight:** Listings priced within this bracket maintain stable year-round occupancy (>60%). Properties listed above $200 experience sharp drops in utilization unless backed by luxury amenities.

### 3. Property Type Selection
* **Recommended Type:** **Entire Home / Apartment (1–2 Bedrooms)**.
* **Insight:** Entire homes yield **~2.1x higher estimated annual revenue** compared to Private Rooms, benefiting from higher length-of-stay metrics from family and business travelers.

### 4. Financial Projections
* **Expected Occupancy Rate:** **60% – 65%** (~220–240 booked nights/year).
* **Projected Annual Revenue:** **$28,000 – $38,000** per unit/year (gross before operational expenses).

---

## 📁 Repository Structure
```text
├── scripts/
│   ├── data_cleaning.py           # Data Wrangling & Feature Engineering
│   └── import_to_mysql.py         # MySQL Batch Pipeline Script
└── README.md                      # Documentation
