# API Reference

## Base URL
- Local: `http://localhost:5000/api`
- Production: `https://your-backend-url.com/api`

## Endpoints

### 1. User Registration
**POST** `/api/register`

Request:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

Response (Success - 201):
```json
{
  "success": true,
  "message": "Registration completed."
}
```

Response (Conflict - 409):
```json
{
  "success": false,
  "message": "Email is already registered."
}
```

---

### 2. User Login
**POST** `/api/login`

Request:
```json
{
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

Response (Success - 200):
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe"
  }
}
```

Response (Unauthorized - 401):
```json
{
  "success": false,
  "message": "Invalid credentials."
}
```

---

### 3. Save Fitness Profile & Get Recommendation
**POST** `/api/profile`

Request:
```json
{
  "user_id": 1,
  "profile": {
    "age": 25,
    "gender": "Male",
    "height": 175,
    "weight": 75,
    "fitness_goal": "Weight Loss",
    "activity_level": "Moderate",
    "budget": "Medium",
    "dietary_preference": "Balanced",
    "available_equipment": "Gym",
    "health_conditions": "None"
  }
}
```

Response (Success - 200):
```json
{
  "success": true,
  "profile": {
    "id": 1,
    "user_id": 1,
    "age": 25,
    "gender": "Male",
    "height": 175,
    "weight": 75,
    "bmi": 24.5,
    "fitness_goal": "Weight Loss",
    "activity_level": "Moderate",
    "budget": "Medium",
    "dietary_preference": "Balanced",
    "available_equipment": "Gym",
    "health_conditions": "None"
  },
  "recommendation": {
    "bmi": 24.5,
    "maintenance_calories": 2750,
    "recommended_calories": 2200,
    "workout_plan": "4-day cardio plan: brisk walking, cycling, HIIT intervals, and recovery stretches",
    "meal_plan": "breakfast with fruit smoothie, lunch with salad bowl, dinner with soup and steamed vegetables",
    "goal_explanation": "Recommended for Weight Loss."
  }
}
```

---

### 4. Get User Profile & Latest Recommendation
**GET** `/api/profile/<user_id>`

Response (Success - 200):
```json
{
  "success": true,
  "profile": {
    "id": 1,
    "user_id": 1,
    "age": 25,
    "gender": "Male",
    "height": 175,
    "weight": 75,
    "bmi": 24.5,
    "fitness_goal": "Weight Loss",
    "activity_level": "Moderate",
    "budget": "Medium",
    "dietary_preference": "Balanced",
    "available_equipment": "Gym",
    "health_conditions": "None"
  },
  "recommendation": {
    "id": 1,
    "user_id": 1,
    "workout_plan": "4-day cardio plan",
    "meal_plan": "breakfast with fruit smoothie",
    "recommended_at": "2024-01-15 10:30:00"
  }
}
```

---

### 5. Get New Recommendation
**POST** `/api/recommendation`

Request:
```json
{
  "user_id": 1,
  "profile": {
    "age": 26,
    "gender": "Male",
    "height": 175,
    "weight": 72,
    "fitness_goal": "Muscle Gain",
    "activity_level": "Active",
    "budget": "High",
    "dietary_preference": "High-Protein",
    "available_equipment": "Gym",
    "health_conditions": "None"
  }
}
```

Response (Success - 200):
```json
{
  "success": true,
  "recommendation": {
    "bmi": 23.5,
    "maintenance_calories": 3050,
    "recommended_calories": 3510,
    "workout_plan": "4-day strength training plan: dumbbell presses, deadlifts, squats, and progressive overload",
    "meal_plan": "breakfast with eggs or greek yogurt, lunch with chicken or paneer, dinner with lentils and beans",
    "goal_explanation": "Recommended for Muscle Gain."
  }
}
```

---

## Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `409` - Conflict (e.g., email already registered)
