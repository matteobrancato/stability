"""
Test script to validate the Stability Dashboard setup
Run this before deploying to catch any issues early
"""

import sys
from pathlib import Path

# Set UTF-8 encoding for console output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl',
        'plotly': 'plotly'
    }

    all_passed = True
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package_name} installed")
        except ImportError:
            print(f"  ✗ {package_name} NOT installed")
            all_passed = False

    return all_passed

def test_config():
    """Test if config file exists and is valid"""
    print("\nTesting configuration...")
    try:
        import config
        print(f"  ✓ config.py found")

        # Check required settings
        required_settings = ['EXCEL_FILE_PATH', 'STATIC_VALUES_SHEET']
        for setting in required_settings:
            if hasattr(config, setting):
                print(f"  ✓ {setting} defined")
            else:
                print(f"  ✗ {setting} NOT defined")
                return False

        return True
    except ImportError:
        print(f"  ⚠ config.py not found (will use defaults)")
        return True

def test_excel_file():
    """Test if Excel file exists and is accessible"""
    print("\nTesting Excel file...")
    try:
        import config
        excel_path = config.EXCEL_FILE_PATH
    except:
        excel_path = r"C:\Users\mbrancato\OneDrive - A.S. Watson Europe\Documents\Stability.xlsx"

    if Path(excel_path).exists():
        print(f"  ✓ Excel file found at: {excel_path}")

        # Try to read it
        try:
            import pandas as pd
            excel_file = pd.ExcelFile(excel_path)
            print(f"  ✓ Excel file can be read")
            print(f"  ℹ Available sheets: {', '.join(excel_file.sheet_names)}")

            # Check for Static Values sheet
            if "Static Values" in excel_file.sheet_names:
                print(f"  ✓ 'Static Values' sheet found")
            else:
                print(f"  ⚠ 'Static Values' sheet NOT found")

            return True
        except Exception as e:
            print(f"  ✗ Error reading Excel file: {e}")
            return False
    else:
        print(f"  ✗ Excel file NOT found at: {excel_path}")
        print(f"  ℹ Please update the path in config.py")
        return False

def test_dashboard_script():
    """Test if main dashboard script exists and has no syntax errors"""
    print("\nTesting dashboard script...")
    dashboard_path = Path("stability_dashboard.py")

    if dashboard_path.exists():
        print(f"  ✓ stability_dashboard.py found")

        # Try to compile it
        try:
            with open(dashboard_path, encoding='utf-8') as f:
                compile(f.read(), dashboard_path, 'exec')
            print(f"  ✓ No syntax errors detected")
            return True
        except SyntaxError as e:
            print(f"  ✗ Syntax error: {e}")
            return False
        except UnicodeDecodeError as e:
            print(f"  ⚠ Encoding issue (file will still work): {e}")
            return True
    else:
        print(f"  ✗ stability_dashboard.py NOT found")
        return False

def test_requirements():
    """Test if requirements.txt exists"""
    print("\nTesting requirements file...")
    req_path = Path("requirements.txt")

    if req_path.exists():
        print(f"  ✓ requirements.txt found")
        with open(req_path) as f:
            packages = f.read().strip().split('\n')
            print(f"  ℹ Required packages: {', '.join(packages)}")
        return True
    else:
        print(f"  ⚠ requirements.txt NOT found")
        print(f"  ℹ This is needed for deployment")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("=" * 60)
    print("Stability Dashboard - Setup Validation")
    print("=" * 60)

    tests = [
        ("Package Dependencies", test_imports),
        ("Configuration", test_config),
        ("Excel File", test_excel_file),
        ("Dashboard Script", test_dashboard_script),
        ("Requirements File", test_requirements)
    ]

    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Run the dashboard: streamlit run stability_dashboard.py")
        print("  2. Test with your data")
        print("  3. Deploy to Streamlit Cloud (see DEPLOYMENT_GUIDE.md)")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above before proceeding.")

    print("=" * 60)

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
