"""
Stability Dashboard - Interactive Streamlit Application
Displays root cause analysis with threshold comparisons
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

try:
    from config import *
except ImportError:
    # Fallback constants if config.py is not available
    EXCEL_FILE_PATH = r"C:\Users\mbrancato\OneDrive - A.S. Watson Europe\Documents\Stability.xlsx"
    STATIC_VALUES_SHEET = "Static Values"
    DASHBOARD_TITLE = "Stability Dashboard"
    DASHBOARD_ICON = "📊"
    PAGE_LAYOUT = "wide"
    LOG_LEVEL = "INFO"
    ENABLE_FILE_UPLOAD = True
    SHOW_SHAREPOINT_LINK = True
    SHAREPOINT_LINK = ""

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)


def clean_column_name(col_name: str) -> str:
    """
    Clean column name for display: remove .1, .2 suffixes and format nicely

    Args:
        col_name: Original column name (e.g., "System Issue.1")

    Returns:
        Cleaned name (e.g., "System Issue")
    """
    clean = str(col_name).strip()

    # Remove .1, .2, etc. suffix
    if '.' in clean and clean.split('.')[-1].isdigit():
        clean = clean.rsplit('.', 1)[0].strip()

    # Remove % suffix if present
    clean = clean.replace(' %', '').replace('%', '').strip()

    return clean


class StabilityDashboard:
    """Main dashboard class for stability analysis"""

    def __init__(self, excel_source=None):
        """
        Initialize the dashboard

        Args:
            excel_source: Can be:
                - String path to local Excel file
                - BytesIO object from uploaded file
                - pd.ExcelFile object
        """
        self.excel_source = excel_source
        self.excel_file = None
        self.thresholds_df = None
        self.available_bus = []
        self.data_source = "Unknown"
        self.last_modified = None

    def load_excel_file(self) -> bool:
        """
        Load the Excel file from the provided source

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Case 1: Already a pandas ExcelFile object
            if isinstance(self.excel_source, pd.ExcelFile):
                self.excel_file = self.excel_source
                self.data_source = "Uploaded file"
                logger.info(f"Using provided ExcelFile object")
                logger.info(f"Sheets: {self.excel_file.sheet_names}")
                return True

            # Case 2: BytesIO object (uploaded file)
            elif hasattr(self.excel_source, 'read'):
                self.excel_file = pd.ExcelFile(self.excel_source, engine='openpyxl')
                self.data_source = "Uploaded file"
                logger.info(f"Successfully loaded from BytesIO")
                logger.info(f"Sheets: {self.excel_file.sheet_names}")
                return True

            # Case 3: String path to local file
            elif isinstance(self.excel_source, (str, Path)):
                file_path = Path(self.excel_source)
                if not file_path.exists():
                    st.error(f"❌ Excel file not found at: {file_path}")
                    return False

                self.excel_file = pd.ExcelFile(file_path, engine='openpyxl')
                self.data_source = f"Local: {file_path.name}"
                self.last_modified = pd.Timestamp.fromtimestamp(file_path.stat().st_mtime)
                logger.info(f"Successfully loaded from local file: {file_path}")
                logger.info(f"Sheets: {self.excel_file.sheet_names}")
                return True

            else:
                st.error("❌ Invalid Excel source provided")
                return False

        except Exception as e:
            st.error(f"❌ Error loading Excel file: {str(e)}")
            logger.error(f"Error loading Excel file: {e}", exc_info=True)
            return False

    def load_static_values(self) -> bool:
        """
        Load threshold values and KPIs from Static Values sheet

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if STATIC_VALUES_SHEET not in self.excel_file.sheet_names:
                st.error(f"❌ '{STATIC_VALUES_SHEET}' sheet not found in Excel file")
                return False

            # Read the Static Values sheet WITHOUT headers (structure is custom)
            df = pd.read_excel(self.excel_file, sheet_name=STATIC_VALUES_SHEET, header=None)

            self.thresholds_df = df
            logger.info("Successfully loaded static values")
            logger.info(f"Static Values structure:\n{df.head(10)}")
            return True

        except Exception as e:
            st.error(f"❌ Error loading static values: {str(e)}")
            logger.error(f"Error loading static values: {e}", exc_info=True)
            return False

    def get_bu_thresholds(self, bu_name: str) -> Dict[str, float]:
        """
        Get threshold values for a specific BU

        Args:
            bu_name: Business unit name

        Returns:
            Dictionary of root cause: threshold percentage
        """
        try:
            thresholds = {}

            # Structure is:
            # Row 0: "Thresholds" label
            # Row 1: Root cause names
            # Row 2: Threshold values

            if len(self.thresholds_df) < 3:
                logger.warning("Static Values sheet has less than 3 rows")
                return thresholds

            # Get root cause names from row 1 (index 1)
            root_cause_names = self.thresholds_df.iloc[1]

            # Get threshold values from row 2 (index 2)
            threshold_values = self.thresholds_df.iloc[2]

            # Build thresholds dictionary
            for col_idx in range(len(root_cause_names)):
                if col_idx < len(threshold_values):
                    root_cause = root_cause_names.iloc[col_idx]
                    threshold_value = threshold_values.iloc[col_idx]

                    if pd.notna(root_cause) and pd.notna(threshold_value):
                        root_cause_str = str(root_cause).strip()

                        # Convert threshold to float
                        if isinstance(threshold_value, (int, float)):
                            thresholds[root_cause_str] = float(threshold_value)
                        elif isinstance(threshold_value, str):
                            # Handle percentage strings
                            if '%' in threshold_value:
                                thresholds[root_cause_str] = float(threshold_value.replace('%', '').strip()) / 100
                            else:
                                try:
                                    thresholds[root_cause_str] = float(threshold_value)
                                except ValueError:
                                    logger.warning(f"Could not convert threshold value: {threshold_value}")

            logger.info(f"Loaded thresholds for {bu_name}: {thresholds}")
            return thresholds

        except Exception as e:
            logger.error(f"Error getting BU thresholds: {e}", exc_info=True)
            return {}

    def get_bu_important_kpis(self, bu_name: str) -> List[str]:
        """
        Get list of important KPIs for a specific BU

        Args:
            bu_name: Business unit name

        Returns:
            List of important KPI names
        """
        try:
            # Structure is:
            # Row 5: BU names (Kruidvat, Trekpleister, etc.)
            # Row 6: Important KPIs for each BU

            if len(self.thresholds_df) < 7:
                logger.warning("Static Values sheet doesn't have enough rows for KPI definitions")
                return []

            # Get BU names from row 5 (index 5)
            bu_names_row = self.thresholds_df.iloc[5]

            # Get KPIs from row 6 (index 6)
            kpis_row = self.thresholds_df.iloc[6]

            # Find which column has this BU
            bu_col_idx = None
            for col_idx in range(len(bu_names_row)):
                if pd.notna(bu_names_row.iloc[col_idx]):
                    if str(bu_names_row.iloc[col_idx]).strip().lower() == bu_name.lower():
                        bu_col_idx = col_idx
                        break

            if bu_col_idx is None:
                logger.warning(f"BU '{bu_name}' not found in Static Values sheet")
                return []

            # Get the KPIs string from the same column
            if bu_col_idx < len(kpis_row):
                kpis_value = kpis_row.iloc[bu_col_idx]

                if pd.notna(kpis_value):
                    # Split by comma to get individual KPIs
                    kpis_str = str(kpis_value).strip()
                    important_kpis = [kpi.strip() for kpi in kpis_str.split(',') if kpi.strip()]

                    logger.info(f"Important KPIs for {bu_name}: {important_kpis}")
                    return important_kpis

            return []

        except Exception as e:
            logger.error(f"Error getting BU important KPIs: {e}", exc_info=True)
            return []

    def load_bu_data(self, bu_name: str) -> Optional[pd.DataFrame]:
        """
        Load data for a specific BU

        Args:
            bu_name: Business unit name

        Returns:
            DataFrame with BU data or None if error
        """
        try:
            if bu_name not in self.excel_file.sheet_names:
                st.error(f"❌ Sheet '{bu_name}' not found in Excel file")
                return None

            df = pd.read_excel(self.excel_file, sheet_name=bu_name)

            # Clean column names
            df.columns = df.columns.str.strip()

            logger.info(f"Loaded {len(df)} rows for BU: {bu_name}")
            return df

        except Exception as e:
            st.error(f"❌ Error loading data for {bu_name}: {str(e)}")
            logger.error(f"Error loading BU data: {e}", exc_info=True)
            return None

    def identify_root_cause_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Identify root cause columns in the dataframe

        Args:
            df: Input dataframe

        Returns:
            List of root cause column names
        """
        # Common root cause column patterns
        root_cause_patterns = [
            'Maintenance', 'System Issue', 'No Defect', 'Configuration',
            'Test Data', 'Deployment', 'System.Issue'
        ]

        # Patterns to exclude (these are not actual data columns)
        exclude_patterns = [
            'threshold', 'treshold', 'limit', 'target', 'goal'
        ]

        # STRATEGY: Two-pass approach
        # Pass 1: Find all columns with " %" or "%" suffix (calculated percentages)
        # Pass 2: Only if no % column found for a root cause, add the non-% version

        percentage_cols = {}  # base_name -> column_name mapping for % columns
        non_percentage_cols = {}  # base_name -> column_name mapping for non-% columns

        # First pass: Categorize all columns (including .1, .2 duplicates)
        for col in df.columns:
            col_clean = str(col).strip()

            # Skip if column contains excluded patterns (like "threshold")
            if any(exclude.lower() in col_clean.lower() for exclude in exclude_patterns):
                logger.info(f"Skipping threshold/reference column: {col_clean}")
                continue

            # Check if column name matches root cause patterns
            if any(pattern.lower() in col_clean.lower() for pattern in root_cause_patterns):
                # Verify it contains numeric or percentage data
                if df[col].dtype in ['float64', 'int64'] or \
                   (df[col].dtype == 'object' and df[col].astype(str).str.contains('%').any()):

                    sample_values = df[col].dropna()
                    max_val = sample_values.max() if len(sample_values) > 0 else 0
                    min_val = sample_values.min() if len(sample_values) > 0 else 0

                    if len(sample_values) > 0:
                        # Check if most non-zero values are < 1 (real percentages in decimal form)
                        non_zero = sample_values[sample_values != 0]
                        if len(non_zero) > 0:
                            pct_below_one = (non_zero < 1).sum() / len(non_zero)
                            is_real_percentage = pct_below_one > 0.7  # 70% of values < 1
                            logger.info(f"  Analyzing '{col}': max={max_val:.4f}, min={min_val:.4f}, %<1={pct_below_one:.1%} → real_pct={is_real_percentage}")
                        else:
                            is_real_percentage = False
                            logger.info(f"  Analyzing '{col}': all zeros → real_pct=False")
                    else:
                        is_real_percentage = False
                        logger.info(f"  Analyzing '{col}': empty → real_pct=False")

                    # Extract base name (remove " %", "%", ".1", ".2", etc.)
                    base_name = col_clean.replace(' %', '').replace('%', '').strip()
                    # Also remove .1, .2, etc. suffix for grouping
                    if '.' in base_name and base_name.split('.')[-1].isdigit():
                        base_name = base_name.rsplit('.', 1)[0].strip()

                    # Categorize based on VALUES, not just column name
                    if is_real_percentage:
                        # If base_name already exists, keep the one with lower max value
                        if base_name in percentage_cols:
                            existing_col = percentage_cols[base_name]
                            existing_max = df[existing_col].dropna().max()
                            if max_val < existing_max:
                                logger.info(f"✓ Replacing '{existing_col}' (max={existing_max:.4f}) with '{col}' (max={max_val:.4f})")
                                percentage_cols[base_name] = col
                            else:
                                logger.info(f"✓ Keeping '{existing_col}' (max={existing_max:.4f}) over '{col}' (max={max_val:.4f})")
                        else:
                            percentage_cols[base_name] = col
                            logger.info(f"✓ Selected as PERCENTAGE column: '{col}' (base: '{base_name}')")
                    else:
                        # Only store non-percentage if we don't already have one for this base_name
                        if base_name not in non_percentage_cols:
                            non_percentage_cols[base_name] = col
                            logger.info(f"✗ Skipped as COUNT column: '{col}' (base: '{base_name}')")
                        else:
                            logger.info(f"✗ Ignoring duplicate COUNT column: '{col}' (base: '{base_name}')")

        # Second pass: Build final list, preferring % columns
        root_cause_cols = []

        # Get all unique base names
        all_base_names = set(percentage_cols.keys()) | set(non_percentage_cols.keys())

        for base_name in all_base_names:
            if base_name in percentage_cols:
                # Use the % column
                root_cause_cols.append(percentage_cols[base_name])
                logger.info(f"Selected: '{percentage_cols[base_name]}' (percentage column)")
            elif base_name in non_percentage_cols:
                # No % column available, use non-% column as fallback
                root_cause_cols.append(non_percentage_cols[base_name])
                logger.info(f"Selected: '{non_percentage_cols[base_name]}' (fallback, no % column found)")

        logger.info(f"Final identified root cause columns: {root_cause_cols}")
        return root_cause_cols

    def prepare_time_series_data(self, df: pd.DataFrame, root_cause_cols: List[str]) -> pd.DataFrame:
        """
        Prepare data for time series visualization

        Args:
            df: Input dataframe
            root_cause_cols: List of root cause column names

        Returns:
            Prepared dataframe with date and percentage values
        """
        try:
            # Find date column
            date_col = None
            for col in df.columns:
                if 'date' in str(col).lower() or 'week' in str(col).lower():
                    date_col = col
                    break

            if date_col is None:
                # Use index as date
                df_plot = df[root_cause_cols].copy()
                df_plot['Date'] = df.index
            else:
                df_plot = df[[date_col] + root_cause_cols].copy()
                df_plot = df_plot.rename(columns={date_col: 'Date'})

            # Convert Date column to datetime and sort
            logger.info(f"Before date conversion: {len(df_plot)} rows")
            df_plot['Date'] = pd.to_datetime(df_plot['Date'], errors='coerce')
            logger.info(f"After date conversion: {df_plot['Date'].notna().sum()} valid dates, {df_plot['Date'].isna().sum()} invalid")
            df_plot = df_plot.sort_values('Date')
            df_plot = df_plot.dropna(subset=['Date'])
            logger.info(f"After dropna(Date): {len(df_plot)} rows")

            if len(df_plot) == 0:
                logger.error("All rows dropped after date processing!")
                return pd.DataFrame()

            # Convert percentage strings to floats
            for col in root_cause_cols:
                col_name = str(col).strip()

                # Check if this is a "%" column (already calculated as percentage)
                is_pct_column = col_name.endswith(' %') or col_name.endswith('%')

                if df_plot[col].dtype == 'object':
                    # Handle string percentages like "5.00%"
                    df_plot[col] = df_plot[col].astype(str).str.replace('%', '').str.strip()
                    df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce')
                    # If it was a string with %, it's likely already a percentage that needs division
                    if not is_pct_column:
                        df_plot[col] = df_plot[col] / 100
                elif df_plot[col].dtype in ['float64', 'int64']:
                    # If column name ends with " %" or "%", values are already in decimal format
                    # (e.g., 0.0030 = 0.30%, 0.0230 = 2.30%)
                    if is_pct_column:
                        # Values are already correct: 0.0030 = 0.30%
                        # No conversion needed!
                        logger.info(f"Column '{col}' is percentage column, keeping values as-is (decimal format)")
                        pass
                    else:
                        # Non-% columns: check if values look like raw numbers needing conversion
                        sample_values = df_plot[col].dropna()
                        if len(sample_values) > 0:
                            # If more than 50% of non-zero values are > 1, assume it's percentage format
                            non_zero_values = sample_values[sample_values != 0]
                            if len(non_zero_values) > 0:
                                pct_above_one = (non_zero_values > 1).sum() / len(non_zero_values)
                                if pct_above_one > 0.5:
                                    # Values are in percentage format (e.g., 50 for 50%)
                                    df_plot[col] = df_plot[col] / 100
                                # Otherwise, values are already in decimal format (e.g., 0.50 for 50%)

            # Remove rows with all NaN values in root cause columns
            df_plot = df_plot.dropna(subset=root_cause_cols, how='all')
            logger.info(f"Final dataframe: {len(df_plot)} rows, columns: {df_plot.columns.tolist()}")

            if len(df_plot) > 0:
                logger.info(f"Date range: {df_plot['Date'].min()} to {df_plot['Date'].max()}")
                for col in root_cause_cols:
                    if col in df_plot.columns:
                        sample = df_plot[col].head(3).tolist()
                        logger.info(f"  {col} sample: {sample}")

            return df_plot

        except Exception as e:
            logger.error(f"Error preparing time series data: {e}", exc_info=True)
            return pd.DataFrame()

    def create_root_cause_chart(self, df: pd.DataFrame, root_cause: str,
                               threshold: float, important_kpis: List[str]) -> go.Figure:
        """
        Create interactive chart for a specific root cause

        Args:
            df: Prepared dataframe
            root_cause: Name of the root cause
            threshold: Threshold value for this root cause
            important_kpis: List of important KPIs

        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()

            # Check if root cause is in important KPIs (compare cleaned names)
            clean_name = clean_column_name(root_cause)
            is_important = clean_name in important_kpis

            # Add actual data line
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df[root_cause] * 100,  # Convert to percentage for display
                mode='lines+markers',
                name='Actual',
                line=dict(color='#2E86AB', width=3),
                marker=dict(size=8, symbol='circle', line=dict(width=1, color='white')),
                hovertemplate='<b>%{x|%d %b %Y}</b><br>' +
                             f'{root_cause}: %{{y:.2f}}%<br>' +
                             '<extra></extra>'
            ))

            # Add threshold line
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=[threshold * 100] * len(df),  # Convert to percentage for display
                mode='lines',
                name=f'Threshold ({threshold * 100:.1f}%)',
                line=dict(color='#F77F00', width=2.5, dash='dash'),
                hovertemplate=f'Threshold: {threshold * 100:.2f}%<br>' +
                             '<extra></extra>'
            ))

            # Highlight areas where actual exceeds threshold
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df[root_cause] * 100,
                fill='tonexty',
                mode='none',
                fillcolor='rgba(255, 0, 0, 0.1)',
                showlegend=False,
                hoverinfo='skip'
            ))

            # Update layout
            title = clean_name
            if is_important:
                title = f"⭐ {title}"

            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=18, weight='bold', color='#d32f2f' if is_important else '#1a1a1a'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title=None,
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#E8E8E8',
                    tickformat='%d %b<br>%Y',
                    tickangle=0,
                    tickfont=dict(size=11, color='#666666'),
                    tickmode='auto',
                    # Show last 12 weeks by default, but allow scrolling to see all data
                    range=[max(df['Date'].min(), df['Date'].max() - pd.Timedelta(weeks=12)), df['Date'].max()],
                    rangeslider=dict(visible=True, thickness=0.05),
                    type='date'
                ),
                yaxis=dict(
                    title=dict(text="Percentage (%)", font=dict(size=13, color='#333333')),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#E8E8E8',
                    tickformat='.2f',
                    ticksuffix='%',
                    tickfont=dict(size=11, color='#666666'),
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='#CCCCCC'
                ),
                hovermode='x unified',
                template='plotly_white',
                height=450,
                width=max(1200, len(df['Date']) * 30),  # Dynamic width: min 1200px, 30px per data point
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=60, r=40, t=80, b=60),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color='#333333'),
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='#CCCCCC',
                    borderwidth=1
                )
            )

            return fig

        except Exception as e:
            logger.error(f"Error creating chart for {root_cause}: {e}", exc_info=True)
            return go.Figure()

    def create_summary_chart(self, df: pd.DataFrame, thresholds: Dict[str, float],
                           root_cause_cols: List[str]) -> go.Figure:
        """
        Create summary chart showing all root causes

        Args:
            df: Prepared dataframe
            thresholds: Dictionary of thresholds
            root_cause_cols: List of root cause columns

        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()

            # Color palette for different root causes
            colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51']

            # Add line for each root cause
            for idx, root_cause in enumerate(root_cause_cols):
                color = colors[idx % len(colors)]
                clean_name = clean_column_name(root_cause)
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[root_cause] * 100,
                    mode='lines+markers',
                    name=clean_name,
                    line=dict(color=color, width=2.5),
                    marker=dict(size=6, symbol='circle', line=dict(width=1, color='white')),
                    hovertemplate=f'<b>{clean_name}</b><br>' +
                                 '%{x|%d %b %Y}<br>' +
                                 'Value: %{y:.2f}%<br>' +
                                 '<extra></extra>'
                ))

            fig.update_layout(
                title=dict(
                    text="Root Causes Overview",
                    font=dict(size=20, weight='bold', color='#1a1a1a'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title=None,
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#E8E8E8',
                    tickformat='%d %b<br>%Y',
                    tickangle=0,
                    tickfont=dict(size=11, color='#666666'),
                    tickmode='auto',
                    # Show last 12 weeks by default, but allow scrolling to see all data
                    range=[max(df['Date'].min(), df['Date'].max() - pd.Timedelta(weeks=12)), df['Date'].max()],
                    rangeslider=dict(visible=True, thickness=0.05),
                    type='date'
                ),
                yaxis=dict(
                    title=dict(text="Percentage (%)", font=dict(size=13, color='#333333')),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#E8E8E8',
                    tickformat='.2f',
                    ticksuffix='%',
                    tickfont=dict(size=11, color='#666666'),
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='#CCCCCC'
                ),
                hovermode='x unified',
                template='plotly_white',
                height=550,
                width=max(1400, len(df['Date']) * 30),  # Dynamic width: min 1400px, 30px per data point
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=60, r=180, t=80, b=60),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=12, color='#333333'),
                    bgcolor='rgba(255, 255, 255, 0.9)',
                    bordercolor='#CCCCCC',
                    borderwidth=1
                )
            )

            return fig

        except Exception as e:
            logger.error(f"Error creating summary chart: {e}", exc_info=True)
            return go.Figure()

    def get_available_bus(self) -> List[str]:
        """
        Get list of available BUs (sheets excluding Static Values)

        Returns:
            List of BU names
        """
        try:
            # Exclude Static Values and other non-data sheets
            exclude_sheets = [STATIC_VALUES_SHEET, 'Sheet1', 'Sheet2', 'Sheet3']
            bus = [sheet for sheet in self.excel_file.sheet_names
                   if sheet not in exclude_sheets]
            return bus
        except Exception as e:
            logger.error(f"Error getting available BUs: {e}", exc_info=True)
            return []


def main():
    """Main function to run the Streamlit dashboard"""

    # Page configuration
    st.set_page_config(
        page_title="Stability Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar: File source selection
    with st.sidebar:
        st.header("📁 Data Source")

        # Check if local file exists
        local_file_exists = Path(EXCEL_FILE_PATH).exists() if EXCEL_FILE_PATH else False

        # Option 1: Local file (if available)
        if local_file_exists:
            use_local = st.radio(
                "Select data source:",
                options=["Use local file", "Upload file"],
                help="Local file is automatically updated if you have OneDrive sync enabled"
            )
            use_uploaded = (use_local == "Upload file")
        else:
            st.warning("⚠️ Local file not found")
            use_uploaded = True

        excel_source = None

        # Local file path
        if not use_uploaded and local_file_exists:
            excel_source = EXCEL_FILE_PATH
            st.success(f"✓ Using local file")
            file_path = Path(EXCEL_FILE_PATH)
            last_modified = pd.Timestamp.fromtimestamp(file_path.stat().st_mtime)
            st.caption(f"Last updated: {last_modified.strftime('%Y-%m-%d %H:%M')}")

        # File uploader
        elif ENABLE_FILE_UPLOAD:
            st.info("📤 Upload your Excel file below")
            uploaded_file = st.file_uploader(
                "Choose Excel file",
                type=['xlsx', 'xls'],
                help="Upload the KPIsStabilityTAS.xlsx file from SharePoint"
            )

            if uploaded_file:
                excel_source = uploaded_file
                st.success(f"✓ File uploaded: {uploaded_file.name}")
            else:
                st.warning("👆 Please upload an Excel file to continue")

                # Show SharePoint link if configured
                if SHOW_SHAREPOINT_LINK and SHAREPOINT_LINK:
                    st.markdown("---")
                    st.markdown("### 🔗 Get the file from SharePoint")
                    st.markdown(f"[Open SharePoint file]({SHAREPOINT_LINK})")
                    st.caption("Click the link above, then use the Download button in SharePoint")

        st.divider()

    # Stop if no data source available
    if excel_source is None:
        st.info("👈 Please select or upload a data file to begin")
        st.stop()

    # Initialize dashboard
    dashboard = StabilityDashboard(excel_source=excel_source)

    # Load Excel file
    with st.spinner("Loading Excel file..."):
        if not dashboard.load_excel_file():
            st.stop()

    # Load static values
    with st.spinner("Loading thresholds and KPIs..."):
        if not dashboard.load_static_values():
            st.stop()

    # Get available BUs
    available_bus = dashboard.get_available_bus()

    if not available_bus:
        st.error("❌ No Business Units (sheets) found in the Excel file")
        st.stop()

    # Continue with sidebar: BU selection
    with st.sidebar:
        st.header("⚙️ Business Unit")

        selected_bu = st.selectbox(
            "Select BU to analyze:",
            options=available_bus,
            index=0 if "Kruidvat" not in available_bus else available_bus.index("Kruidvat"),
            help="Choose the Business Unit to analyze"
        )

        st.divider()

        # Show file info
        st.caption(f"📊 {len(dashboard.excel_file.sheet_names)} sheets available")
        if dashboard.last_modified:
            st.caption(f"🕒 Data from: {dashboard.last_modified.strftime('%Y-%m-%d %H:%M')}")

        # Refresh button (only if using local file)
        if not use_uploaded:
            if st.button("🔄 Reload", use_container_width=True, help="Reload from source"):
                st.rerun()

    # Main content area - simple header
    st.title(f"{selected_bu}")

    # Load BU data
    with st.spinner(f"Loading data for {selected_bu}..."):
        bu_data = dashboard.load_bu_data(selected_bu)

    if bu_data is None or bu_data.empty:
        st.error(f"❌ No data available for {selected_bu}")
        st.stop()

    # Get thresholds and important KPIs
    thresholds = dashboard.get_bu_thresholds(selected_bu)
    important_kpis = dashboard.get_bu_important_kpis(selected_bu)

    # Display important KPIs - more subtle
    if important_kpis:
        st.caption(f"⭐ Important KPIs: {', '.join(important_kpis)}")

    # Identify root cause columns
    root_cause_cols = dashboard.identify_root_cause_columns(bu_data)

    if not root_cause_cols:
        st.warning("⚠️ No root cause columns identified in the data")
        st.stop()

    # Prepare data for visualization
    with st.spinner("Preparing visualizations..."):
        prepared_data = dashboard.prepare_time_series_data(bu_data, root_cause_cols)

    if prepared_data.empty:
        st.error("❌ Unable to prepare data for visualization")
        st.stop()

    # Display individual charts for each root cause

    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 All Charts", "📋 Data Table"])

    with tab1:
        # Display charts in a grid
        for i in range(0, len(root_cause_cols), 2):
            cols = st.columns(2)

            for j, col in enumerate(cols):
                if i + j < len(root_cause_cols):
                    root_cause = root_cause_cols[i + j]
                    threshold = thresholds.get(root_cause, 0.05)  # Default 5% if not found

                    with col:
                        chart = dashboard.create_root_cause_chart(
                            prepared_data, root_cause, threshold, important_kpis
                        )
                        st.plotly_chart(chart, key=f"chart_{root_cause}_{i}_{j}")

    with tab2:
        st.subheader("Raw Data")

        # Display data with formatting
        display_data = prepared_data.copy()

        # Format percentage columns
        for col in root_cause_cols:
            if col in display_data.columns:
                display_data[col] = display_data[col].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "")

        st.dataframe(
            display_data,
            use_container_width=True,
            height=400
        )

        # Download button
        csv = prepared_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"{selected_bu}_stability_data.csv",
            mime="text/csv"
        )

    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Stability Dashboard v1.0 | Built with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error in main: {e}", exc_info=True)
        st.info("Please check the logs for more details or contact support.")
