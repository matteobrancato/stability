# Stability Dashboard - Project Summary

## 🎯 Project Overview

The Stability Dashboard is an interactive web application built with Streamlit that visualizes root cause analysis data with threshold monitoring. It allows users to track weekly stability metrics across multiple Business Units (BUs) and compare actual values against predefined thresholds.

## ✅ What Has Been Completed

### Core Files Created

1. **stability_dashboard.py** (Main Application)
   - Interactive Streamlit dashboard with BU selection
   - Dynamic chart generation with Plotly
   - Threshold monitoring and visualization
   - Important KPI highlighting
   - Data export functionality
   - Comprehensive error handling

2. **config.py** (Configuration)
   - Centralized settings management
   - Easy customization of paths, colors, and behavior
   - Fallback values for robustness

3. **requirements.txt** (Dependencies)
   - streamlit >= 1.28.0
   - pandas >= 2.0.0
   - openpyxl >= 3.1.0
   - plotly >= 5.17.0

4. **test_setup.py** (Validation Script)
   - Automated testing of setup
   - Validates dependencies, configuration, and data access
   - Pre-deployment checks

5. **Documentation**
   - README.md: Complete project documentation
   - QUICK_START.md: Getting started guide
   - DEPLOYMENT_GUIDE.md: Streamlit Cloud deployment instructions
   - PROJECT_SUMMARY.md: This file

6. **.gitignore** (Version Control)
   - Excludes sensitive and temporary files
   - Ready for GitHub

## 🎨 Features Implemented

### Dashboard Capabilities

#### 1. Business Unit Selection
- Dropdown menu in sidebar
- Automatically detects all BU sheets in Excel file
- Default selection: "Kruidvat"

#### 2. Data Visualization
- **Summary Overview Chart**: All root causes on one chart
- **Individual Root Cause Charts**:
  - Line chart showing trend over time
  - Threshold overlay (dashed orange line)
  - Highlighted regions where values exceed thresholds (red shading)
  - Important KPIs marked with ⭐

#### 3. Interactive Features
- Hover tooltips with exact values
- Zoom and pan capabilities
- Responsive design
- Real-time data refresh

#### 4. Data Management
- Raw data table view
- CSV export functionality
- Date/time series support

#### 5. Metrics Display
- Total data points
- Number of root causes tracked
- Number of thresholds defined

### Technical Features

#### Error Handling
- File not found errors
- Missing sheets or columns
- Invalid data formats
- Empty datasets
- Permission errors
- Encoding issues

#### Performance
- Efficient data loading
- Prepared for caching
- Optimized chart rendering

#### Code Quality
- Clean, well-documented code
- Type hints for better maintainability
- Logging for debugging
- Modular class-based design

## 📊 Excel File Structure

### Required Sheets

1. **Static Values Sheet**
   ```
   Row 1: Thresholds | Maintenance | System Issue | Test Data | ...
          5%          | 2%          | ...

   Row 2: Kruidvat | Maintenance, System Issue, Test Data
   Row 3: [Other BUs] | [Their important KPIs]
   ```

2. **BU Sheets (e.g., "Kruidvat")**
   - Date/Week column
   - Root cause columns with percentage values
   - Data updated weekly

### Currently Available BUs
Based on your Excel file:
- Kruidvat (Primary - configured)
- Trekpleister
- KVbozza
- ratioE
- KV, TP, IPXL, MRN, SD, SV, TPS, WTR, DRG
- NEXTGENExecutionTime
- ExecutionTimeTestimNR
- re-run
- BOSMA

## 🎯 How It Works

### Data Flow

1. **Load Excel File**
   ```
   Excel File → pandas.ExcelFile → Available Sheets
   ```

2. **Read Static Values**
   ```
   Static Values Sheet → Thresholds + Important KPIs
   ```

3. **Load BU Data**
   ```
   Selected BU Sheet → Raw Data → Clean & Process
   ```

4. **Identify Root Causes**
   ```
   Column Analysis → Root Cause Columns → Extract Data
   ```

5. **Prepare Visualization**
   ```
   Convert Percentages → Time Series → Plotly Charts
   ```

6. **Display Dashboard**
   ```
   Summary Stats + Overview Chart + Individual Charts
   ```

## 🚀 Usage Instructions

### Running Locally

1. **Open Terminal/Command Prompt**
   ```bash
   cd "C:\Users\mbrancato\PyCharm\Automation\Report\stability"
   ```

2. **Make sure Excel file is CLOSED** (important!)

3. **Start Dashboard**
   ```bash
   streamlit run stability_dashboard.py
   ```
   OR
   ```bash
   py -m streamlit run stability_dashboard.py
   ```

4. **Access Dashboard**
   - Automatic: Opens in default browser
   - Manual: Navigate to http://localhost:8501

### Using the Dashboard

1. Select BU from dropdown (sidebar)
2. View summary statistics
3. Analyze overview chart (all root causes)
4. Review individual charts
5. Check data table
6. Export data as CSV if needed
7. Click "Refresh Data" to reload from Excel

## ⚠️ Important Notes

### Before Running
- **Close the Excel file** if it's open (prevents permission errors)
- Ensure you have read access to the Excel file
- Verify all required packages are installed

### File Path
Current path: `C:\Users\mbrancato\OneDrive - A.S. Watson Europe\Documents\Stability.xlsx`

To change: Edit `config.py` and update `EXCEL_FILE_PATH`

### Data Format
- Percentages can be: "5.00%" or 0.05 or 5 (all handled automatically)
- Date column is auto-detected (looks for "date", "week", "period")
- Root cause columns are auto-detected by pattern matching

## 🔧 Customization

### Change Colors
Edit `config.py`:
```python
COLOR_ACTUAL_DATA = "#1f77b4"    # Change to your color
COLOR_THRESHOLD = "#ff7f0e"       # Change threshold color
```

### Change Chart Height
Edit `config.py`:
```python
CHART_HEIGHT_INDIVIDUAL = 400  # Height in pixels
CHART_HEIGHT_SUMMARY = 500
```

### Add New Root Cause Patterns
Edit `config.py`:
```python
ROOT_CAUSE_PATTERNS = [
    'Maintenance',
    'System Issue',
    'Your New Pattern'  # Add here
]
```

### Change Default Threshold
Edit `config.py`:
```python
DEFAULT_THRESHOLD = 0.05  # 5%
```

## 📈 Next Steps

### Immediate (Completed ✅)
- [x] Create dashboard application
- [x] Implement BU selection
- [x] Read thresholds from Static Values
- [x] Create interactive charts
- [x] Add error handling
- [x] Test with Kruidvat data
- [x] Create documentation

### Short-term (To Do)
- [ ] Test with other BUs (Trekpleister, etc.)
- [ ] Standardize remaining sheets
- [ ] Gather user feedback
- [ ] Refine visualizations based on feedback
- [ ] Add any additional features requested

### Medium-term (To Do)
- [ ] Deploy to Streamlit Cloud
- [ ] Share link with team
- [ ] Set up automated data refresh
- [ ] Add filters (date range, specific root causes)
- [ ] Add comparison views (BU vs BU)

### Long-term (To Do)
- [ ] Add predictive analytics
- [ ] Implement email alerts for threshold breaches
- [ ] Create PDF reports
- [ ] Add user authentication
- [ ] Integrate with other data sources

## 🐛 Troubleshooting

### Dashboard won't start
- Check if Python is installed: `py --version`
- Verify packages: `py -m pip list`
- Run test script: `py test_setup.py`

### "Permission denied" error
- **Close the Excel file** in Excel
- Ensure you have read access
- Check if file is locked by another process

### Charts not showing
- Verify root cause columns exist in BU sheet
- Check data format (should be percentages or numbers)
- Look at browser console for errors (F12)

### Data looks wrong
- Verify Static Values sheet has correct thresholds
- Check column names match exactly
- Ensure dates are in proper format

### Performance issues
- Large datasets may take longer to load
- Consider filtering data by date range
- Close other applications to free memory

## 📊 Testing Results

All setup validation tests passed ✅:
- ✓ Package Dependencies
- ✓ Configuration
- ✓ Excel File Access
- ✓ Dashboard Script
- ✓ Requirements File

## 🎓 What You Learned

This project demonstrates:
- Streamlit application development
- Interactive data visualization with Plotly
- Excel data processing with pandas
- Error handling and validation
- Configuration management
- Documentation best practices
- Deployment preparation

## 💡 Key Design Decisions

1. **Streamlit**: Chosen for rapid dashboard development and easy deployment
2. **Plotly**: Selected for interactive, professional-looking charts
3. **Class-based design**: Organized code for maintainability
4. **Config file**: Separated configuration for easy customization
5. **Comprehensive error handling**: Robust application that handles edge cases
6. **Static Values sheet**: Centralized threshold management

## 📞 Support

### Resources
- Project README: See `README.md`
- Quick Start: See `QUICK_START.md`
- Deployment: See `DEPLOYMENT_GUIDE.md`
- Test Setup: Run `test_setup.py`

### Common Issues
1. **File Permission**: Close Excel file before running
2. **Package Missing**: Run `py -m pip install -r requirements.txt`
3. **Wrong Path**: Update `EXCEL_FILE_PATH` in `config.py`
4. **No Data**: Check sheet names and column formats

## 🎉 Success Criteria

✅ Dashboard loads successfully
✅ BU selection works
✅ Thresholds load from Static Values
✅ Charts display correctly
✅ Interactive features work
✅ Data can be exported
✅ Errors are handled gracefully
✅ Code is clean and documented
✅ Ready for deployment

## 📝 Version History

**v1.0** (2025-01-07)
- Initial release
- Multi-BU support with Kruidvat as primary
- Interactive Plotly charts
- Threshold monitoring
- Important KPI highlighting
- CSV export functionality
- Comprehensive documentation

## 🔮 Future Enhancements (Ideas)

- Time range filters
- Trend analysis (week-over-week changes)
- Anomaly detection
- Email notifications
- Mobile responsive design
- Dark mode
- Multiple language support
- Custom report generation
- API integration
- Real-time data updates
- User preferences saving
- Advanced filtering options

---

**Project Status**: ✅ **READY FOR USE**

The dashboard is fully functional and ready to be used locally. Once you're satisfied with the functionality, follow the DEPLOYMENT_GUIDE.md to deploy to Streamlit Cloud for team-wide access.

**Next Action**: Close the Excel file and run `streamlit run stability_dashboard.py` to start using your dashboard!
