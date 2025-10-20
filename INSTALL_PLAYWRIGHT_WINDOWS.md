# 🪟 Install Playwright on Windows

## Error Encountered

```
ModuleNotFoundError: No module named 'playwright'
```

This happens because Playwright is not installed on your Windows environment.

---

## ✅ Solution: Install Playwright

### Option 1: Quick Install (Recommended)

Open Command Prompt or PowerShell **as Administrator** in your project directory:

```bash
# Navigate to backend folder
cd backend

# Install playwright
pip install playwright

# Install Chromium browser
python -m playwright install chromium
```

**Expected output:**
```
Successfully installed playwright-1.55.0 ...
Downloading Chromium 140.0... (173 MB)
Chromium downloaded successfully
```

---

### Option 2: Install from requirements.txt

```bash
# Navigate to backend folder
cd backend

# Reinstall all requirements (includes playwright)
pip install -r requirements.txt

# Install Chromium browser
python -m playwright install chromium
```

---

### Option 3: If You Can't Install Playwright

The application will automatically fall back to matplotlib-based maps (without real basemap) if Playwright is not available.

**You'll see this message:**
```
⚠️ Playwright not installed - will use matplotlib for maps
Using matplotlib for map visualization...
```

The PDF will still generate successfully, but the map will be a simple scatter plot instead of a real Indonesia map.

---

## 🧪 Test Installation

After installing, test if it works:

```bash
cd backend
python
```

Then in Python:
```python
>>> from playwright.sync_api import sync_playwright
>>> print("✅ Playwright installed successfully!")
>>> exit()
```

If no error, installation was successful!

---

## 🔧 Troubleshooting

### Issue 1: "pip: command not found"

**Solution:** Use `python -m pip` instead:
```bash
python -m pip install playwright
python -m playwright install chromium
```

### Issue 2: Permission Denied

**Solution:** Run as Administrator or use `--user` flag:
```bash
pip install --user playwright
python -m playwright install chromium
```

### Issue 3: Chromium Download Fails

**Solution:** Install manually:
```bash
# First install playwright package
pip install playwright

# Then install browsers with verbose output
python -m playwright install chromium --with-deps
```

### Issue 4: Still Getting "Module not found"

**Solution:** Check you're using the correct Python environment:
```bash
# Check which Python
python --version

# Check where pip installs to
pip show playwright

# If different Python, activate your virtual environment first:
# For venv:
.\venv\Scripts\activate

# Then install again
pip install playwright
python -m playwright install chromium
```

---

## 📦 What Gets Installed

1. **Playwright package** (~46 MB)
   - Python library for browser automation
   
2. **Chromium browser** (~173 MB)
   - Headless browser for screenshots
   - Installed in: `%USERPROFILE%\AppData\Local\ms-playwright\`

**Total disk space needed:** ~220 MB

---

## 🎯 Benefits of Installing Playwright

### With Playwright:
- ✅ **Real Indonesia map** (OpenStreetMap basemap)
- ✅ **Professional quality**
- ✅ **Geographical context** (rivers, roads, cities)
- ✅ **Beautiful visualization**

### Without Playwright (Fallback):
- ⚠️ Simple scatter plot
- ⚠️ No map background
- ⚠️ Less professional looking
- ✅ Still works, just not as nice

---

## 🚀 After Installation

1. **Restart your backend server:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Try downloading PDF again**

3. **Check console output:**
   ```
   ✅ Creating map with 494 points across 3 clusters
      Coordinates mapped from city names: 494
      Coordinates from member data: 0
      Attempting Folium map with Playwright screenshot...
      ✅ Folium map with OpenStreetMap basemap created successfully!
   ```

---

## 📝 Quick Reference

```bash
# Full installation (recommended)
pip install playwright
python -m playwright install chromium

# Verify installation
python -c "from playwright.sync_api import sync_playwright; print('✅ OK')"

# Restart server
python manage.py runserver
```

---

## ❓ Still Having Issues?

If you continue to have problems installing Playwright:

1. **Check Python version:**
   ```bash
   python --version
   ```
   Playwright requires Python 3.8+

2. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Try in virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install playwright
   python -m playwright install chromium
   ```

4. **Use the fallback:**
   - The app will still work with matplotlib fallback
   - Maps won't have real basemap but will show cluster points
   - All other features work normally

---

**Status:** Once installed, Playwright will work automatically for all future PDF generations! 🎉
