"""
SharePoint Helper - Download files from SharePoint/OneDrive
Handles downloading, caching, and fallback logic
"""

import requests
from io import BytesIO
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def download_from_sharepoint(sharepoint_url: str, cache_path: str = None, force_refresh: bool = False) -> tuple[BytesIO, str]:
    """
    Download file from SharePoint/OneDrive with caching and fallback

    Args:
        sharepoint_url: SharePoint file URL
        cache_path: Optional local cache file path
        force_refresh: If True, ignore cache and force download from SharePoint

    Returns:
        Tuple of (BytesIO object with file content, source description)
        source can be: "SharePoint", "Cache", "Local"
    """
    try:
        # If cache exists and we're not forcing refresh, use it if recent
        if cache_path and Path(cache_path).exists() and not force_refresh:
            cache_age = datetime.now().timestamp() - Path(cache_path).stat().st_mtime
            cache_age_hours = cache_age / 3600

            # Use cache if less than 24 hours old
            if cache_age_hours < 24:
                logger.info(f"Using recent cache (age: {cache_age_hours:.1f} hours)")
                with open(cache_path, 'rb') as f:
                    cache_time = datetime.fromtimestamp(Path(cache_path).stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    return BytesIO(f.read()), f"Cache (updated: {cache_time})"

        # Try to download from SharePoint
        logger.info(f"Downloading file from SharePoint...")

        # Convert SharePoint sharing link to direct download link
        # Format: https://asweu-my.sharepoint.com/:x:/g/personal/.../FILE_ID?e=CODE
        # To: https://asweu-my.sharepoint.com/personal/.../_layouts/15/download.aspx?UniqueId=FILE_ID

        download_url = sharepoint_url

        # Try to extract the unique ID from the sharing URL
        if "/:x:/" in sharepoint_url or "/:w:/" in sharepoint_url or "/:p:/" in sharepoint_url:
            try:
                # Extract parts from URL like: https://asweu-my.sharepoint.com/:x:/g/personal/c_maestroni_eu_aswatson_com/FILE_ID?e=CODE
                parts = sharepoint_url.split("/")

                # Find the unique ID (usually starts with IQD or similar)
                file_id = None
                for part in parts:
                    if part.startswith("IQD") or part.startswith("EQD") or part.startswith("AQD"):
                        # Extract just the ID before any query parameters
                        file_id = part.split("?")[0]
                        break

                if file_id:
                    # Extract the base URL and personal path
                    base_url = "/".join(parts[:3])  # https://asweu-my.sharepoint.com
                    personal_path = "/".join(parts[4:6])  # personal/c_maestroni_eu_aswatson_com

                    # Construct direct download URL
                    download_url = f"{base_url}/{personal_path}/_layouts/15/download.aspx?UniqueId={file_id}"
                    logger.info(f"Converted to direct download URL: {download_url[:80]}...")
                else:
                    # Fallback: just add download=1 parameter
                    if "download=1" not in sharepoint_url:
                        download_url = sharepoint_url + ("&download=1" if "?" in sharepoint_url else "?download=1")
            except Exception as e:
                logger.warning(f"Could not convert URL to direct download: {e}")
                # Fallback: just add download=1 parameter
                if "download=1" not in sharepoint_url:
                    download_url = sharepoint_url + ("&download=1" if "?" in sharepoint_url else "?download=1")

        # Add headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,*/*',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        # Attempt download with redirect following
        response = requests.get(download_url, headers=headers, timeout=30, allow_redirects=True)

        if response.status_code == 200:
            # Verify that we got an Excel file, not an HTML page
            content_type = response.headers.get('Content-Type', '')
            first_bytes = response.content[:100]

            # Check if it's actually an Excel file
            # Excel files start with PK (zip format) or specific Excel magic bytes
            is_excel = (
                first_bytes.startswith(b'PK') or  # ZIP format (modern Excel)
                b'spreadsheet' in content_type.lower() or
                b'excel' in content_type.lower() or
                content_type.startswith('application/vnd.openxmlformats')
            )

            # Check if it's HTML (redirect page)
            is_html = (
                first_bytes.startswith(b'<!DOCTYPE') or
                first_bytes.startswith(b'<html') or
                b'text/html' in content_type.lower()
            )

            if is_html:
                logger.error("Received HTML page instead of Excel file - authentication may be required")
                raise Exception("SharePoint returned an HTML page. You may need to be logged in via browser, or the sharing permissions may not allow programmatic access.")

            if not is_excel:
                logger.warning(f"Unexpected content type: {content_type}")
                logger.warning(f"First bytes: {first_bytes[:50]}")
                # Don't fail immediately, let pandas try to read it

            logger.info("✓ File downloaded successfully from SharePoint")
            file_content = BytesIO(response.content)

            # Save to cache if path provided and content looks valid
            if cache_path and is_excel:
                try:
                    # Create cache directory if it doesn't exist
                    Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(cache_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"✓ File cached locally at: {cache_path}")
                except Exception as e:
                    logger.warning(f"Could not save cache file: {e}")

            return file_content, "SharePoint (live)"
        else:
            raise Exception(f"HTTP {response.status_code}: Could not download file")

    except Exception as e:
        logger.error(f"✗ Error downloading from SharePoint: {e}")

        # Try to use cache if available (even if old)
        if cache_path and Path(cache_path).exists():
            logger.info(f"⚠ Using cached file as fallback from: {cache_path}")
            with open(cache_path, 'rb') as f:
                cache_time = datetime.fromtimestamp(Path(cache_path).stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                return BytesIO(f.read()), f"Cache (fallback, updated: {cache_time})"
        else:
            raise Exception(f"Could not download from SharePoint and no cache available: {e}")


def load_excel_from_sharepoint(sharepoint_url: str, cache_path: str = None, force_refresh: bool = False) -> tuple[pd.ExcelFile, str]:
    """
    Load Excel file from SharePoint with caching

    Args:
        sharepoint_url: SharePoint file URL
        cache_path: Optional local cache file path
        force_refresh: If True, force download from SharePoint

    Returns:
        Tuple of (pandas ExcelFile object, source description)
    """
    try:
        file_content, source = download_from_sharepoint(sharepoint_url, cache_path, force_refresh)
        excel_file = pd.ExcelFile(file_content, engine='openpyxl')
        logger.info(f"✓ Excel file loaded successfully from {source}. Sheets: {excel_file.sheet_names}")
        return excel_file, source
    except Exception as e:
        logger.error(f"✗ Error loading Excel from SharePoint: {e}")
        raise


def load_excel_with_fallback(sharepoint_url: str = None, local_path: str = None,
                             cache_folder: str = ".cache", cache_filename: str = "Stability.xlsx",
                             force_refresh: bool = False, use_sharepoint: bool = True) -> tuple[pd.ExcelFile, str]:
    """
    Load Excel file with full fallback logic: SharePoint -> Cache -> Local File

    Args:
        sharepoint_url: SharePoint file URL
        local_path: Local file path as final fallback
        cache_folder: Folder for cache files
        cache_filename: Name of cached file
        force_refresh: If True, force download from SharePoint
        use_sharepoint: If False, skip SharePoint and use local file only

    Returns:
        Tuple of (pandas ExcelFile object, source description)
    """
    cache_path = Path(cache_folder) / cache_filename if cache_folder else None

    # Strategy 1: Try SharePoint (if enabled)
    if use_sharepoint and sharepoint_url:
        try:
            logger.info("Attempting to load from SharePoint...")
            excel_file, source = load_excel_from_sharepoint(sharepoint_url, str(cache_path), force_refresh)
            return excel_file, source
        except Exception as e:
            logger.warning(f"SharePoint loading failed: {e}")
            # Continue to fallback options

    # Strategy 2: Try local file
    if local_path and Path(local_path).exists():
        try:
            logger.info(f"Loading from local file: {local_path}")
            excel_file = pd.ExcelFile(local_path, engine='openpyxl')
            logger.info(f"✓ Excel file loaded from local file. Sheets: {excel_file.sheet_names}")
            return excel_file, f"Local file: {Path(local_path).name}"
        except Exception as e:
            logger.error(f"✗ Error loading local file: {e}")
            raise Exception(f"All loading methods failed. Last error: {e}")

    raise Exception("No valid data source available. Please check SharePoint URL or local file path.")