from backend.ai_engine import calculate_bmi, calculate_bmr, recommend


def test_calculate_bmi():
    assert calculate_bmi(180, 75) == 23.1


def test_calculate_bmr():
    bmr_male = calculate_bmr(25, "Male", 70, 175)
    bmr_female = calculate_bmr(25, "Female", 70, 175)
    assert bmr_male > bmr_female
    assert round(bmr_male) == 1674


def test_recommendation_keys():
    profile = {
        "age": 30,
        "gender": "Female",
        "height": 165,
        "weight": 62,
        "fitness_goal": "Weight Loss",
        "activity_level": "Light",
        "budget": "Low",
        "dietary_preference": "Balanced",
        "available_equipment": "Bodyweight",
        "health_conditions": "None",
    }
    rec = recommend(profile)
    assert "workout_plan" in rec
    assert "meal_plan" in rec
    assert "recommended_calories" in rec
