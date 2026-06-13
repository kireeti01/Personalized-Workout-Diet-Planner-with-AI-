const API_BASE = "http://127.0.0.1:5000/api";
const registerPanel = document.getElementById("register-panel");
const loginPanel = document.getElementById("login-panel");
const profileCard = document.getElementById("profile-card");
const recommendationCard = document.getElementById("recommendation-card");
const recommendationOutput = document.getElementById("recommendation-output");
const showRegisterButton = document.getElementById("show-register");
const showLoginButton = document.getElementById("show-login");

let currentUser = null;

showRegisterButton.addEventListener("click", () => {
    registerPanel.classList.remove("hidden");
    loginPanel.classList.add("hidden");
});

showLoginButton.addEventListener("click", () => {
    registerPanel.classList.add("hidden");
    loginPanel.classList.remove("hidden");
});

async function postJson(path, body) {
    const response = await fetch(`${API_BASE}/${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    return response.json();
}

function showMessage(message) {
    recommendationOutput.textContent = message;
    recommendationOutput.classList.add('visible');
    recommendationCard.classList.remove("hidden");
}

function showLoading() {
    recommendationOutput.innerHTML = '<div class="spinner" aria-hidden="true"></div>';
    recommendationOutput.classList.remove('visible');
    recommendationCard.classList.remove('hidden');
}

function setRecommendationContent(text) {
    // convert newlines to paragraphs
    const html = text.split('\n').map(line=> `<p>${line}</p>`).join('');
    recommendationOutput.innerHTML = html;
    recommendationOutput.classList.add('visible');
}

async function handleRegister(event) {
    event.preventDefault();
    const name = document.getElementById("register-name").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;

    const result = await postJson("register", { name, email, password });
    if (result.success) {
        alert("Registration completed. Please log in.");
        showLoginButton.click();
    } else {
        alert(result.message || "Registration failed.");
    }
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    const result = await postJson("login", { email, password });
    if (result.success) {
        currentUser = result.user;
        profileCard.classList.remove("hidden");
        recommendationCard.classList.remove("hidden");
        recommendationOutput.textContent = `Welcome ${currentUser.name}. Fill your profile to see your workout and meal plan.`;
    } else {
        alert(result.message || "Login failed.");
    }
}

async function handleProfileSubmit(event) {
    event.preventDefault();
    if (!currentUser) {
        alert("Please log in before submitting your profile.");
        return;
    }

    const profile = {
        age: parseInt(document.getElementById("age").value, 10),
        gender: document.getElementById("gender").value,
        height: parseFloat(document.getElementById("height").value),
        weight: parseFloat(document.getElementById("weight").value),
        fitness_goal: document.getElementById("fitness_goal").value,
        activity_level: document.getElementById("activity_level").value,
        budget: document.getElementById("budget").value,
        dietary_preference: document.getElementById("dietary_preference").value,
        available_equipment: document.getElementById("available_equipment").value,
        health_conditions: document.getElementById("health_conditions").value,
    };

    const result = await postJson("profile", { user_id: currentUser.id, profile });
    if (result.success) {
        setRecommendationContent(formatRecommendation(result.recommendation, result.profile));
    } else {
        alert(result.message || "Unable to save profile.");
    }
}

function formatRecommendation(data, profile) {
    return `BMI: ${profile.bmi}\n` +
        `Daily Calories Target: ${data.recommended_calories}\n` +
        `Workout Plan: ${data.workout_plan}\n` +
        `Meal Plan: ${data.meal_plan}\n` +
        `${data.goal_explanation}`;
}

async function refreshRecommendation() {
    if (!currentUser) {
        alert("Please log in first.");
        return;
    }
    const profile = {
        age: parseInt(document.getElementById("age").value, 10),
        gender: document.getElementById("gender").value,
        height: parseFloat(document.getElementById("height").value),
        weight: parseFloat(document.getElementById("weight").value),
        fitness_goal: document.getElementById("fitness_goal").value,
        activity_level: document.getElementById("activity_level").value,
        budget: document.getElementById("budget").value,
        dietary_preference: document.getElementById("dietary_preference").value,
        available_equipment: document.getElementById("available_equipment").value,
        health_conditions: document.getElementById("health_conditions").value,
    };
    showLoading();
    const result = await postJson("recommendation", { user_id: currentUser.id, profile });
    if (result.success) {
        setRecommendationContent(formatRecommendation(result.recommendation, profile));
    } else {
        alert(result.message || "Unable to refresh recommendation.");
    }
}

document.getElementById("register-form").addEventListener("submit", handleRegister);
document.getElementById("login-form").addEventListener("submit", handleLogin);
document.getElementById("profile-form").addEventListener("submit", handleProfileSubmit);
document.getElementById("refresh-button").addEventListener("click", refreshRecommendation);
