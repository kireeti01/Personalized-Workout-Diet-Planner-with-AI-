# AI Model Training & Methodology

## Training Pipeline

### Data Generation
The `backend/train_model.py` generates synthetic user profiles with correlated attributes:
- **360 profiles** used for training
- Realistic distribution of fitness goals, activity levels, and budgets
- Features balanced to avoid class imbalance

### Feature Engineering
**Categorical Features** (7):
- Gender (Male, Female, Other)
- Activity Level (Sedentary, Light, Moderate, Active, Very Active)
- Budget (Low, Medium, High)
- Dietary Preference (Balanced, Vegetarian, High-Protein, Low-Calorie)
- Available Equipment (Bodyweight, Basic, Gym)
- Health Condition (None, Joint Pain, Diabetes, Hypertension)
- Fitness Goal (Weight Loss, Maintenance, Muscle Gain)

**Numeric Features** (4):
- Age (17-45)
- Height (150-190 cm)
- Weight (50-95 kg)
- BMI (calculated from height and weight)

### Preprocessing
1. **One-Hot Encoding** for categorical features
2. **Standard Scaling** for numeric features
3. **Combined via ColumnTransformer** pipeline

### Model Architecture
**Algorithm**: Logistic Regression (multiclass classification)
- Efficient for multi-class problems
- Interpretable for academic submission
- Fast training and inference

**Hyperparameters**:
- `max_iter=500` - sufficient for convergence
- `random_state=42` - reproducible results

### Training Results
- **Workout Model Accuracy**: 99% on test set
- **Meal Model Accuracy**: 100% on test set
- Test-train split: 80-20

### Model Output
Two `.pkl` files saved to `backend/artifacts/`:
- `workout_model.pkl` - classifies 5 workout categories
- `diet_model.pkl` - classifies 5 meal categories

---

## Recommendation Logic

### Step 1: BMI Calculation
Formula: $BMI = \frac{weight(kg)}{height(m)^2}$

### Step 2: Basal Metabolic Rate (BMR)
**Mifflin-St Jeor Formula** (industry standard):

For males:
$$BMR = 10 \times weight + 6.25 \times height - 5 \times age + 5$$

For females:
$$BMR = 10 \times weight + 6.25 \times height - 5 \times age - 161$$

### Step 3: Daily Energy Expenditure (DEE)
$$DEE = BMR \times activity\_factor$$

Where activity factors:
- Sedentary: 1.2
- Light: 1.375
- Moderate: 1.55
- Active: 1.725
- Very Active: 1.9

### Step 4: Goal-Specific Calorie Adjustment
- **Weight Loss**: 0.8 × DEE (~500-650 kcal deficit)
- **Maintenance**: 1.0 × DEE
- **Muscle Gain**: 1.15 × DEE (~300-500 kcal surplus)

### Step 5: Workout & Meal Categorization
Input features are normalized and passed to trained models:
- Model predicts primary category
- If models not available, rule-based defaults apply
- Health conditions override to recommend low-impact routines

---

## Category Mappings

### Workout Categories
1. **Beginner-Home**: Bodyweight routines for beginners
2. **Intermediate-Gym**: Compound lifts with gym equipment
3. **Cardio-Focus**: Endurance and high-intensity training
4. **Strength-Focus**: Progressive resistance training
5. **Low-Impact**: Gentle routines for injuries/conditions

### Meal Categories
1. **Balanced**: Standard macro distribution
2. **High-Protein**: 30%+ protein for muscle gain
3. **Low-Calorie**: Reduced portion sizes for weight loss
4. **Vegetarian**: Plant-based options
5. **Budget-Friendly**: Affordable, accessible foods

---

## Validation & Testing

### Unit Tests
- BMI calculation accuracy
- BMR calculation correctness
- Recommendation output structure

### Integration Tests
- Full recommendation flow (register → profile → get recommendation)
- API endpoint validation

### Manual Testing
1. Create test user profile
2. Compare recommendation against expected output
3. Verify calorie calculations
4. Confirm fitness goal alignment

---

## Future Improvements
1. Integrate real-time wearable data (step count, heart rate)
2. Expand dataset with user feedback and outcomes
3. Add deep learning models (neural networks) for better accuracy
4. Implement A/B testing for recommendation variants
5. Add explainability layer (LIME/SHAP) for AI reasoning
