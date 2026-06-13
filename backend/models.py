import sqlite3
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_connection


def register_user(email: str, name: str, password: str) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            (email.lower().strip(), name.strip(), password_hash),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def authenticate_user(email: str, password: str) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, email, name, password_hash FROM users WHERE email = ?", (email.lower().strip(),))
    row = cursor.fetchone()
    connection.close()
    if row and check_password_hash(row["password_hash"], password):
        return {"id": row["id"], "email": row["email"], "name": row["name"]}
    return None


def save_profile(user_id: int, profile_data: dict) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id FROM profiles WHERE user_id = ?",
        (user_id,),
    )
    existing = cursor.fetchone()
    values = (
        user_id,
        profile_data.get("age"),
        profile_data.get("gender"),
        profile_data.get("height"),
        profile_data.get("weight"),
        profile_data.get("bmi"),
        profile_data.get("fitness_goal"),
        profile_data.get("activity_level"),
        profile_data.get("budget"),
        profile_data.get("dietary_preference"),
        profile_data.get("available_equipment"),
        profile_data.get("health_conditions"),
    )
    if existing:
        cursor.execute(
            "UPDATE profiles SET age=?, gender=?, height=?, weight=?, bmi=?, fitness_goal=?, activity_level=?, budget=?, dietary_preference=?, available_equipment=?, health_conditions=?, created_at=CURRENT_TIMESTAMP WHERE user_id=?",
            values[1:] + (user_id,),
        )
    else:
        cursor.execute(
            "INSERT INTO profiles (user_id, age, gender, height, weight, bmi, fitness_goal, activity_level, budget, dietary_preference, available_equipment, health_conditions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            values,
        )
    connection.commit()
    connection.close()
    return True


def load_profile(user_id: int) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    connection.close()
    if not row:
        return None
    return dict(row)


def save_recommendation(user_id: int, workout_plan: str, meal_plan: str) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO recommendations (user_id, workout_plan, meal_plan) VALUES (?, ?, ?)",
        (user_id, workout_plan, meal_plan),
    )
    connection.commit()
    connection.close()


def get_latest_recommendation(user_id: int) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM recommendations WHERE user_id = ? ORDER BY recommended_at DESC LIMIT 1",
        (user_id,),
    )
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None
