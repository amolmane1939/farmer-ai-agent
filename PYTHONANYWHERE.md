# Deploy to PythonAnywhere (EASIEST & WORKS!)

## Why PythonAnywhere?
- ✅ Actually works (no httpx issues)
- ✅ Free tier available
- ✅ Simple upload
- ✅ No complex config
- ✅ Python-focused hosting

## Steps (10 minutes):

### 1. Create Account
- Go to: https://www.pythonanywhere.com
- Click "Start running Python online in less than a minute!"
- Sign up (FREE account)

### 2. Upload Files
- Click "Files" tab
- Click "Upload a file"
- Upload these files:
  - app.py
  - requirements.txt
  - templates/index.html
  - static/manifest.json
  - static/service-worker.js

### 3. Install Dependencies
- Click "Consoles" tab
- Click "Bash"
- Run:
```bash
pip3 install --user -r requirements.txt
```

### 4. Create Web App
- Click "Web" tab
- Click "Add a new web app"
- Choose "Flask"
- Python version: 3.10
- Path: /home/YOUR_USERNAME/app.py

### 5. Set Environment Variable
- In "Web" tab, scroll to "Environment variables"
- Add:
  - Variable: GROQ_API_KEY
  - Value: YOUR_GROQ_API_KEY_HERE

### 6. Reload
- Click green "Reload" button
- Done! ✅

Your URL: `https://YOUR_USERNAME.pythonanywhere.com`

## Much Simpler Than Render!
No httpx issues, no build errors, just works!
