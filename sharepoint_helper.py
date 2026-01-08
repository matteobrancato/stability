"""
SharePoint Helper - Download files from SharePoint/OneDrive
"""

import requests
from io import BytesIO
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def download_from_sharepoint(sharepoint_url: str, cache_path: str = None) -> BytesIO:
    """
    Download file from SharePoint/OneDrive

    Args:
        sharepoint_url: SharePoint file URL
        cache_path: Optional local cache file path

    Returns:
        BytesIO object with file content
    """
    try:
        # Try to download from SharePoint
        logger.info(f"Downloading file from SharePoint...")

        # Convert web view URL to download URL
        if "?web=1" in sharepoint_url:
            # Remove ?web=1 parameter
            download_url = sharepoint_url.replace("?web=1", "?download=1")
        else:
            download_url = sharepoint_url

        # Add headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Attempt download
        response = requests.get(download_url, headers=headers, timeout=30)

        if response.status_code == 200:
            logger.info("File downloaded successfully from SharePoint")
            file_content = BytesIO(response.content)

            # Save to cache if path provided
            if cache_path:
                try:
                    with open(cache_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"File cached locally at: {cache_path}")
                except Exception as e:
                    logger.warning(f"Could not save cache file: {e}")

            return file_content
        else:
            raise Exception(f"HTTP {response.status_code}: Could not download file")

    except Exception as e:
        logger.error(f"Error downloading from SharePoint: {e}")

        # Try to use cache if available
        if cache_path and Path(cache_path).exists():
            logger.info(f"Using cached file from: {cache_path}")
            with open(cache_path, 'rb') as f:
                return BytesIO(f.read())
        else:
            raise Exception(f"Could not download from SharePoint and no cache available: {e}")


def load_excel_from_sharepoint(sharepoint_url: str, cache_path: str = None) -> pd.ExcelFile:
    """
    Load Excel file from SharePoint

    Args:
        sharepoint_url: SharePoint file URL
        cache_path: Optional local cache file path

    Returns:
        pandas ExcelFile object
    """
    try:
        file_content = download_from_sharepoint(sharepoint_url, cache_path)
        excel_file = pd.ExcelFile(file_content, engine='openpyxl')
        logger.info(f"Excel file loaded successfully. Sheets: {excel_file.sheet_names}")
        return excel_file
    except Exception as e:
        logger.error(f"Error loading Excel from SharePoint: {e}")
        raise