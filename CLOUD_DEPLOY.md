# Cloud Deployment Guide (Render.com)

## Step 1: Prepare GitHub Repository

1. Create GitHub account: https://github.com
2. Create new repository: "farmer-ai-agent"
3. Upload all files EXCEPT `.env` file

**Using Git:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/farmer-ai-agent.git
git push -u origin main
```

**Or upload manually** on GitHub website

---

## Step 2: Deploy on Render.com

1. Go to: https://render.com
2. Sign up (free account)
3. Click "New +" → "Web Service"
4. Connect GitHub account
5. Select your repository: "farmer-ai-agent"

**Settings:**
- Name: `farmer-ai-agent`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Instance Type: `Free`

6. Click "Advanced" → "Add Environment Variable"
   - Key: `GROQ_API_KEY`
   - Value: `YOUR_GROQ_API_KEY_HERE`

7. Click "Create Web Service"

---

## Step 3: Wait for Deployment

- Takes 2-5 minutes
- You'll get a URL like: `https://farmer-ai-agent.onrender.com`
- Share this URL with anyone!

---

## Your App Will Be:
✅ Always online (24/7)
✅ Accessible from anywhere
✅ Free (with some limitations)
✅ Auto-updates when you push to GitHub

---

## Free Tier Limitations:
- App sleeps after 15 min of inactivity
- First request after sleep takes 30-60 seconds
- 750 hours/month free

---

## Alternative: Railway.app

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select repository
5. Add environment variable: `GROQ_API_KEY`
6. Deploy!

**Railway gives $5 free credit/month**

---

## Need Help?
- Render docs: https://render.com/docs
- Railway docs: https://docs.railway.app
