import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.ai_engine import calculate_bmi, recommend
from backend.database import init_db
from backend.models import (
    authenticate_user,
    get_latest_recommendation,
    load_profile,
    register_user,
    save_profile,
    save_recommendation,
)

app = Flask(__name__)
CORS(app)

init_db()


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")

    if not email or not name or not password:
        return jsonify({"success": False, "message": "Name, email, and password are required."}), 400

    success = register_user(email, name, password)
    if not success:
        return jsonify({"success": False, "message": "Email is already registered."}), 409

    return jsonify({"success": True, "message": "Registration completed."}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    return jsonify({"success": True, "user": user}), 200


@app.route("/api/profile", methods=["POST"])
def profile():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    profile_data = data.get("profile", {})

    if not user_id or not profile_data:
        return jsonify({"success": False, "message": "User ID and profile data are required."}), 400

    height = float(profile_data.get("height", 0))
    weight = float(profile_data.get("weight", 0))
    profile_data["bmi"] = calculate_bmi(height, weight)
    save_profile(user_id, profile_data)

    recommendation = recommend(profile_data)
    save_recommendation(user_id, recommendation["workout_plan"], recommendation["meal_plan"])

    return jsonify({"success": True, "profile": profile_data, "recommendation": recommendation}), 200


@app.route("/api/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    profile = load_profile(user_id)
    if not profile:
        return jsonify({"success": False, "message": "Profile not found."}), 404
    recommendation = get_latest_recommendation(user_id)
    return jsonify({"success": True, "profile": profile, "recommendation": recommendation}), 200


@app.route("/api/recommendation", methods=["POST"])
def get_recommendation():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    profile_data = data.get("profile", {})

    if not user_id or not profile_data:
        return jsonify({"success": False, "message": "User ID and profile are required."}), 400

    profile_data["bmi"] = calculate_bmi(float(profile_data.get("height", 0)), float(profile_data.get("weight", 0)))
    recommendation = recommend(profile_data)
    save_recommendation(user_id, recommendation["workout_plan"], recommendation["meal_plan"])
    return jsonify({"success": True, "recommendation": recommendation}), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Personalized Workout & Diet Planner API is running."})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
