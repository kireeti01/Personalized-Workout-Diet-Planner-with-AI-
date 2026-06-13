# Deployment Guide

## Local Deployment
1. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Train the AI models:
   ```powershell
   python backend\train_model.py
   ```
4. Start the backend:
   ```powershell
   python backend\app.py
   ```
5. Open `frontend/index.html` in a browser.

## Hosting Backend on Render/Railway
1. Create a new Python service.
2. Add `requirements.txt`.
3. Set the start command to `python backend/app.py`.
4. Ensure `PORT` environment variable is supported by the platform.
5. Update the frontend `API_BASE` variable with the production backend URL.

## Hosting Frontend on GitHub Pages
1. Add the `frontend/` folder to the repo.
2. In repository settings, configure GitHub Pages to serve the main branch from `/frontend`.
3. Update `frontend/script.js` if the backend URL changes.

## Notes
- For production, replace local endpoints and add HTTPS.
- Save the trained models by running `backend/train_model.py` before deployment.
