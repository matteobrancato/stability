"""
Helper script to get the correct SharePoint download link
This script helps you find the right download URL for your SharePoint file
"""

print("""
================================================================================
SharePoint Download Link Helper
================================================================================

The sharing link you have doesn't work for programmatic download because
SharePoint requires authentication for corporate files.

SOLUTION OPTIONS:

Option 1: MANUAL DOWNLOAD (RECOMMENDED - SEMPRE FUNZIONA)
---------------------------------------------------------
1. Open the SharePoint link in your browser
2. Click "Download" button
3. Save the file to a known location (e.g., Downloads folder or project folder)
4. Update config.py to point to that location
5. The app will use the local file and show when it was last updated

This is the EASIEST and MOST RELIABLE solution.


Option 2: USE LOCAL SYNCED FOLDER (IF YOU HAVE ONEDRIVE SYNC)
--------------------------------------------------------------
If your OneDrive is synced to your computer:
1. Find the file in: C:\\Users\\[username]\\OneDrive - A.S. Watson Europe\\...
2. Use that path in config.py
3. The file will auto-update when OneDrive syncs

This is what you're currently using and it works!


Option 3: EMBED LINK (EXPERIMENTAL - MAY NOT WORK)
--------------------------------------------------
Try this embed link format:
https://asweu-my.sharepoint.com/personal/c_maestroni_eu_aswatson_com/_layouts/15/Doc.aspx?sourcedoc={7D5888E2-6971-49DF-A57B-8B891FB4F859}&action=embedview

This MIGHT work but likely still requires browser authentication.


RECOMMENDATION FOR YOUR USE CASE:
==================================

Since you want OTHER PEOPLE to use this dashboard WITHOUT needing the local file:

1. Keep SharePoint DISABLED in config.py (USE_SHAREPOINT = False)

2. Tell users to either:
   a) Sync their OneDrive folder (automatic updates)
   b) Download the file manually once and put it in a specific folder

3. Add a "Data Source" display in the dashboard showing:
   - Where the file is loaded from
   - When it was last modified
   - A button to open SharePoint link in browser to download updated version

4. Optionally: Add a file uploader in Streamlit where users can drag/drop
   the Excel file directly into the dashboard (no need to save locally)


Would you like me to implement option 4 (file uploader)?
This would be the BEST solution for sharing with others!

================================================================================
""")
