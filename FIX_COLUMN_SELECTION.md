# Fix for Column Selection Issue

## Problem Identified

Based on your terminal logs and the Excel file structure, the issue was:

### Excel Column Structure (Kruidvat sheet)
The Excel file has **DUPLICATE columns** with the same names:

**Count Columns (WRONG - these are raw counts):**
- `System Issue`: values like 60, 98, 241 (max=241)
- `No Defect`: values like 0, 0, 225 (max=225)
- `Test Data`: values like 190, 186, 358 (max=358)
- `Configuration`: values like 6, 8, 632 (max=632)

**Percentage Columns (CORRECT - these are calculated percentages):**
- `System Issue.1`: values like 0.016, 0.026, 0.059 (max=0.059 = 5.9%)
- `No Defect.1`: values like 0.000, 0.000, 0.054 (max=0.054 = 5.4%)
- `Test Data.1`: values like 0.050, 0.049, 0.088 (max=0.088 = 8.8%)
- `Configuration.1`: values like 0.002, 0.003, 0.155 (max=0.155 = 15.5%)
- `Maintenance`: values like 0.011, 0.002, 0.016 (max=0.016 = 1.6%)

Note: Pandas automatically adds `.1`, `.2` suffixes when Excel has duplicate column names.

## Root Cause

The previous code was:
1. **Skipping all `.1` columns** - assuming they were duplicates to ignore
2. This meant it only saw the COUNT columns
3. COUNT columns have values like 60, 241, 632
4. When divided by 100, these became 0.60 (60%), 2.41 (241%), 6.32 (632%)
5. Result: Charts showing 60%, 241%, 632% instead of 1.6%, 5.9%, 15.5%

## Solution Applied

Modified `identify_root_cause_columns()` in `stability_dashboard.py` (lines 259-321):

### Key Changes:

1. **Process ALL columns (including .1, .2)**
   - Removed the early skip for duplicate columns
   - Now evaluates EVERY column based on its values

2. **Strip .1, .2 for grouping**
   ```python
   base_name = col_clean.replace(' %', '').replace('%', '').strip()
   if '.' in base_name and base_name.split('.')[-1].isdigit():
       base_name = base_name.rsplit('.', 1)[0].strip()
   ```
   - "System Issue" → base_name: "System Issue"
   - "System Issue.1" → base_name: "System Issue"
   - Both map to the same base_name for comparison

3. **Value-based detection**
   ```python
   pct_below_one = (non_zero < 1).sum() / len(non_zero)
   is_real_percentage = pct_below_one > 0.7  # 70% of values < 1
   ```
   - Count columns: 0% of values < 1 → NOT percentage
   - Percentage columns: 100% of values < 1 → IS percentage

4. **Collision handling**
   ```python
   if base_name in percentage_cols:
       existing_max = df[percentage_cols[base_name]].dropna().max()
       if max_val < existing_max:
           percentage_cols[base_name] = col  # Replace with better column
   ```
   - When multiple columns have same base_name
   - Keep the one with LOWER max value
   - Example: System Issue (max=241) vs System Issue.1 (max=0.059)
   - Keeps System Issue.1 ✓

## Test Results

Tested with quick script:

```
System Issue: max=241.0000, %<1=0.0% → pct=False
System Issue.1: max=0.0590, %<1=100.0% → pct=True

No Defect: max=225.0000, %<1=0.0% → pct=False
No Defect.1: max=0.0540, %<1=100.0% → pct=True

Test Data: max=358.0000, %<1=0.0% → pct=False
Test Data.1: max=0.0880, %<1=100.0% → pct=True

Configuration: max=632.0000, %<1=0.0% → pct=False
Configuration.1: max=0.1550, %<1=100.0% → pct=True

Maintenance: max=0.0160, %<1=100.0% → pct=True

Final selection:
  Maintenance: Maintenance
  System Issue: System Issue.1
  No Defect: No Defect.1
  Configuration: Configuration.1
  Test Data: Test Data.1
```

✓ All correct columns selected!

## Expected Dashboard Behavior

After this fix, the dashboard will:

1. **Select the correct columns**
   - System Issue.1, No Defect.1, Configuration.1, Test Data.1, Maintenance

2. **Show realistic values**
   - Maintenance: 0.2% - 1.6% range
   - System Issue: 1.6% - 5.9% range
   - No Defect: 0.0% - 5.4% range
   - Configuration: 0.2% - 15.5% range
   - Test Data: 4.9% - 8.8% range

3. **Charts match Excel**
   - Values from columns Q, R, S, T, U (the ones you pointed to)
   - Orange threshold lines at correct positions
   - Red shading where values exceed thresholds
   - ⭐ on Maintenance, System Issue, Test Data (important KPIs)

## How to Test

**IMPORTANT: Close the Excel file first!**

Then run:
```bash
launch_dashboard.bat
```

Or:
```bash
streamlit run stability_dashboard.py
```

### What to verify:

1. **Root Causes Tracked**: Should show 5
2. **Chart values**: All between 0-20% (not 60%, 241%, 632%!)
3. **Column names in logs**: Should see "System Issue.1" selected, not "System Issue"
4. **Graphs match Excel**: Compare with your screenshot values

## Why Only Maintenance Worked Before

Maintenance was the ONLY root cause that didn't have a duplicate:
- There was only ONE "Maintenance" column
- It had percentage values (0.011, 0.002, etc.)
- So it was always selected correctly

All others had TWO columns:
- One with counts (wrong)
- One with percentages (.1 version - correct)

The old code only saw the first one, hence the wrong values.

## Status

✓ Fix applied to `stability_dashboard.py`
✓ Tested with Excel file
✓ All 5 root causes now select correct columns
✓ Ready to run dashboard

**Next step**: Close Excel and run the dashboard to see the corrected charts!
