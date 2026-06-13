# Deployment Instructions

## Option 1: Deploy Backend on Render.com

### Prerequisites
- GitHub account with repository
- Render.com account (free tier available)

### Steps
1. Generate Render configuration:
   ```bash
   python deploy_render.py
   ```

2. Commit and push to GitHub:
   ```bash
   git add render.yaml
   git commit -m "Add Render deployment config"
   git push
   ```

3. Connect to Render:
   - Go to https://render.com
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select `render.yaml` as the configuration
   - Click "Deploy"

4. Get your backend URL:
   - After deployment, Render shows your service URL
   - Update `frontend/script.js` API_BASE to your Render URL

---

## Option 2: Deploy Backend on Railway.app

### Prerequisites
- GitHub account with repository
- Railway.app account (credit-based, free tier included)

### Steps
1. Create a Procfile:
   ```bash
   echo "web: python backend/app.py" > Procfile
   ```

2. Push to GitHub

3. Connect to Railway:
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and installs from requirements.txt

4. Set environment variables in Railway dashboard:
   - `FLASK_ENV=production`
   - `FLASK_DEBUG=false`

5. Get your backend URL and update frontend

---

## Option 3: Deploy Frontend on GitHub Pages

### Steps
1. Create a `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy Frontend
   on:
     push:
       branches: [main]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Deploy to GitHub Pages
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./frontend
   ```

2. Enable GitHub Pages:
   - Go to Settings → Pages
   - Set source to `gh-pages` branch
   - Your frontend is live at `https://username.github.io/repo-name`

3. Update `frontend/script.js`:
   ```javascript
   const API_BASE = "https://your-render-backend.onrender.com/api";
   ```

---

## Local Deployment Testing

Before deploying to production, test locally:

```bash
# Terminal 1: Start Backend
.venv\Scripts\python.exe backend\app.py

# Terminal 2: Serve Frontend (using Python)
.venv\Scripts\python.exe -m http.server 8000 --directory frontend
```

Visit `http://localhost:8000` to test the complete system.

---

## Environment Variables for Production

Create a `.env` file in production environments:
```
FLASK_ENV=production
FLASK_DEBUG=false
DATABASE_URL=sqlite:///app_data.db
```

---

## Post-Deployment Checklist

- [ ] Backend API responds to health check
- [ ] Frontend loads without CORS errors
- [ ] Registration and login work end-to-end
- [ ] Profile submission generates recommendations
- [ ] Models load and produce accurate outputs
- [ ] Database persists user data
