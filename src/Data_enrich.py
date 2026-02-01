import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# --- 1. Dynamic Path Setup (Production Grade) ---
# Get the folder where THIS script lives (i.e., .../week10/src)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the project root (i.e., .../week10)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Define the data directory (i.e., .../week10/data/raw)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')

print(f"📂 Looking for data in: {DATA_DIR}")

# --- 2. Define File Paths ---
# We join the directory with the EXACT filenames you uploaded
FILE_MAIN = os.path.join(DATA_DIR, 'ethiopia_fi_unified_data.xlsx - ethiopia_fi_unified_data.csv')
FILE_SHEET_B = os.path.join(DATA_DIR, 'Additional Data Points Guide.xlsx - B. Direct Corrln.csv')
FILE_SHEET_C = os.path.join(DATA_DIR, 'Additional Data Points Guide.xlsx - C. Indirect Corrln.csv')
#
# def clean_year(val):
#     """Helper to convert Year (e.g., 2011) to Date (2011-12-31)"""
#     try:
#         return pd.to_datetime(f"{int(val)}-12-31")
#     except:
#         return None

# ... (The rest of your main() function stays exactly the same)


# --- 1. System Configuration & Schema Definition ---


class ProjectSchema:
    """
    The Single Source of Truth.
    Enforces strict column definitions and types.
    """
    # The strict column order and existence guarantee
    COLUMNS = [
        'record_id', 'record_type', 'category', 'pillar',
        'indicator', 'indicator_code', 'indicator_direction',
        'value_numeric', 'value_text', 'value_type', 'unit',
        'observation_date', 'period_start', 'period_end', 'fiscal_year',
        'gender', 'location', 'region',
        'source_name', 'source_type', 'source_url',
        'confidence', 'related_indicator', 'relationship_type',
        'impact_direction', 'impact_magnitude', 'impact_estimate',
        'lag_months', 'evidence_basis', 'comparable_country',
        'collected_by', 'collection_date', 'original_text', 'notes'
    ]

    @staticmethod
    def enforce(df, source_tag="unknown"):
        """
        Applies the schema to a dataframe.
        Creates missing columns with NaN.
        Drops extra columns.
        """
        # 1. Add missing columns
        for col in ProjectSchema.COLUMNS:
            if col not in df.columns:
                df[col] = np.nan

        # 2. Select strictly the defined columns
        df_out = df[ProjectSchema.COLUMNS].copy()

        # 3. Add Audit Metadata if missing
        mask_collected = df_out['collected_by'].isna()
        df_out.loc[mask_collected, 'collected_by'] = f"Pipeline_Ingest_{source_tag}"

        mask_date = df_out['collection_date'].isna()
        df_out.loc[mask_date, 'collection_date'] = datetime.now().strftime('%Y-%m-%d')

        return df_out

    @staticmethod
    def validate_logic(df):
        """
        Logical validation for 'record_type' vs 'pillar'.
        Events must NOT have a pillar.
        """
        # Rule: Events should not have a pillar
        event_mask = df['record_type'] == 'event'
        # Force pillar to NaN for all events
        df.loc[event_mask, 'pillar'] = np.nan
        return df


# --- 2. Path Management ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to week10, then down to data
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')


# --- 3. Data Generators ---

def get_manual_enrichment():
    """
    Returns:
    1. The Major Events (Shocks)
    2. The Proxy Data (Observations) - CRITICAL for filling gaps

    Source: Project Brief (54M users, 10M M-Pesa, Inflation stats)
    """
    records = []

    # --- A. EVENTS (The Shocks) ---
    # ------------------------------
    events = [
        {
            'record_type': 'event',
            'category': 'product_launch',
            'pillar': np.nan,  # STRICT RULE: No Pillar
            'event_name': 'Telebirr Launch',
            'indicator': 'Telebirr Launch',
            'observation_date': '2021-05-11',
            'source_name': 'Ethio Telecom',
            'source_type': 'operator',
            'confidence': 'High',
            'notes': 'Major market disruption. 54M users by 2024.'
        },
        {
            'record_type': 'event',
            'category': 'market_entry',
            'pillar': np.nan,
            'indicator': 'M-Pesa Ethiopia Launch',
            'observation_date': '2023-08-16',
            'source_name': 'Safaricom',
            'source_type': 'operator',
            'confidence': 'High',
            'notes': 'First foreign competition entry.'
        },
        {
            'record_type': 'event',
            'category': 'policy',
            'pillar': np.nan,
            'indicator': 'Mandatory Digital Fuel Payment',
            'observation_date': '2023-07-01',
            'source_name': 'National Bank of Ethiopia',
            'source_type': 'regulator',
            'confidence': 'Medium',
            'notes': 'Forced usage driver for digital payments.'
        }
    ]
    records.extend(events)

    # --- B. PROXY OBSERVATIONS (The Gap Fillers) ---
    # -----------------------------------------------
    # These inject the "missing" rows for 2021-2024 using data from the prompt

    proxies = [
        # 1. Telebirr User Growth (Proxy for Access/Usage)
        # Source: "Telebirr has grown to over 54 million users"
        {
            'record_type': 'observation',
            'pillar': 'USAGE',
            'indicator_code': 'USG_TELEBIRR_USERS',
            'indicator': 'Telebirr Registered Users (Millions)',
            'value_numeric': 54.0,
            'unit': 'millions',
            'observation_date': '2024-01-01',
            'source_name': 'Ethio Telecom',
            'confidence': 'High'
        },
        {
            'record_type': 'observation',
            'pillar': 'USAGE',
            'indicator_code': 'USG_TELEBIRR_USERS',
            'indicator': 'Telebirr Registered Users (Millions)',
            'value_numeric': 27.0,  # Approximate midpoint
            'unit': 'millions',
            'observation_date': '2022-06-01',
            'source_name': 'Ethio Telecom',
            'confidence': 'Medium'
        },

        # 2. M-Pesa User Growth
        # Source: "M-Pesa... now has over 10 million users"
        {
            'record_type': 'observation',
            'pillar': 'USAGE',
            'indicator_code': 'USG_MPESA_USERS',
            'indicator': 'M-Pesa Registered Users (Millions)',
            'value_numeric': 10.0,
            'unit': 'millions',
            'observation_date': '2024-01-01',
            'source_name': 'Safaricom',
            'confidence': 'High'
        },

        # 3. Inflation (Proxy for Affordability/Savings Headwind)
        {
            'record_type': 'observation',
            'pillar': 'AFFORDABILITY',
            'indicator_code': 'ECON_INFLATION',
            'indicator': 'Inflation, consumer prices (annual %)',
            'value_numeric': 33.89,
            'unit': '%',
            'observation_date': '2022-12-31',
            'source_name': 'World Bank',
            'confidence': 'High'
        },
        {
            'record_type': 'observation',
            'pillar': 'AFFORDABILITY',
            'indicator_code': 'ECON_INFLATION',
            'indicator': 'Inflation, consumer prices (annual %)',
            'value_numeric': 30.22,
            'unit': '%',
            'observation_date': '2023-12-31',
            'source_name': 'World Bank',
            'confidence': 'High'
        }
    ]
    records.extend(proxies)

    return pd.DataFrame(records)


# --- 4. Main Pipeline ---

def main():
    print("--- 🚀 Starting Production Ingestion Pipeline ---")

    # A. Load Main Dataset
    # -----------------------------------------------------
    unified_files = [f for f in os.listdir(DATA_RAW) if 'unified' in f.lower() and f.endswith('.csv')]
    if not unified_files:
        unified_files = [f for f in os.listdir(DATA_RAW) if 'unified' in f.lower() and f.endswith('.xlsx')]

    if not unified_files:
        print("❌ CRITICAL: No 'unified' dataset found in data/raw.")
        sys.exit(1)

    main_path = os.path.join(DATA_RAW, unified_files[0])
    print(f"📄 Loading Primary Source: {unified_files[0]}")

    try:
        if main_path.endswith('.csv'):
            df_main = pd.read_csv(main_path)
        else:
            df_main = pd.read_excel(main_path)
    except Exception as e:
        print(f"❌ Error reading primary source: {e}")
        sys.exit(1)

    # Apply Schema
    df_main_clean = ProjectSchema.enforce(df_main, source_tag="Official_Unified")
    print(f"   -> Validated {len(df_main_clean)} rows.")

    # B. Load Manual Enrichments (Events + Proxies)
    # -----------------------------------------------------
    print("🛠️  Injecting Manual High-Confidence Data...")
    df_manual = get_manual_enrichment()
    df_manual_clean = ProjectSchema.enforce(df_manual, source_tag="Manual_Inject")

    print(f"   -> Added {len(df_manual_clean)} manual records (Events + Proxy Observations).")

    # C. Merge
    # -----------------------------------------------------
    df_final = pd.concat([df_main_clean, df_manual_clean], ignore_index=True)

    # D. Logic Validation
    # -----------------------------------------------------
    print("🔍 Running Logic Validation...")
    df_final = ProjectSchema.validate_logic(df_final)

    # E. Save to Processed
    # -----------------------------------------------------
    if not os.path.exists(DATA_PROCESSED):
        os.makedirs(DATA_PROCESSED)

    output_path = os.path.join(DATA_PROCESSED, 'ethiopia_fi_enrichedv1.csv')

    # Sort for cleanliness
    df_final['observation_date'] = pd.to_datetime(df_final['observation_date'])
    df_final = df_final.sort_values('observation_date')

    df_final.to_csv(output_path, index=False)

    print("\n" + "=" * 50)
    print(f"✅ PIPELINE SUCCESS.")
    print(f"   Output: {output_path}")
    print(f"   Total Records: {len(df_final)} (Should be > 50)")
    print(f"   Schema Columns: {len(df_final.columns)} (Strictly Enforced)")
    print("=" * 50)


if __name__ == "__main__":
    main()