# Data Enrichment Log – Task 1
Project: Ethiopia Digital Financial Transformation Forecasting  
Task: Data Exploration and Enrichment  
Date: 2026-01-30  
Collected by: Selam_Analyst_Manual  

---

## 1. Purpose

This document records all exploration findings, manual enrichments, and assumptions made during Task 1. The goal is to prepare a clean, auditable dataset suitable for forecasting financial access and usage in Ethiopia.

---

## 2. Original Dataset Overview

### 2.1 Record Counts (Before Enrichment)

| Dimension | Count |
|---------|------|
| Total records | 43 |
| Observations | 3 |
| Events | 4 |
| Impact Links | 36 |

### 2.2 Records by Pillar

| Pillar | Count |
|------|------|
| Access | 3 |
| Usage | 0 (Major Gap) |
| Infrastructure | 0 |
| Policy | 1 |
| Enablers | 0 |

### 2.3 Records by Source Type

| Source Type | Count |
|------------|------|
| Regulator | 5 |
| Operator | 2 |
| Survey | 3 |
| International | 0 |

### 2.4 Records by Confidence

| Confidence | Count |
|-----------|------|
| High | 38 |
| Medium | 5 |
| Low | 0 |

---

## 3. Temporal Coverage

- Earliest observation date: 2014-12-31
- Latest observation date: 2021-12-31
- Primary gaps identified:
  - **Critical Gap:** No usage data between 2021–2024 (The "Boom" period).
  - Limited post-2023 survey-based inclusion metrics.

---

## 4. Indicator Coverage

### 4.1 Unique Indicators (indicator_code)

List of key indicators present:
- `ACC_OWNERSHIP` (Account Ownership Rate)
- `EVT_FX_REFORM` (Foreign Exchange Liberalization)
- `EVT_CROSSOVER` (P2P Transaction Count Surpasses ATM)

Coverage issues:
- `ACC_OWNERSHIP` stops at 2021.
- No high-frequency usage indicators (e.g., Active Users, Transaction Volume) were present in the starter file.

---

## 5. Existing Events Review

Existing events captured in the dataset include:
- Foreign Exchange Liberalization (2024)
- M-Pesa EthSwitch Integration (2025 - Future Dated)
- EthioPay Instant Payment System Launch (2025 - Future Dated)

Limitations:
- **Telebirr Launch (2021)** was missing (Critical omission).
- **Mandatory Fuel Payment (2023)** was missing.

---

## 6. Manual Enrichments Added

### 6.1 New Events

| Event Name | Category | Date | Source | Confidence | Notes |
|-----------|--------|------|--------|-----------|------|
| Telebirr Launch | product_launch | 2021-05-11 | Ethio Telecom | High | Created mobile money market |
| M-Pesa Launch | market_entry | 2023-08-16 | Safaricom | High | Introduced competition |
| Mandatory Digital Fuel Payment | policy | 2023-07-01 | NBE | Medium | Forced usage driver |

**Source URLs**
- https://www.ethiotelecom.et/
- https://safaricom.et/
- https://nbe.gov.et/

---

### 6.2 New Observations (Proxy Data)

| Indicator | Year / Date | Value | Source | Confidence | Justification |
|---------|------------|------|--------|-----------|--------------|
| Telebirr Users | 2024-01-01 | 54.0 M | Ethio Telecom | High | Proxy for mobile money usage |
| Telebirr Users | 2022-06-01 | 27.0 M | Ethio Telecom | Medium | Interpolated midpoint |
| M-Pesa Users | 2024-01-01 | 10.0 M | Safaricom | High | Market entry traction |
| Inflation (%) | 2022-12-31 | 33.89 | World Bank | High | Affordability headwind |
| Inflation (%) | 2023-12-31 | 30.22 | World Bank | High | Continued macro pressure |

**Original Text Examples**
- "Telebirr has grown to over 54 million users" – Ethio Telecom report
- "M-Pesa... now has over 10 million users" – Safaricom Press Release

---

## 7. Impact Links (Initial Assessment)

No new `impact_link` records were populated in Task 1.

However, the following relationships were identified for modeling in Task 3:
- Telebirr Launch → Increase in mobile money usage indicators
- M-Pesa Launch → Competitive acceleration of usage growth
- Digital fuel mandate → Short-term increase in transaction volume

These will be formalized with lag estimates and magnitudes in Task 3.

---

## 8. Assumptions and Limitations

- Proxy values (Telebirr/M-Pesa user counts) were used where official national time-series data was unavailable.
- Inflation data was added as a "Negative Enabler" to explain potential stagnation in savings despite high usage.
- No forecasting or model fitting was performed in Task 1.
- Impact magnitudes are not yet estimated.

---

## 9. Outcome

The enriched dataset:
- Conforms strictly to the unified schema.
- Preserves event/observation separation (Events have `pillar=NaN`).
- Is suitable for exploratory analysis and forecasting model design.

**Task 1 objectives are satisfied.**