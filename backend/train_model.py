from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "artifacts"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
DATASET_PATH = BASE_DIR.parent / "dataset" / "training_data.csv"

CATEGORICAL_FEATURES = [
    "Gender",
    "ActivityLevel",
    "Budget",
    "DietaryPreference",
    "AvailableEquipment",
    "HealthCondition",
    "FitnessGoal",
]
NUMERIC_FEATURES = ["Age", "Height", "Weight", "BMI"]

WORKOUT_LABELS = [
    "Beginner-Home",
    "Intermediate-Gym",
    "Cardio-Focus",
    "Strength-Focus",
    "Low-Impact",
]
MEAL_LABELS = [
    "Balanced",
    "High-Protein",
    "Low-Calorie",
    "Vegetarian",
    "Budget-Friendly",
]


def synthetic_profile(index: int) -> dict:
    genders = ["Male", "Female", "Other"]
    goals = ["Weight Loss", "Maintenance", "Muscle Gain"]
    activities = ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
    budgets = ["Low", "Medium", "High"]
    diets = ["Balanced", "Vegetarian", "High-Protein", "Low-Calorie"]
    equipment = ["Bodyweight", "Basic", "Gym"]
    health = ["None", "Joint Pain", "Diabetes", "Hypertension"]

    age = np.random.randint(17, 45)
    gender = np.random.choice(genders)
    height = np.random.randint(150, 190)
    weight = np.random.randint(50, 95)
    bmi = round(weight / ((height / 100) ** 2), 1)
    goal = np.random.choice(goals, p=[0.4, 0.3, 0.3])
    activity = np.random.choice(activities, p=[0.15, 0.2, 0.35, 0.2, 0.1])
    budget = np.random.choice(budgets, p=[0.25, 0.55, 0.2])
    diet = np.random.choice(diets, p=[0.5, 0.2, 0.2, 0.1])
    equip = np.random.choice(equipment, p=[0.45, 0.35, 0.2])
    health_condition = np.random.choice(health, p=[0.7, 0.1, 0.1, 0.1])

    if goal == "Weight Loss":
        meal = "Low-Calorie" if budget != "High" else "Balanced"
        workout = "Cardio-Focus" if activity in ["Moderate", "Active"] else "Beginner-Home"
    elif goal == "Muscle Gain":
        meal = "High-Protein"
        workout = "Strength-Focus" if equip != "Bodyweight" else "Intermediate-Gym"
    else:
        meal = "Balanced"
        workout = "Intermediate-Gym" if equip == "Gym" else "Beginner-Home"
    if health_condition != "None":
        workout = "Low-Impact"
        meal = "Balanced"

    return {
        "Age": age,
        "Gender": gender,
        "Height": height,
        "Weight": weight,
        "BMI": bmi,
        "FitnessGoal": goal,
        "ActivityLevel": activity,
        "Budget": budget,
        "DietaryPreference": diet,
        "AvailableEquipment": equip,
        "HealthCondition": health_condition,
        "WorkoutCategory": workout,
        "MealCategory": meal,
    }


def create_dataset(rows: int = 300) -> pd.DataFrame:
    return pd.DataFrame([synthetic_profile(i) for i in range(rows)])


def build_pipeline() -> Pipeline:
    transformer = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERIC_FEATURES),
        ],
        remainder="drop",
    )
    return Pipeline(
        steps=[
            ("transform", transformer),
            ("model", LogisticRegression(max_iter=500, random_state=42)),
        ]
    )


def train_and_save():
    df = create_dataset(360)
    df.to_csv(DATASET_PATH, index=False)

    X = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y_workout = df["WorkoutCategory"]
    y_meal = df["MealCategory"]

    workout_pipeline = build_pipeline()
    diet_pipeline = build_pipeline()

    X_train, X_test, y_train, y_test = train_test_split(X, y_workout, test_size=0.2, random_state=42)
    workout_pipeline.fit(X_train, y_train)
    workout_accuracy = workout_pipeline.score(X_test, y_test)

    X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y_meal, test_size=0.2, random_state=42)
    diet_pipeline.fit(X_train2, y_train2)
    diet_accuracy = diet_pipeline.score(X_test2, y_test2)

    joblib.dump(workout_pipeline, MODEL_DIR / "workout_model.pkl")
    joblib.dump(diet_pipeline, MODEL_DIR / "diet_model.pkl")

    print(f"Saved workout model to {MODEL_DIR / 'workout_model.pkl'}")
    print(f"Saved diet model to {MODEL_DIR / 'diet_model.pkl'}")
    print(f"Workout model accuracy: {workout_accuracy:.2f}")
    print(f"Diet model accuracy: {diet_accuracy:.2f}")


if __name__ == "__main__":
    train_and_save()
