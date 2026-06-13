# Viva Questions & Answers

## Technical Questions

### 1. What is the main problem your system solves?
**Answer**: Most fitness apps provide generic workout and diet recommendations that don't account for individual constraints like budget, equipment availability, cultural food preferences, and health conditions. Our system personalizes recommendations based on 11 user profile fields, making fitness guidance practical and affordable for students.

---

### 2. Why did you choose SQLite for the database instead of MySQL or PostgreSQL?
**Answer**: SQLite was the optimal choice because:
- No server setup required (lightweight, perfect for prototypes)
- Self-contained database (single .db file)
- Ideal for academic projects and small-to-medium user bases
- Sufficient for this project's scope
- Can be easily migrated to PostgreSQL or MySQL if scaling to millions of users

---

### 3. Explain the architecture of your system.
**Answer**: The system has three tiers:
1. **Frontend** (HTML/CSS/JavaScript) - User interface for registration, profile input, and viewing recommendations
2. **Backend** (Flask API) - Handles business logic, authentication, database queries, and recommendation generation
3. **Database** (SQLite) - Stores users, profiles, and recommendation history

The AI engine runs on the backend, using trained ML models to classify workout and meal categories based on user profiles.

---

### 4. How does the AI recommendation engine work?
**Answer**: The recommendation process:
1. Accepts user profile data (age, gender, height, weight, fitness goal, activity level, budget, dietary preference, equipment, health conditions)
2. Calculates BMI using the formula: $BMI = \frac{weight(kg)}{height(m)^2}$
3. Computes daily energy expenditure using BMR (Basal Metabolic Rate) and activity factors
4. Adjusts calorie target based on fitness goal (weight loss -20%, maintenance 0%, muscle gain +15%)
5. Uses pre-trained ML models to classify workout and meal categories
6. Returns personalized recommendations with calorie targets and specific plans

---

### 5. What ML algorithms did you use, and why?
**Answer**: I used **Logistic Regression** for multiclass classification:
- Advantages:
  - Interpretable (important for academic projects)
  - Fast training and inference
  - Works well with engineered features
  - No hyperparameter tuning needed for good results
  - ~99% accuracy on this dataset
- Why not deep learning? Neural networks would be overkill for this problem size and would reduce interpretability

---

### 6. How did you handle the dataset? Is it real data?
**Answer**: The training data is **synthetically generated** (360 profiles), not real user data:
- **Why synthetic?** Real fitness data is hard to obtain, and generating it ensures no privacy issues
- **How realistic?** The synthetic profiles follow realistic distributions matching real-world fitness patterns
- **Methodology**: 
  - Random sampling of age (17-45), height (150-190cm), weight (50-95kg)
  - Correlated features (e.g., high fitness goals tend with gym access)
  - 80-20 train-test split
  - Cross-validation to prevent overfitting

---

### 7. How do you ensure user security and data privacy?
**Answer**: Security measures implemented:
1. **Password hashing**: Werkzeug's `generate_password_hash` + bcrypt
2. **Input validation**: All API endpoints validate and sanitize inputs
3. **CORS** enabled: Prevents unauthorized cross-origin requests
4. **Local database**: No external API calls expose user data
5. **Future improvements**: SSL/TLS for HTTPS, environment variables for secrets, rate limiting

---

### 8. What are the key features of your frontend?
**Answer**:
1. **Responsive design** - Works on mobile, tablet, desktop using CSS Grid and media queries
2. **User authentication** - Separate registration and login tabs with form validation
3. **Profile form** - 11 input fields with dropdowns for consistency
4. **Real-time display** - Results appear immediately after submission
5. **Refresh button** - Users can regenerate recommendations without re-entering profile

---

### 9. Explain your API endpoints.
**Answer**: Five main endpoints:
1. `POST /api/register` - Creates new user with hashed password
2. `POST /api/login` - Authenticates user and returns user ID
3. `POST /api/profile` - Saves profile and generates recommendation
4. `GET /api/profile/<user_id>` - Retrieves user's profile and last recommendation
5. `POST /api/recommendation` - Generates new recommendation for profile

All return JSON responses with success flags and error messages.

---

### 10. How did you test your system?
**Answer**: Multi-level testing:
1. **Unit tests** - Test individual functions (BMI calculation, BMR calculation)
2. **Integration tests** - Test full API flows (register → login → profile → recommendation)
3. **Manual testing** - Tested in browser across different devices
4. **Model validation** - Checked ML accuracy on test set
5. **Framework**: Used pytest with 4/4 tests passing

---

## Design & Methodology Questions

### 11. How did you calculate calorie requirements?
**Answer**: Using the **Mifflin-St Jeor formula** (industry standard):

For males: $BMR = 10W + 6.25H - 5A + 5$
For females: $BMR = 10W + 6.25H - 5A - 161$

Then multiply by activity factor:
- Sedentary: 1.2
- Light: 1.375
- Moderate: 1.55
- Active: 1.725
- Very Active: 1.9

Finally, adjust for goal: -20% (loss), 0% (maintenance), +15% (gain)

---

### 12. How do you handle health conditions?
**Answer**: Health conditions override other recommendations:
- If user has Joint Pain, Diabetes, or Hypertension → recommend "Low-Impact" workout
- Low-impact includes swimming, walking, gentle stretching
- Meal plan becomes "Balanced" to avoid complications

This ensures safety is prioritized.

---

### 13. What was the most challenging part of the project?
**Answer**: **Generating realistic synthetic data**:
- Challenge: ML models need diverse, balanced training data
- Solution: Created synthetic profiles with realistic distributions and correlations
- Implementation: Probabilities for each feature reflect real-world patterns
- Validation: Achieved 99-100% model accuracy

---

### 14. How would you deploy this to production?
**Answer**: Three-tier deployment strategy:
1. **Backend**: Deploy to Render.com or Railway.app
   - Push code to GitHub
   - Platform auto-deploys from repo
   - Environment variables for production settings
2. **Database**: SQLite stored on backend server
3. **Frontend**: Deploy to GitHub Pages
   - Update API_BASE URL to production backend
   - Static files served globally

Cost: Mostly free with hobby tiers.

---

### 15. What would you improve if you had more time?
**Answer**: Top improvements:
1. **Mobile app** - React Native for iOS/Android
2. **Real-time data** - Integration with fitness trackers (Fitbit, Apple Watch)
3. **Advanced ML** - Deep learning models for better accuracy
4. **Chatbot** - AI assistant for personalized advice
5. **Social features** - Community challenges, group accountability
6. **Marketplace** - Connect users with trainers and nutritionists

---

## Code & Implementation Questions

### 16. Walk me through your Flask app structure.
**Answer**: 
- `app.py` initializes Flask, sets up routes, and calls helper functions
- Each route calls appropriate functions from `models.py` and `ai_engine.py`
- `database.py` handles SQLite connections
- Pattern: request validation → database query → AI logic → response

This modular approach keeps code organized and testable.

---

### 17. How do you validate user input?
**Answer**: 
1. **Type checking**: Ensure age is int, weight is float
2. **Range validation**: Age 15-80, height 120-230cm, weight 30-150kg
3. **Required fields**: All profile fields must be provided
4. **Frontend validation**: HTML5 required and type attributes
5. **Backend validation**: Python type hints and explicit checks

---

### 18. Explain your feature engineering process.
**Answer**: 
- **Categorical features** (7): Gender, Activity Level, Budget, Dietary Preference, Equipment, Health Condition, Fitness Goal
  - One-hot encoded into binary columns
- **Numeric features** (4): Age, Height, Weight, BMI
  - Standardized using StandardScaler (mean 0, std 1)
- **Pipeline**: Combined via ColumnTransformer with proper fit/transform separation

This ensures models train on normalized, properly-typed data.

---

### 19. How do you handle model loading and caching?
**Answer**: 
- Models saved as `.pkl` files using joblib
- On API startup: `load_models()` tries to load from disk
- If models exist: use trained models for predictions
- If models missing: fall back to rule-based recommendations
- This avoids retraining on every API call

---

### 20. What logging and error handling do you implement?
**Answer**: 
- All API routes have try-except blocks
- Database errors caught and reported
- Model loading failures fall back gracefully
- Success flags in JSON responses
- HTTP status codes (200, 201, 400, 401, 409, 404)
- Client receives meaningful error messages

---

## Project Management Questions

### 21. How long did this project take?
**Answer**: [Tailor to your actual timeline]
- Planning and design: [X weeks]
- Core backend development: [X weeks]
- Frontend development: [X weeks]
- ML training and validation: [X weeks]
- Testing and debugging: [X weeks]
- Documentation and deployment: [X weeks]
- **Total**: [X weeks]

---

### 22. What tools and technologies did you learn?
**Answer**:
- **Backend**: Flask, REST API design, database relationships
- **ML**: scikit-learn, feature engineering, model training
- **Frontend**: Responsive design with CSS Grid
- **DevOps**: Git, GitHub, CI/CD with GitHub Actions
- **Deployment**: Render, Railway, GitHub Pages
- **Database**: SQL, SQLite, relationships

---

### 23. How would you measure success of this project?
**Answer**: Key metrics:
1. **Technical**: All features working, 100% test pass rate
2. **Performance**: API responds < 200ms, model inference < 100ms
3. **User experience**: Intuitive interface, clear recommendations
4. **Scalability**: System handles 1000s of concurrent users
5. **Adoption**: If deployed, track user registration and engagement

---

### 24. What would you do differently if starting over?
**Answer**:
1. Start with API-first design before frontend
2. Use more sophisticated ML models from the beginning
3. Implement logging from day 1
4. Create more comprehensive unit tests earlier
5. Document as I code, not at the end
6. Use a task management system (Jira, Trello)

---

### 25. How would you handle scalability if this became popular?
**Answer**:
1. **Database**: Migrate from SQLite to PostgreSQL
2. **Caching**: Implement Redis for frequent queries
3. **ML**: Distributed model training with MLflow
4. **API**: Load balancing with multiple backend instances
5. **Frontend**: CDN for static files
6. **Monitoring**: Application performance monitoring (APM) tools

---

## Conceptual Questions

### 26. What is BMI, and why is it important?
**Answer**: 
- **BMI** (Body Mass Index) = weight(kg) / height(m)²
- **Importance**: Quick indicator of whether weight is healthy for height
- **Limitations**: Doesn't distinguish muscle from fat, varies by ethnicity
- **Usage**: Starting point for fitness recommendations; correlates with health risks

---

### 27. Why use activity factors in calorie calculation?
**Answer**: 
- Different activity levels burn different calories
- Sedentary person needs fewer calories than active person
- Activity factor ranges from 1.2-1.9
- Ensures recommendations match real energy expenditure
- More accurate personalization

---

### 28. What is Basal Metabolic Rate (BMR)?
**Answer**: 
- **Definition**: Calories your body burns at rest (sleeping, breathing, cell function)
- **Formula**: Mifflin-St Jeor is most accurate for general population
- **Why it matters**: Different for everyone based on age, weight, gender
- **Usage**: Multiply by activity factor to get total daily needs

---

### 29. How does your system handle conflicting preferences?
**Answer**: 
- If user selects High-Protein diet but is Vegetarian: recommend plant-based proteins (lentils, tofu, beans)
- If Low-Budget but needs Muscle Gain: recommend affordable high-protein foods (eggs, rice, chickpeas)
- Health conditions override other preferences for safety
- ML model learns these correlations from training data

---

### 30. Why is personalization important in fitness?
**Answer**: 
- One-size-fits-all doesn't work: people have different goals, budgets, constraints
- Personalized plans improve adherence (people follow plans they trust)
- Accounts for cultural food preferences and available equipment
- Safer (considers health conditions and fitness level)
- More effective (matches recommendations to individual reality)

---

## Wrap-Up

### Final Thoughts for the Viva

1. **Be confident** - You built a complete system
2. **Use examples** - Refer to specific code sections when explaining
3. **Show passion** - Discuss improvements you'd make
4. **Be honest** - If you don't know, say so and offer to research
5. **Connect to problem** - Always link back to solving student fitness needs

### Common Follow-up Questions

- "Can you show me the code for [component]?"
  - Be ready to explain key files quickly
  
- "What would happen if [scenario]?"
  - Think about edge cases (invalid input, network failure, etc.)
  
- "Why didn't you use [alternative technology]?"
  - Have thoughtful reasons for your choices

