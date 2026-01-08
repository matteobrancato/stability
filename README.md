# Stability Dashboard

An interactive Streamlit dashboard for monitoring root cause analysis with threshold comparisons.

## Features

- **Interactive Visualizations**: Dynamic charts showing root cause trends over time
- **Threshold Monitoring**: Compare actual values against predefined thresholds
- **Multi-BU Support**: Select different Business Units from a dropdown
- **Important KPI Highlighting**: Automatically highlights critical KPIs
- **Data Export**: Download filtered data as CSV
- **Comprehensive Error Handling**: Robust error handling for all edge cases

## Installation

1. Ensure Python 3.8+ is installed
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Locally

```bash
streamlit run stability_dashboard.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository, branch, and `stability_dashboard.py`
5. Click "Deploy"

**Important**: When deploying, you'll need to update the `EXCEL_FILE_PATH` in the code to point to a file accessible by the cloud instance (e.g., uploaded to the repo or a cloud storage service).

## File Structure

```
stability/
├── stability_dashboard.py  # Main dashboard application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Excel File Requirements

The Excel file should contain:

1. **Static Values Sheet**: Contains thresholds and important KPIs for each BU
   - Row with "Thresholds" label containing threshold percentages
   - Rows with BU names listing their important KPIs

2. **BU Sheets** (e.g., "Kruidvat"): Contains weekly data
   - Date/Week column
   - Root cause columns (Maintenance, System Issue, Configuration, Test Data, etc.)
   - Values as percentages (e.g., "5.00%" or 0.05)

## Dashboard Features

### Overview Section
- Total data points
- Number of root causes tracked
- Number of defined thresholds

### All Root Causes Overview
- Combined line chart showing all root causes over time
- Interactive tooltips with exact values

### Detailed Analysis
- Individual charts for each root cause
- Threshold line overlay
- Highlighted regions where values exceed thresholds
- Important KPIs marked with ⭐

### Data Table
- Raw data view with formatted percentages
- CSV export functionality

## Error Handling

The dashboard includes comprehensive error handling for:
- Missing Excel file
- Missing sheets or columns
- Invalid data formats
- Empty datasets
- Permission errors

## Customization

To customize the dashboard:

1. **Change file path**: Update `EXCEL_FILE_PATH` constant
2. **Modify colors**: Edit color codes in chart creation methods
3. **Add new visualizations**: Extend the `StabilityDashboard` class
4. **Change thresholds**: Update values in the Static Values sheet

## Troubleshooting

### Dashboard won't start
- Verify Python is installed: `python --version`
- Check all dependencies are installed: `pip list`
- Ensure Excel file exists at the specified path

### Data not displaying
- Check sheet names match exactly (case-sensitive)
- Verify root cause columns contain numeric/percentage data
- Ensure Static Values sheet has correct format

### Performance issues
- Large datasets may take longer to load
- Consider filtering data by date range if needed

## Support

For issues or questions, please contact the development team or create an issue in the project repository.

## Version History

- **v1.0** (2025-01-07): Initial release
  - Multi-BU support with Kruidvat as primary
  - Interactive Plotly charts
  - Threshold monitoring
  - Important KPI highlighting
  - CSV export functionality
