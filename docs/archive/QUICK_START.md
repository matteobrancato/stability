# Quick Start Guide

## Running the Dashboard

### Option 1: Command Line
```bash
cd "C:\Users\mbrancato\PyCharm\Automation\Report\stability"
streamlit run stability_dashboard.py
```

### Option 2: Python
```bash
cd "C:\Users\mbrancato\PyCharm\Automation\Report\stability"
py -m streamlit run stability_dashboard.py
```

The dashboard will automatically open in your default browser at: **http://localhost:8501**

## Using the Dashboard

### 1. Select Business Unit
- Use the dropdown in the sidebar to select a BU (e.g., "Kruidvat")
- The dashboard will automatically load and display the data

### 2. View Overview
- **Summary Statistics**: See total data points, root causes, and thresholds
- **All Root Causes Overview**: Combined chart showing all metrics over time

### 3. Analyze Detailed Charts
- Each root cause has its own chart
- Blue line = Actual values
- Orange dashed line = Threshold
- Red shaded area = Values exceeding threshold
- ⭐ = Important KPI (defined in Static Values sheet)

### 4. Export Data
- Go to "Data Table" tab
- Click "Download Data as CSV" button
- Save for further analysis

## Key Features

### Interactive Charts
- **Hover**: See exact values for any data point
- **Zoom**: Click and drag to zoom into specific time periods
- **Pan**: Hold shift and drag to move around
- **Reset**: Double-click to reset view

### Threshold Monitoring
- Automatically compares actual values with thresholds
- Highlights violations in red
- Shows important KPIs with star marker

### Real-time Updates
- Click "Refresh Data" button in sidebar to reload from Excel
- Changes in Excel file will be reflected immediately

## Troubleshooting

### Dashboard won't start
```bash
# Check if Streamlit is installed
py -m pip list | findstr streamlit

# If not installed
py -m pip install -r requirements.txt
```

### Excel file not found
- Verify the file exists at: `C:\Users\mbrancato\OneDrive - A.S. Watson Europe\Documents\Stability.xlsx`
- Check if file is open in Excel (close it and try again)
- Ensure you have read permissions

### No data showing
1. Check if "Kruidvat" sheet exists in Excel file
2. Verify "Static Values" sheet has thresholds
3. Ensure root cause columns contain percentage data

## Next Steps

### For Local Use
- Keep the dashboard running in the terminal
- Open browser to http://localhost:8501
- Share the network URL with colleagues on same network

### For Cloud Deployment
1. Create a GitHub repository
2. Upload these files:
   - stability_dashboard.py
   - requirements.txt
   - Stability.xlsx (or link to cloud storage)
3. Go to https://share.streamlit.io
4. Deploy from your repository
5. Share the public URL

## Tips

- **Performance**: Dashboard loads faster with fewer data points
- **Data Quality**: Ensure consistent date formats in Excel
- **Thresholds**: Update Static Values sheet to change thresholds
- **New BUs**: Add new sheets in Excel, they'll appear automatically
- **Customization**: Edit stability_dashboard.py to add features

## Support

For help:
1. Check README.md for detailed documentation
2. Review error messages in dashboard
3. Check terminal/console for detailed logs
4. Contact development team for assistance
