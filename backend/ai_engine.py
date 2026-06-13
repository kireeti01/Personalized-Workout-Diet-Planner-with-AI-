from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MODEL_DIR = Path(__file__).resolve().parent / "artifacts"
WORKOUT_MODEL_PATH = MODEL_DIR / "workout_model.pkl"
DIET_MODEL_PATH = MODEL_DIR / "diet_model.pkl"

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

WORKOUT_MAP = {
    "Beginner-Home": [
        "3-day full-body home routine",
        "bodyweight squats, lunges, push-ups, planks, and walking",
    ],
    "Intermediate-Gym": [
        "5-day strength split with gym equipment",
        "compound lifts, rows, chest presses, and core stability",
    ],
    "Cardio-Focus": [
        "4-day cardio plan",
        "brisk walking, cycling, HIIT intervals, and recovery stretches",
    ],
    "Strength-Focus": [
        "4-day strength training plan",
        "dumbbell presses, deadlifts, squats, and progressive overload",
    ],
    "Low-Impact": [
        "gentle low-impact routine",
        "swimming, brisk walking, stretching, and mobility work",
    ],
}

MEAL_MAP = {
    "Balanced": [
        "breakfast with oats, fruit, and milk; lunch with grains, lean protein, vegetables; dinner with salad, legumes, and moderate carbs",
    ],
    "High-Protein": [
        "breakfast with eggs or greek yogurt, lunch with chicken or paneer, dinner with lentils and beans",
    ],
    "Low-Calorie": [
        "breakfast with fruit smoothie, lunch with salad bowl, dinner with soup and steamed vegetables",
    ],
    "Vegetarian": [
        "breakfast with sprouts and fruit, lunch with dal, rice, and vegetables, dinner with vegetable curry and whole-wheat roti",
    ],
    "Budget-Friendly": [
        "breakfast with poha/upma, lunch with dal rice and seasonal vegetables, dinner with chana curry and chapati",
    ],
}


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    if height_cm <= 0:
        return 0.0
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def calculate_bmr(age: int, gender: str, weight: float, height: float) -> float:
    gender = gender.lower().strip()
    if gender == "female":
        return 10 * weight + 6.25 * height - 5 * age - 161
    return 10 * weight + 6.25 * height - 5 * age + 5


def activity_factor(activity_level: str) -> float:
    mapping = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9,
    }
    return mapping.get(activity_level, 1.375)


def adjust_calories(calories: float, goal: str) -> float:
    goal = goal.lower().strip()
    if goal == "weight loss":
        return round(calories * 0.8)
    if goal == "muscle gain":
        return round(calories * 1.15)
    return round(calories)


def build_feature_vector(profile: dict) -> dict:
    return {
        "Age": int(profile.get("age", 20)),
        "Gender": profile.get("gender", "Other"),
        "Height": float(profile.get("height", 165.0)),
        "Weight": float(profile.get("weight", 65.0)),
        "BMI": float(profile.get("bmi", 22.0)),
        "ActivityLevel": profile.get("activity_level", "Moderate"),
        "Budget": profile.get("budget", "Medium"),
        "DietaryPreference": profile.get("dietary_preference", "Balanced"),
        "AvailableEquipment": profile.get("available_equipment", "Bodyweight"),
        "HealthCondition": profile.get("health_conditions", "None"),
        "FitnessGoal": profile.get("fitness_goal", "Maintenance"),
    }


def create_transformer() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERIC_FEATURES),
        ],
        remainder="drop",
    )


def load_models() -> tuple[Pipeline, Pipeline] | tuple[None, None]:
    if WORKOUT_MODEL_PATH.exists() and DIET_MODEL_PATH.exists():
        workout_model = joblib.load(WORKOUT_MODEL_PATH)
        diet_model = joblib.load(DIET_MODEL_PATH)
        return workout_model, diet_model
    return None, None


def plan_from_category(category: str, plan_map: dict[str, list[str]]) -> str:
    if category in plan_map:
        details = plan_map[category]
        return f"{details[0]}: {details[1]}" if len(details) > 1 else details[0]
    return "A mixed workout and meal plan based on your profile."


def recommend(profile: dict) -> dict[str, Any]:
    features = build_feature_vector(profile)
    workout_model, diet_model = load_models()
    workout_category = "Beginner-Home"
    meal_category = "Balanced"

    if workout_model is not None and diet_model is not None:
        input_df = pd.DataFrame([ {k: features[k] for k in CATEGORICAL_FEATURES + NUMERIC_FEATURES} ])
        workout_category = workout_model.predict(input_df)[0]
        meal_category = diet_model.predict(input_df)[0]

    workout_plan = plan_from_category(workout_category, WORKOUT_MAP)
    meal_plan = plan_from_category(meal_category, MEAL_MAP)
    bmr = calculate_bmr(features["Age"], features["Gender"], features["Weight"], features["Height"])
    maintenance_calories = round(bmr * activity_factor(features["ActivityLevel"]))
    calorie_target = adjust_calories(maintenance_calories, features["FitnessGoal"])

    return {
        "bmi": features["BMI"],
        "maintenance_calories": maintenance_calories,
        "recommended_calories": calorie_target,
        "workout_plan": workout_plan,
        "meal_plan": meal_plan,
        "goal_explanation": f"Recommended for {features['FitnessGoal']}.",
    }
