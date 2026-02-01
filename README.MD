# Ethiopia Financial Inclusion Forecasting (2025–2027)

**Status:** Ongoing

**Author:** Yonatan

**Date:** February 2026  

---

## 📌 1. Business Need & Problem Statement

### The "Data Desert" Paradox
Ethiopia is undergoing a massive digital financial transformation, driven by the launch of **Telebirr (2021)**, the entry of **M-Pesa (2023)**, and aggressive government policy reforms (Fuel Payment Mandate).

However, official data sources (World Bank Findex) lag significantly behind this reality. The last official survey (2022) depicts a **stagnant financial inclusion rate (~46%)**, missing the explosion of **60 Million+** digital wallet accounts opened between 2021 and 2024.

**The Business Problem:**
Policymakers and investors cannot rely on historical linear trends to forecast Ethiopia's financial future because the market has undergone a **structural break**. Traditional models predict stagnation, while reality suggests a boom.

**The Solution:**
This project builds an **Event-Augmented Forecasting Engine** that bridges the gap between sparse official data and high-frequency market signals. We use proxy indicators (operator data) and structural impact modeling to generate a realistic forecast for **2025–2027**.

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

## 🛠️ Installation & Usage

1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/your-username/ethiopia-fi-forecast.git](https://github.com/your-username/ethiopia-fi-forecast.git)
    cd ethiopia-fi-forecast
    ```

2.  **Install Dependencies:**
    ```bash
    pip install pandas numpy matplotlib seaborn scipy statsmodels scikit-learn
    ```

3.  **Run the Pipeline:**
    * **Enrichment:** `python src/task1_enrich.py`
    * **EDA:** Open `notebooks/Task_2_EDA.ipynb`
    * **Impact Modeling:** `python src/task3_impact.py`
    * **Forecasting:** Open `notebooks/Task_4_Forecast.ipynb`

---

## 📂 Project Structure