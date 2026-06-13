# Installation & Setup Guide

## Prerequisites
- Python 3.11+
- pip (Python package manager)
- Git
- A code editor (VS Code recommended)

## Step 1: Clone or Download Project

### Option A: Clone from GitHub
```bash
git clone https://github.com/your-username/fitness-planner.git
cd fitness-planner
```

### Option B: Manual Download
1. Download project ZIP
2. Extract to your desired location
3. Open terminal in project root

## Step 2: Create and Activate Virtual Environment

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**What gets installed**:
- Flask 3.0.0 - web framework
- pandas 2.2.3 - data manipulation
- scikit-learn 1.4.2 - machine learning
- joblib 1.3.2 - model serialization
- pytest 8.4.2 - testing framework

## Step 4: Initialize Database & Train Models
```bash
python backend/train_model.py
```

**Output**:
- Creates `backend/artifacts/` directory
- Saves `workout_model.pkl` and `diet_model.pkl`
- Generates `dataset/training_data.csv`
- Prints accuracy metrics

Expected output:
```
Saved workout model to .../backend/artifacts/workout_model.pkl
Saved diet model to .../backend/artifacts/diet_model.pkl
Workout model accuracy: 0.99
Diet model accuracy: 1.00
```

## Step 5: Start the Backend Server
```bash
python backend/app.py
```

**Expected output**:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Press Ctrl+C to quit
```

**Keep this terminal running** while testing the application.

## Step 6: Start the Frontend (New Terminal)

### Option A: Python HTTP Server
```bash
python -m http.server 8000 --directory frontend
```

### Option B: Open directly
Open `frontend/index.html` in your browser directly.

## Step 7: Access the Application

### Via Browser:
- **Frontend**: http://localhost:8000 (if using HTTP server)
- **Backend API**: http://localhost:5000/api

### First-time user flow:
1. Click "Register" tab
2. Fill in name, email, password
3. Click "Create Account"
4. Click "Login" tab
5. Enter credentials
6. Fill fitness profile form
7. Click "Save Profile & Get Recommendation"
8. View personalized results

## Troubleshooting

### Issue: "No module named 'flask'"
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution**: Use a different port
```bash
python backend/app.py --port 5001
```

### Issue: "ModuleNotFoundError: No module named 'backend'"
**Solution**: Run commands from project root directory
```bash
cd /path/to/fitness-planner
python backend/app.py
```

### Issue: Models not loading
**Solution**: Retrain models
```bash
python backend/train_model.py
```

---

## Testing the Application

### Run All Tests
```bash
pytest tests -q
```

### Run Specific Test File
```bash
pytest tests/test_app.py -v
```

### Run with Coverage Report
```bash
pytest tests --cov=backend
```

---

## Development Workflow

### Making Code Changes
1. Edit `.py` files in `backend/`
2. Flask auto-reloads on save (debug mode on)
3. Frontend changes reload on browser refresh

### Adding New Features
1. Modify `backend/` for API logic
2. Update `frontend/` for UI
3. Add tests to `tests/`
4. Run tests to verify

### Deactivating Virtual Environment
```bash
deactivate
```

