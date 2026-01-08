"""
Quick test script to verify SharePoint integration
"""

import logging
from pathlib import Path
from config import SHAREPOINT_FILE_URL, CACHE_FOLDER, CACHE_FILE_NAME
from sharepoint_helper import load_excel_with_fallback

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_sharepoint_download():
    """Test downloading from SharePoint"""
    print("\n" + "="*60)
    print("Testing SharePoint Download")
    print("="*60)

    print(f"\nSharePoint URL: {SHAREPOINT_FILE_URL[:80]}...")
    print(f"Cache folder: {CACHE_FOLDER}")
    print(f"Cache filename: {CACHE_FILE_NAME}")

    try:
        print("\n[1] Attempting to load from SharePoint...")
        excel_file, source = load_excel_with_fallback(
            sharepoint_url=SHAREPOINT_FILE_URL,
            local_path=None,  # Don't use local fallback for this test
            cache_folder=CACHE_FOLDER,
            cache_filename=CACHE_FILE_NAME,
            force_refresh=True,  # Force fresh download
            use_sharepoint=True
        )

        print(f"\n✓ SUCCESS!")
        print(f"  Data source: {source}")
        print(f"  Available sheets: {len(excel_file.sheet_names)}")
        print(f"  Sheet names: {', '.join(excel_file.sheet_names[:5])}...")

        # Check if cache was created
        cache_path = Path(CACHE_FOLDER) / CACHE_FILE_NAME
        if cache_path.exists():
            cache_size_mb = cache_path.stat().st_size / (1024 * 1024)
            print(f"\n✓ Cache file created: {cache_path}")
            print(f"  Size: {cache_size_mb:.2f} MB")

        print("\n" + "="*60)
        print("✓ SharePoint integration is WORKING!")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n✗ FAILED: {str(e)}")
        print("\nThis might happen if:")
        print("  1. You need to be logged into SharePoint in your browser")
        print("  2. The link doesn't have proper sharing permissions")
        print("  3. Your network blocks SharePoint access")
        print("\n" + "="*60)
        print("✗ SharePoint integration FAILED")
        print("="*60)
        return False

if __name__ == "__main__":
    test_sharepoint_download()
