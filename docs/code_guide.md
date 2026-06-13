# Code Structure & File Guide

## Backend Architecture

### `backend/app.py`
**Purpose**: Flask REST API server.

**Key Functions**:
- `register()` - User registration endpoint
- `login()` - User authentication endpoint
- `profile()` - Save profile and get recommendation
- `get_profile()` - Retrieve user profile and latest recommendation
- `get_recommendation()` - Generate new recommendation
- `index()` - Health check endpoint

**Dependencies**: Flask, Flask-CORS, models, ai_engine, database

---

### `backend/database.py`
**Purpose**: SQLite connection and schema initialization.

**Key Functions**:
- `get_connection()` - Returns an SQLite connection with row factory
- `init_db()` - Creates all tables if they don't exist

**Tables Created**:
- `users` - User accounts
- `profiles` - Fitness profiles
- `recommendations` - Personalized recommendations

---

### `backend/models.py`
**Purpose**: Database operations and authentication logic.

**Key Functions**:
- `register_user(email, name, password)` - Creates new user with hashed password
- `authenticate_user(email, password)` - Validates credentials
- `save_profile(user_id, profile_data)` - Saves or updates user fitness profile
- `load_profile(user_id)` - Retrieves user profile
- `save_recommendation(user_id, workout_plan, meal_plan)` - Stores recommendation
- `get_latest_recommendation(user_id)` - Retrieves the most recent recommendation

**Security**: Password hashing with Werkzeug

---

### `backend/ai_engine.py`
**Purpose**: AI recommendation engine and health calculations.

**Key Functions**:
- `calculate_bmi(height_cm, weight_kg)` - Computes BMI
- `calculate_bmr(age, gender, weight, height)` - Computes Basal Metabolic Rate (Mifflin-St Jeor formula)
- `activity_factor(activity_level)` - Returns activity multiplier
- `adjust_calories(calories, goal)` - Adjusts calorie target based on fitness goal
- `build_feature_vector(profile)` - Normalizes profile for ML model
- `load_models()` - Loads pre-trained models from disk
- `recommend(profile)` - Generates personalized workout and meal recommendations

**Recommendation Logic**:
- Uses trained ML models (if available) to classify workout and meal categories
- Falls back to rule-based defaults if models are not loaded
- Calculates BMI and daily calorie needs
- Applies goal-specific adjustments

---

### `backend/train_model.py`
**Purpose**: Synthetic data generation and model training.

**Key Functions**:
- `synthetic_profile(index)` - Generates one synthetic user profile
- `create_dataset(rows)` - Creates a DataFrame of synthetic profiles
- `build_pipeline()` - Creates scikit-learn ML pipeline with preprocessing and logistic regression
- `train_and_save()` - Trains both workout and diet models, saves to disk

**Output**:
- `backend/artifacts/workout_model.pkl` - Trained model for workout categories
- `backend/artifacts/diet_model.pkl` - Trained model for meal categories
- `dataset/training_data.csv` - Synthetic dataset used for training

**Model Accuracy**: ~99% for workout, 100% for meal (on synthetic data)

---

## Frontend Architecture

### `frontend/index.html`
**Purpose**: User interface markup and form structure.

**Sections**:
- Auth card - registration and login tabs
- Profile card - fitness profile form
- Recommendation card - displays personalized output

**Form Fields**:
- Age, gender, height, weight
- Fitness goal, activity level, budget
- Dietary preference, equipment, health conditions

---

### `frontend/styles.css`
**Purpose**: Responsive styling with modern design system.

**Design Features**:
- Gradient background
- Card-based layout
- Mobile-first responsive grid
- Smooth hover transitions
- Clean typography

---

### `frontend/script.js`
**Purpose**: Client-side logic and API integration.

**Key Functions**:
- `handleRegister()` - Processes user registration
- `handleLogin()` - Authenticates user and displays profile form
- `handleProfileSubmit()` - Saves profile and fetches recommendation
- `refreshRecommendation()` - Generates new recommendation
- `formatRecommendation()` - Formats output for display
- `postJson()` - Helper for API calls

**API Integration**: Communicates with Flask backend at `http://127.0.0.1:5000/api`

---

## Tests

### `tests/test_app.py`
**Purpose**: Integration tests for API endpoints.

**Tests**:
- `test_register_login_profile_endpoints()` - Full flow: register → login → save profile → get recommendation

---

### `tests/test_ai_engine.py`
**Purpose**: Unit tests for AI calculations.

**Tests**:
- `test_calculate_bmi()` - Verifies BMI formula
- `test_calculate_bmr()` - Verifies BMR calculation
- `test_recommendation_keys()` - Ensures recommendation has all required keys

---

## Configuration Files

### `requirements.txt`
Lists all Python dependencies and versions.

### `.gitignore`
Excludes virtual environment, cache, database, and model files from version control.

### `README.md`
Overview, installation, and project structure.

