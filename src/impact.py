import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'ethiopia_fi_enriched.csv')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'ethiopia_fi_modeledv1.csv')

def generate_id(prefix="IMP"):
    """Generates a unique short ID."""
    return f"{prefix}_{str(uuid.uuid4())[:8]}"


def main():
    print("--- Starting Task 3: Structural Impact Modeling ---")

    # 1. Load Enriched Data
    if not os.path.exists(INPUT_FILE):
        print("❌ CRITICAL: Enriched data not found.")
        return
    df = pd.read_csv(INPUT_FILE)

    # --- SCHEMA NORMALIZATION (Fixing Issue #3) ---
    # Ensure Pillars are Uppercase (ACCESS, USAGE) to match reference_codes.csv
    if 'pillar' in df.columns:
        df['pillar'] = df['pillar'].str.upper()

    # Ensure event_name exists (Fixing Issue #2)
    if 'event_name' not in df.columns:
        # Fallback logic if Task 1 mapped it differently
        if 'indicator' in df.columns:
            print("⚠️ Warning: 'event_name' missing. Mapping from 'indicator'.")
            df['event_name'] = df['indicator']
        else:
            print("❌ CRITICAL: Schema violation. Neither 'event_name' nor 'indicator' found.")
            return

    print(f"✅ Loaded Data: {len(df)} rows. Schema normalized.")

    # 2. Robust Event ID Mapping
    # --------------------------
    event_mask = df['record_type'] == 'event'

    # Ensure all events have IDs
    if 'record_id' not in df.columns:
        df['record_id'] = np.nan

    # Generate IDs for missing ones
    for idx, row in df[event_mask].iterrows():
        if pd.isna(row['record_id']):
            df.at[idx, 'record_id'] = f"EVT_{str(uuid.uuid4())[:8]}"

    # Create strict lookup dictionary: Name -> ID
    event_map = df[event_mask].set_index('event_name')['record_id'].to_dict()
    print(f"🔗 Event Dictionary Created: {len(event_map)} events.")
    # Debug print to ensure keys are correct
    # print(list(event_map.keys()))

    # 3. Define Structural Model Assumptions (The Logic)
    # ------------------------------------------------
    # NOTE: We do NOT hard-code the result (54M). We define the *mechanism*.

    impacts = []

    # --- LOGIC BLOCK A: Telebirr Launch ---
    # Assumption: Disruptive Product Launch -> High Impact on Usage, Medium on Access
    evt_name = 'Telebirr Launch'
    if evt_name in event_map:
        evt_id = event_map[evt_name]

        # Link 1: Usage (Direct Effect)
        impacts.append({
            'record_id': generate_id(),
            'record_type': 'impact_link',
            'parent_id': evt_id,
            'pillar': 'USAGE',
            'related_indicator': 'USG_TELEBIRR_USERS',
            'relationship_type': 'direct',
            'impact_direction': 'increase',
            'impact_magnitude': 'High',  # Qualitative assessment
            'impact_estimate': np.nan,  # FIX: No hard-coded 54.0. Let the model fit this.
            'lag_months': 0,  # Immediate adoption
            'evidence_basis': 'empirical',
            'confidence': 'High',
            'notes': 'Primary driver of mobile money adoption curve.'
        })

        # Link 2: Access (Indirect/Enabling Effect)
        impacts.append({
            'record_id': generate_id(),
            'record_type': 'impact_link',
            'parent_id': evt_id,
            'pillar': 'ACCESS',
            'related_indicator': 'ACC_OWNERSHIP',
            'relationship_type': 'indirect',
            'impact_direction': 'increase',
            'impact_magnitude': 'Medium',  # Lower than usage because of "OTC" behavior
            'impact_estimate': np.nan,
            'lag_months': 12,  # Lagged effect on formal account ownership
            'evidence_basis': 'literature',
            'comparable_country': 'Kenya',  # M-Pesa trajectory
            'confidence': 'Medium',
            'notes': 'Over-the-counter (OTC) usage often precedes account registration.'
        })

    # --- LOGIC BLOCK B: Mandatory Fuel Payment ---
    # Assumption: Policy Mandate -> High Impact on Transaction Volume
    evt_name = 'Mandatory Digital Fuel Payment'
    if evt_name in event_map:
        evt_id = event_map[evt_name]

        impacts.append({
            'record_id': generate_id(),
            'record_type': 'impact_link',
            'parent_id': evt_id,
            'pillar': 'USAGE',
            'related_indicator': 'USG_DIGITAL_TRANSACTIONS',
            'relationship_type': 'direct',
            'impact_direction': 'increase',
            'impact_magnitude': 'High',
            'impact_estimate': np.nan,
            'lag_months': 1,  # Policy forced rapid compliance
            'evidence_basis': 'expert',
            'confidence': 'High',
            'notes': 'Forced regulatory driver for merchant payments.'
        })

    # --- LOGIC BLOCK C: M-Pesa Entry ---
    # Assumption: Market Entry -> Competition -> Accelerates Growth
    evt_name = 'M-Pesa Ethiopia Launch'  # Ensure this matches Task 1 exact string
    if evt_name in event_map:
        evt_id = event_map[evt_name]

        impacts.append({
            'record_id': generate_id(),
            'record_type': 'impact_link',
            'parent_id': evt_id,
            'pillar': 'USAGE',
            'related_indicator': 'USG_MPESA_USERS',
            'relationship_type': 'direct',
            'impact_direction': 'increase',
            'impact_magnitude': 'Medium',  # High growth, but starting from 0
            'impact_estimate': np.nan,
            'lag_months': 6,  # Time to build agent network
            'evidence_basis': 'theoretical',
            'confidence': 'Medium',
            'notes': 'Competitive entry accelerates overall market awareness.'
        })

    # 4. Append & Save
    # ----------------
    if impacts:
        df_impacts = pd.DataFrame(impacts)

        # Align columns to ensure strict schema compliance
        for col in df.columns:
            if col not in df_impacts.columns:
                df_impacts[col] = np.nan

        # Keep only valid columns
        df_impacts = df_impacts[df.columns]

        df_final = pd.concat([df, df_impacts], ignore_index=True)

        # Save
        df_final.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Success! Added {len(impacts)} Impact Links.")
        print(f"   Saved to: {OUTPUT_FILE}")
    else:
        print("⚠️ Warning: No impacts generated. Check event naming.")


if __name__ == "__main__":
    main()