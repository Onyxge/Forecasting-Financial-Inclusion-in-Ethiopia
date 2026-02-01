# Ethiopia Financial Inclusion Forecasting (2025–2027)

**Status:** Ongoing

**Author:** Yonatan

**Date:** February 2026  

---

## 1. Project Goal and Business Context

### The Problem

Official financial inclusion data for Ethiopia (World Bank Global Findex) is sparse and outdated. The most recent official survey (2022) reports a stagnant account ownership rate of approximately **46 percent**, failing to capture the structural break introduced by the launch of **Telebirr (2021)** and **M-Pesa (2023)**. These platforms collectively onboarded more than **60 million users within four years**, creating a major disconnect between official inclusion metrics and observed digital financial behavior.

### The Solution

This project develops a custom **Event-Augmented Forecasting Engine**. By enriching sparse survey-based indicators with high-frequency proxy data from mobile money operators and embedding causal impact rules, the system produces realistic forecasts for **2025–2027** that explicitly account for Ethiopia’s recent digital payments boom.

---

## 🚀 2. Project Methodology (Tasks)

The project was executed in four rigorous phases:

### **Task 1: Data Enrichment (The "Rescue" Phase)**
* **Goal:** Bridge the 2021–2024 data gap.
* **Action:** We injected 8 high-confidence records into the dataset, including:
    * **Events:** Telebirr Launch (May 2021), Mandatory Fuel Payment (July 2023), M-Pesa Entry (Aug 2023).
    * **Proxies:** Operator-reported user counts (54M Telebirr users) and macroeconomic headwinds (30% Inflation).
* **Outcome:** A "Model-Ready" dataset (`ethiopia_fi_enriched.csv`) that captures the digital boom.

### **Task 2: Exploratory Data Analysis (The "Insight" Phase)**
* **Goal:** Validate the hypothesis.
* **Key Insight:** We visualized the **"Inclusion Paradox"**—Account Ownership (Official) grew only +3% while Usage (Proxies) grew +5000%.
* **Outcome:** Confirmed that "Registered Users" is a leading indicator for "Financial Access," validating our ratio-based modeling approach.

### **Task 3: Structural Impact Modeling (The "Logic" Phase)**
* **Goal:** Teach the model *causality*.
* **Action:** We created a rules-based engine (`ethiopia_fi_modeled.csv`) that links specific events to forecast adjustments:
    * *Telebirr Launch* → **High Boost** to Usage (Immediate).
    * *Fuel Mandate* → **High Boost** to Transaction Volume (Forced Adoption).
* **Outcome:** A causal lookup table used to adjust baseline trends.

### **Task 4: Forecasting (The "Prediction" Phase)**
* **Goal:** Predict Account Ownership for 2025–2027.
* **Method:** We deployed a **Bayesian Ensemble** of 5 models:
    1.  **Trend Regression:** Pessimistic baseline (History repeats).
    2.  **Logistic Saturation:** Ceiling-aware growth (Caps at 100%).
    3.  **External Drivers:** Event-augmented growth (Trend + Shocks).
    4.  **Ratio Nowcasting:** Using Telebirr proxy to fix the 2025 starting point.
    5.  **Scenario Synthesis:** Combining all above into Pessimistic, Base, and Optimistic futures.

---

## 📊 3. Key Limitations

Transparency is critical for forecasting. The following limitations apply:

1.  **The "Active vs. Registered" Gap:**
    * Our proxy models rely on "Registered User" counts (54M). However, Findex defines inclusion as "Active Usage." We applied a **65% discount factor** to correct for this, but the true conversion rate remains an estimate.
2.  **Lack of Regional Granularity:**
    * The model assumes national-level impact. In reality, policy shocks like the "Fuel Mandate" likely impacted Addis Ababa (Urban) faster than rural regions. Regional data was unavailable.
3.  **No Endogenous Feedback:**
    * The model treats "Usage" and "Access" as separate tracks. It does not dynamically model the "virtuous cycle" where increased usage *causes* increased savings behavior over time.
4.  **Inflation Uncertainty:**
    * While we modeled inflation as a "Headwind," its specific quantitative drag on account opening is difficult to isolate from other macroeconomic factors.

---

## 🔮 4. Future Work

To improve forecast accuracy in Phase 2, we recommend:

1.  **Regional Disaggregation:** Acquire regional telecom penetration data to model the "Urban-Rural Divide."
2.  **Agent Network Modeling:** Incorporate "Agent Density" as a leading indicator, as proximity to agents is the #1 predictor of sustained usage.
3.  **Dynamic System Model:** Move from spreadsheet-based logic to a Python System Dynamics model (e.g., PySD) to capture feedback loops.

---

## 3. Environment Setup

### Clone the Repository

```bash
git clone https://github.com/your-username/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast
```

### Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Usage Guide

The pipeline is modular and should be executed in the following order.

### Step 1: Data Enrichment (Task 1)

Injects missing events (Telebirr, M-Pesa) and high-frequency proxy indicators into the raw dataset.

```bash
python src/task1_enrich.py
```

**Output:**

* `data/processed/ethiopia_fi_enriched.csv`

---

### Step 2: Exploratory Data Analysis (Task 2)

Open `notebooks/Task_2_EDA.ipynb` to analyze the **Inclusion Paradox**: stagnant official access metrics versus explosive digital usage growth.

---

### Step 3: Impact Modeling (Task 3)

Applies causal rules that translate discrete events into directional pressure on inclusion indicators.

```bash
python src/task3_impact.py
```

**Output:**

* `data/processed/ethiopia_fi_modeled.csv`

---

### Step 4: Forecasting (Task 4)

Open `notebooks/Task_4_Forecast.ipynb` to generate forecasts for **2025–2027** using a five-model ensemble approach combining:

* Trend regression
* External drivers
* Saturation-aware growth
* Ratio-based nowcasting
* Scenario analysis

---

## 5. Unified Schema Reference

The project uses a strict unified schema to merge surveys, events, and causal rules.

| Field              | Description                                   | Allowed Values or Examples                                   |
| ------------------ | --------------------------------------------- | ------------------------------------------------------------ |
| `record_type`      | Defines the function of the row               | `observation`, `event`, `impact_link`, `target`              |
| `pillar`           | Financial inclusion dimension                 | `ACCESS`, `USAGE`, `INFRASTRUCTURE`                          |
| `indicator_code`   | Unique metric identifier                      | `ACC_OWNERSHIP`, `USG_TELEBIRR_USERS`, `EVT_TELEBIRR_LAUNCH` |
| `value_numeric`    | Numeric value of the indicator                | `46.0` (%), `54.0` (millions), `30.2` (inflation)            |
| `impact_magnitude` | Strength of causal effect (impact links only) | `High`, `Medium`, `Low`                                      |
| `lag_months`       | Delay before impact materializes              | `0`, `6`, `12`                                               |
| `confidence`       | Reliability of the source                     | `High`, `Medium`, `Low`                                      |

---

## 6. Data Sources

The enriched dataset draws from the following sources:

* **World Bank Global Findex**: Historical account ownership (2014, 2017, 2022)
* **Ethio Telecom (Audited Reports)**: Telebirr user counts and transaction metrics
* **Safaricom Ethiopia**: M-Pesa adoption statistics
* **National Bank of Ethiopia**: Policy events, regulatory changes, inflation data
* **GSMA**: Mobile connectivity and digital infrastructure benchmarks

---

## 📂 Project Structure
```
├── data/
│   ├── raw/                      # Original sparse Findex data
│   ├── processed/
│   │   ├── ethiopia_fi_enriched.csv  # Output of Task 1 (Enriched with 8 new records)
│   │   ├── ethiopia_fi_modeled.csv   # Output of Task 3 (Includes causal impact links)
│   │   └── ethiopia_fi_forecast_final.csv # Final predictions (2025-2027)
│
├── notebooks/
│   ├── Task_2_EDA.ipynb          # Exploratory Analysis: The "Inclusion Paradox"
│   └── Task_4_Forecast.ipynb     # The 5-Model Forecasting Ensemble
│
├── src/
│   ├── task1_enrich.py           # Script: Data injection and schema validation
│   └── task3_impact.py           # Script: Causal rules engine (Intervention modeling)
│   ├── data_enrichment_log.md    # Audit trail of manual data additions (Task 1)
│   └── task_3_modeling_notes.md  # Documentation of model assumptions & logic (Task 3)
│
├── README.md                     # Project documentation
└── requirements.txt              # Python dependencies
```