"""
Configuration file for Stability Dashboard
Modify these settings to customize the dashboard behavior
"""

# File paths
# Local file path (for users with OneDrive sync)
EXCEL_FILE_PATH = r"C:\Users\mbrancato\OneDrive - A.S. Watson Europe\Documents\KPIsStabilityTAS.xlsx"

# SharePoint link (for manual download - opens in browser)
SHAREPOINT_LINK = "https://asweu-my.sharepoint.com/:x:/g/personal/c_maestroni_eu_aswatson_com/IQDiiFh9cWnfSaV7i4kftPhZAfD0zUT5faDzqQduMg2GcrY?e=jdXTpF"

# Feature toggles
ENABLE_FILE_UPLOAD = True  # Allow users to upload Excel file directly in the dashboard
SHOW_SHAREPOINT_LINK = True  # Show link to SharePoint file for manual download

# Sheet names
STATIC_VALUES_SHEET = "Static Values"

# Dashboard settings
DASHBOARD_TITLE = "Stability Dashboard"
DASHBOARD_ICON = "📊"
PAGE_LAYOUT = "wide"  # Options: "centered", "wide"

# Chart settings
CHART_HEIGHT_INDIVIDUAL = 400  # Height of individual root cause charts
CHART_HEIGHT_SUMMARY = 500     # Height of summary overview chart
CHART_TEMPLATE = "plotly_white"  # Options: "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white"

# Colors
COLOR_ACTUAL_DATA = "#1f77b4"      # Blue - for actual data line
COLOR_THRESHOLD = "#ff7f0e"         # Orange - for threshold line
COLOR_EXCEEDED = "rgba(255, 0, 0, 0.1)"  # Light red - for areas exceeding threshold
COLOR_IMPORTANT_KPI = "#d32f2f"     # Dark red - for important KPI titles

# Default values
DEFAULT_THRESHOLD = 0.05  # 5% - used when threshold not found in Static Values

# Data processing
PERCENTAGE_THRESHOLD = 1  # Values above this are treated as percentages (e.g., 50 vs 0.50)

# Root cause patterns (used to identify root cause columns)
ROOT_CAUSE_PATTERNS = [
    'Maintenance',
    'System Issue',
    'System.Issue',
    'No Defect',
    'Configuration',
    'Test Data',
    'Deployment',
    'TC in Review',
    'Investigate',
    'R Program'
]

# Date column patterns (used to identify date/time columns)
DATE_COLUMN_PATTERNS = ['date', 'week', 'period', 'time']

# Sheets to exclude from BU list
EXCLUDE_SHEETS = [
    STATIC_VALUES_SHEET,
    'Sheet1',
    'Sheet2',
    'Sheet3',
    'Template',
    'Instructions'
]

# Display settings
SHOW_DATA_POINTS_COUNT = True      # Show metric for total data points
SHOW_ROOT_CAUSES_COUNT = True      # Show metric for root causes tracked
SHOW_THRESHOLDS_COUNT = True       # Show metric for thresholds defined
SHOW_SUMMARY_CHART = True          # Show overview chart with all root causes
SHOW_INDIVIDUAL_CHARTS = True      # Show individual charts for each root cause
SHOW_DATA_TABLE = True             # Show raw data table tab

# Grid layout
CHARTS_PER_ROW = 2  # Number of charts to display per row

# Export settings
CSV_FILENAME_TEMPLATE = "{bu}_stability_data.csv"  # Template for exported CSV filename

# Logging
LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"

# Performance
CACHE_TTL = 300  # Cache time-to-live in seconds (5 minutes)

# UI Text
UI_TEXT = {
    "sidebar_header": "⚙️ Configuration",
    "select_bu_label": "Select Business Unit",
    "select_bu_help": "Choose the BU to analyze",
    "refresh_button": "🔄 Refresh Data",
    "file_info_header": "📁 File Information",
    "analysis_header": "📈 Analysis for: {bu}",
    "important_kpis_label": "⭐ **Important KPIs for {bu}:** {kpis}",
    "summary_stats_header": "📊 Summary Statistics",
    "overview_header": "📈 All Root Causes Overview",
    "detailed_analysis_header": "🔍 Detailed Root Cause Analysis",
    "all_charts_tab": "📊 All Charts",
    "data_table_tab": "📋 Data Table",
    "raw_data_header": "Raw Data",
    "download_button": "📥 Download Data as CSV",
    "footer": """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Stability Dashboard v1.0 | Built with Streamlit</p>
        </div>
    """
}

# Error messages
ERROR_MESSAGES = {
    "file_not_found": "❌ Excel file not found at: {path}",
    "file_load_error": "❌ Error loading Excel file: {error}",
    "static_values_not_found": "❌ '{sheet}' sheet not found in Excel file",
    "static_values_error": "❌ Error loading static values: {error}",
    "sheet_not_found": "❌ Sheet '{bu}' not found in Excel file",
    "data_load_error": "❌ Error loading data for {bu}: {error}",
    "no_bu_found": "❌ No Business Units (sheets) found in the Excel file",
    "no_data": "❌ No data available for {bu}",
    "no_root_causes": "⚠️ No root cause columns identified in the data",
    "preparation_error": "❌ Unable to prepare data for visualization",
    "unexpected_error": "❌ An unexpected error occurred: {error}"
}

# Warning messages
WARNING_MESSAGES = {
    "thresholds_not_found": "Thresholds row not found in Static Values sheet",
    "bu_not_found": "BU '{bu}' not found in Static Values sheet"
}

# Info messages
INFO_MESSAGES = {
    "file_exists": "Please ensure the file exists at the specified location.",
    "check_logs": "Please check the logs for more details or contact support."
}
