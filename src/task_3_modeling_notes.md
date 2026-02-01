# Task 3: Impact Modeling Notes
**Analyst:** Selam_Analyst_Manual  
**Date:** 2026-01-30  
**Model Type:** Rule-Based Structural Model (Intervention Analysis)

---

## 1. Model Philosophy
This model avoids "fitting the answer" (using realized 2024 data to predict 2021). Instead, it defines **Structural Rules** based on economic logic. We assume that specific classes of events (Product Launches, Mandates) exert directional pressure on financial inclusion metrics with variable lags.

The forecasting engine (Task 4) will use these links to:
1.  Identify when a regime change occurred.
2.  Apply a "boost factor" (Magnitude) to the baseline trend.
3.  Account for delayed effects (Lag).

---

## 2. Structural Assumptions

### A. Telebirr Launch (May 2021)
* **Mechanism:** Product Launch (Infrastructure + Platform).
* **Impact on USAGE:** `High` Magnitude, `0` Lag.
    * *Justification:* Mobile money registration is instant and requires low friction (USSD). The impact on user counts is immediate upon launch due to the existing Ethio Telecom subscriber base.
* **Impact on ACCESS:** `Medium` Magnitude, `12` Month Lag.
    * *Justification:* While users register quickly, "Financial Inclusion" (as defined by Findex) often requires perceiving the account as a formal financial tool. Literature from Kenya (M-Pesa) suggests a lag between "using to send money" and "considering oneself banked."

### B. Mandatory Fuel Payment (July 2023)
* **Mechanism:** Policy Mandate (Forced Adoption).
* **Impact on USAGE:** `High` Magnitude, `1` Month Lag.
    * *Justification:* Regulatory mandates force behavioral change faster than organic market forces. The lag is minimal because non-compliance meant inability to purchase fuel.

### C. M-Pesa Market Entry (Aug 2023)
* **Mechanism:** Competition / Market Entry.
* **Impact on USAGE:** `Medium` Magnitude, `6` Month Lag.
    * *Justification:* Unlike the incumbent (Telebirr), the entrant must build an agent network from scratch. Impact accelerates after the agent network reaches critical density (estimated 6 months).

---

## 3. Pillar Normalization
To ensure data integrity, all model inputs have been normalized to the strict schema:
* `ACCESS` (Capitalized)
* `USAGE` (Capitalized)
* `INFRASTRUCTURE` (Capitalized)

---

## 4. Limitations & Risks

1.  **No Endogenous Feedback:** The model currently links *Events* $\rightarrow$ *Indicators*. It does not model how *Usage* growth might feedback into *Access* growth (e.g., a virtuous cycle).
2.  **Magnitude Uncertainty:** Magnitudes are currently categorical (`High`/`Medium`). In Task 4, these must be converted to numeric weights (e.g., High = 1.2x multiplier, Medium = 1.1x multiplier) or calibrated against the limited data points.
3.  **Regional Heterogeneity:** The model assumes national-level impact. It does not account for the fact that the "Fuel Mandate" likely impacted Addis Ababa (Urban) much faster than rural regions.
4.  **Active vs. Registered:** The model links events to "Registered Users" (Proxy). It likely overestimates the impact on "Active 90-day Usage," which is the stricter Findex standard.

---

## 5. Schema Compliance Check
* **Event Lookups:** Performed via `event_name` (Canonical) rather than `indicator`.
* **Data Leakage:** `impact_estimate` is set to `NaN`. The forecast model must solve for the coefficient, rather than having the answer hard-coded.