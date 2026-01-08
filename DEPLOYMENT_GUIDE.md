# Deployment Guide for Streamlit Cloud

This guide will help you deploy the Stability Dashboard to Streamlit Cloud so anyone with the link can access it.

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at https://share.streamlit.io)
3. Your Excel file accessible via cloud storage or included in the repository

## Step-by-Step Deployment

### Step 1: Prepare Your Excel File

You have two options:

#### Option A: Include Excel File in Repository (Simple)
```bash
# Add Excel file to your repository
# Note: Only do this if the data is not sensitive
```

#### Option B: Use Cloud Storage (Recommended for Sensitive Data)
1. Upload your Excel file to OneDrive, Google Drive, or Dropbox
2. Get a shareable link with read permissions
3. Update `config.py` to use the cloud storage link:
   ```python
   EXCEL_FILE_PATH = "https://yourstorage.com/path/to/Stability.xlsx"
   ```

### Step 2: Create GitHub Repository

1. Go to https://github.com and create a new repository
2. Name it something like "stability-dashboard"
3. Choose "Public" (required for free Streamlit Cloud tier)

### Step 3: Push Code to GitHub

```bash
# Navigate to your project directory
cd "C:\Users\mbrancato\PyCharm\Automation\Report\stability"

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Stability Dashboard v1.0"

# Add remote repository (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/stability-dashboard.git

# Push to GitHub
git push -u origin main
```

### Step 4: Configure Streamlit Secrets (for Cloud Storage)

If using Option B above, create a secrets file:

1. Create `.streamlit` folder in your project:
   ```bash
   mkdir .streamlit
   ```

2. Create `secrets.toml` file:
   ```toml
   # .streamlit/secrets.toml
   excel_file_url = "https://your-cloud-storage-url/Stability.xlsx"
   ```

3. Update `config.py` to use secrets:
   ```python
   import streamlit as st

   # Try to get from Streamlit secrets first
   if hasattr(st, 'secrets') and 'excel_file_url' in st.secrets:
       EXCEL_FILE_PATH = st.secrets['excel_file_url']
   else:
       EXCEL_FILE_PATH = r"C:\Users\mbrancato\OneDrive - A.S. Watson Europe\Documents\Stability.xlsx"
   ```

4. DO NOT commit secrets.toml to GitHub (it's already in .gitignore)

### Step 5: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Sign in with GitHub
4. Authorize Streamlit to access your repositories
5. Fill in the deployment form:
   - **Repository**: Select your `stability-dashboard` repository
   - **Branch**: `main`
   - **Main file path**: `stability_dashboard.py`
6. Click "Advanced settings" if you need to add secrets
7. Paste your secrets in the secrets field
8. Click "Deploy"

### Step 6: Wait for Deployment

- Streamlit will install dependencies from `requirements.txt`
- This usually takes 2-5 minutes
- You'll see a build log showing progress

### Step 7: Get Your Dashboard URL

Once deployed, you'll receive a URL like:
```
https://yourusername-stability-dashboard-stabilityda-xyz123.streamlit.app
```

Share this URL with anyone who needs access!

## Updating the Dashboard

### Update Code

```bash
# Make changes to your code
# Commit changes
git add .
git commit -m "Update: description of changes"

# Push to GitHub
git push

# Streamlit Cloud will automatically redeploy
```

### Update Excel Data

#### If using Option A (Excel in repo):
```bash
# Replace Excel file
# Commit and push
git add Stability.xlsx
git commit -m "Update: weekly data refresh"
git push
```

#### If using Option B (Cloud storage):
- Simply update the Excel file in your cloud storage
- Dashboard will fetch the latest version on next refresh

## Advanced Configuration

### Custom Domain

1. Go to your app settings in Streamlit Cloud
2. Click "Settings" > "General"
3. Add your custom domain
4. Follow DNS configuration instructions

### Authentication

Streamlit Cloud apps are public by default. For authentication:

1. **Option 1**: Use Streamlit's built-in authentication (requires paid plan)
2. **Option 2**: Implement custom authentication in your app:
   ```python
   import streamlit as st

   def check_password():
       def password_entered():
           if st.session_state["password"] == st.secrets["password"]:
               st.session_state["password_correct"] = True
               del st.session_state["password"]
           else:
               st.session_state["password_correct"] = False

       if "password_correct" not in st.session_state:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           return False
       elif not st.session_state["password_correct"]:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           st.error("Password incorrect")
           return False
       else:
           return True

   if check_password():
       # Your dashboard code here
       main()
   ```

### Environment Variables

Add environment variables in Streamlit Cloud settings:
1. Go to your app settings
2. Click "Secrets"
3. Add your variables in TOML format

### Resource Limits

Free tier limits:
- 1 GB RAM
- 1 CPU core
- Apps sleep after inactivity (wake up on access)

For more resources, upgrade to Streamlit Cloud Professional.

## Troubleshooting

### App Won't Deploy

1. Check build logs for errors
2. Verify `requirements.txt` is correct
3. Ensure Python version compatibility
4. Check file paths are relative, not absolute

### Excel File Not Loading

1. Verify file URL is accessible
2. Check secrets are configured correctly
3. Ensure cloud storage link has proper permissions
4. Test URL in browser

### Performance Issues

1. Optimize data loading (use caching)
2. Reduce data size
3. Consider pagination for large datasets
4. Upgrade to paid tier for more resources

### App Keeps Restarting

1. Check for infinite loops in code
2. Verify no crashes in error logs
3. Ensure dependencies are compatible
4. Check memory usage

## Monitoring

### App Analytics

Streamlit Cloud provides:
- Viewer count
- Session duration
- Error frequency
- Resource usage

Access via your app's dashboard.

### Error Logging

View logs in real-time:
1. Go to your app
2. Click "Manage app"
3. Click "Logs"

### Health Checks

Implement health check endpoint:
```python
@st.cache_data(ttl=60)
def health_check():
    # Check if Excel file is accessible
    # Check if data can be loaded
    # Return status
    pass
```

## Best Practices

1. **Version Control**: Always use git for version control
2. **Testing**: Test locally before deploying
3. **Documentation**: Keep README updated
4. **Security**: Never commit secrets or sensitive data
5. **Performance**: Use caching for expensive operations
6. **Monitoring**: Regularly check logs and analytics
7. **Updates**: Keep dependencies up to date
8. **Backup**: Keep backup of your Excel data

## Support

- Streamlit Documentation: https://docs.streamlit.io
- Streamlit Community Forum: https://discuss.streamlit.io
- GitHub Issues: Create issues in your repository
- Streamlit Cloud Support: support@streamlit.io

## Cost Considerations

### Free Tier (Community)
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Community support
- ❌ No private apps
- ❌ Apps sleep after inactivity

### Paid Tier (Professional)
- ✅ Private apps
- ✅ More resources (3 GB RAM)
- ✅ Always-on apps
- ✅ Priority support
- ✅ Custom domains
- ✅ SSO authentication

Choose based on your needs and budget.

## Next Steps

1. Deploy your first version
2. Test thoroughly with real data
3. Share with stakeholders
4. Gather feedback
5. Iterate and improve
6. Set up automated data updates
7. Monitor usage and performance
8. Scale as needed

Good luck with your deployment!
