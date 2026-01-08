"""
Quick test script to verify data reading fixes
"""

import pandas as pd
import sys

# Set UTF-8 encoding for console output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

EXCEL_PATH = r"C:\Users\mbrancato\OneDrive - A.S. Watson Europe\Documents\Stability.xlsx"

print("=" * 60)
print("Testing Data Reading Fixes")
print("=" * 60)

try:
    # Test 1: Read Static Values sheet
    print("\n1. Reading Static Values sheet...")
    df_static = pd.read_excel(EXCEL_PATH, sheet_name='Static Values', header=None)
    print(f"   ✓ Loaded {len(df_static)} rows")

    # Test 2: Extract thresholds
    print("\n2. Extracting thresholds...")
    root_cause_names = df_static.iloc[1]
    threshold_values = df_static.iloc[2]

    thresholds = {}
    for col_idx in range(len(root_cause_names)):
        if col_idx < len(threshold_values):
            root_cause = root_cause_names.iloc[col_idx]
            threshold_value = threshold_values.iloc[col_idx]

            if pd.notna(root_cause) and pd.notna(threshold_value):
                thresholds[str(root_cause).strip()] = float(threshold_value)

    print(f"   ✓ Found {len(thresholds)} thresholds:")
    for rc, thresh in thresholds.items():
        print(f"     - {rc}: {thresh*100:.1f}%")

    # Test 3: Extract important KPIs for Kruidvat
    print("\n3. Extracting important KPIs for Kruidvat...")
    bu_names_row = df_static.iloc[5]
    kpis_row = df_static.iloc[6]

    bu_col_idx = None
    for col_idx in range(len(bu_names_row)):
        if pd.notna(bu_names_row.iloc[col_idx]):
            if str(bu_names_row.iloc[col_idx]).strip().lower() == 'kruidvat':
                bu_col_idx = col_idx
                break

    if bu_col_idx is not None and bu_col_idx < len(kpis_row):
        kpis_value = kpis_row.iloc[bu_col_idx]
        if pd.notna(kpis_value):
            important_kpis = [kpi.strip() for kpi in str(kpis_value).split(',') if kpi.strip()]
            print(f"   ✓ Found {len(important_kpis)} important KPIs:")
            for kpi in important_kpis:
                print(f"     - {kpi}")
        else:
            print("   ⚠ No KPIs defined")
    else:
        print("   ⚠ Kruidvat not found in Static Values")

    # Test 4: Read Kruidvat sheet
    print("\n4. Reading Kruidvat sheet...")
    df_kruidvat = pd.read_excel(EXCEL_PATH, sheet_name='Kruidvat')
    print(f"   ✓ Loaded {len(df_kruidvat)} rows, {len(df_kruidvat.columns)} columns")

    # Test 5: Identify root cause columns
    print("\n5. Identifying root cause columns...")
    root_cause_patterns = [
        'Maintenance', 'System Issue', 'No Defect', 'Configuration',
        'Test Data', 'Deployment', 'System.Issue'
    ]

    exclude_patterns = [
        'threshold', 'treshold', 'limit', 'target', 'goal'
    ]

    root_cause_cols = []
    for col in df_kruidvat.columns:
        col_clean = str(col).strip()

        # Skip duplicates (.1, .2, etc.)
        if '.' in col_clean and col_clean.split('.')[-1].isdigit():
            continue

        # Skip threshold columns
        if any(exclude.lower() in col_clean.lower() for exclude in exclude_patterns):
            print(f"   → Skipping threshold column: {col_clean}")
            continue

        if any(pattern.lower() in col_clean.lower() for pattern in root_cause_patterns):
            if df_kruidvat[col].dtype in ['float64', 'int64'] or \
               (df_kruidvat[col].dtype == 'object' and df_kruidvat[col].astype(str).str.contains('%').any()):
                root_cause_cols.append(col)

    print(f"   ✓ Found {len(root_cause_cols)} root cause columns:")
    for rc in root_cause_cols:
        sample_val = df_kruidvat[rc].dropna().iloc[0] if len(df_kruidvat[rc].dropna()) > 0 else "N/A"
        print(f"     - {rc} (sample: {sample_val}, type: {df_kruidvat[rc].dtype})")

    # Test 6: Check percentage conversion
    print("\n6. Testing percentage conversion...")
    for col in root_cause_cols[:3]:  # Test first 3 columns
        sample_values = df_kruidvat[col].dropna().head(5)
        print(f"\n   Column: {col}")
        print(f"   Type: {df_kruidvat[col].dtype}")
        print(f"   Sample values: {sample_values.tolist()}")

        if df_kruidvat[col].dtype in ['float64', 'int64']:
            non_zero = sample_values[sample_values != 0]
            if len(non_zero) > 0:
                pct_above_one = (non_zero > 1).sum() / len(non_zero)
                format_type = "percentage (>1)" if pct_above_one > 0.5 else "decimal (<=1)"
                print(f"   Format detected: {format_type}")

    print("\n" + "=" * 60)
    print("✓ All tests completed successfully!")
    print("=" * 60)

except PermissionError:
    print("\n❌ Excel file is open! Please close it and try again.")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
