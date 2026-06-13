# GitHub Repository Setup Guide

## Creating a GitHub Repository

### Step 1: Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: Personalized Workout & Diet Planner with AI"
```

### Step 2: Create Repository on GitHub
1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `fitness-planner` (or your preferred name)
   - **Description**: "AI-powered personalized workout and diet planner for students"
   - **Visibility**: Public (for portfolio) or Private
   - **Initialize with**: No (we already have files)
3. Click "Create repository"

### Step 3: Push to GitHub
```bash
git remote add origin https://github.com/your-username/fitness-planner.git
git branch -M main
git push -u origin main
```

---

## Repository Structure for GitHub

Your repository should have:
```
fitness-planner/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── ai_engine.py
│   ├── train_model.py
│   ├── artifacts/
│   │   ├── workout_model.pkl
│   │   └── diet_model.pkl
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── dataset/
│   ├── README.md
│   └── training_data.csv
├── docs/
│   ├── architecture.md
│   ├── database_schema.md
│   ├── api_reference.md
│   ├── code_guide.md
│   ├── ai_methodology.md
│   ├── setup_guide.md
│   ├── deployment.md
│   ├── deployment_detailed.md
│   ├── documentation.md
│   └── presentation.md
├── tests/
│   ├── test_app.py
│   ├── test_ai_engine.py
│   └── __init__.py
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── deploy.yml
├── .gitignore
├── .env.example
├── Procfile
├── requirements.txt
├── deploy_render.py
├── README.md
```

---

## GitHub Repository Configuration

### 1. Add Topics (for discoverability)
- `fitness`
- `ai`
- `machine-learning`
- `flask`
- `recommendation-system`

### 2. Enable GitHub Pages
1. Go to **Settings** → **Pages**
2. **Build and deployment**:
   - Source: `Deploy from a branch`
   - Branch: `gh-pages` (or `main` if using `/docs` folder)
3. Your frontend will be available at: `https://username.github.io/fitness-planner/`

### 3. Enable Branch Protection
1. Go to **Settings** → **Branches**
2. Add rule for `main` branch:
   - Require pull request reviews before merging
   - Require status checks to pass (CI/CD)
   - Require branches to be up to date

### 4. Configure Actions Secrets (for Render/Railway)
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `RENDER_API_KEY` - from Render dashboard
   - `RAILWAY_API_TOKEN` - from Railway dashboard

---

## Release Management

### Creating a Release
```bash
# Create a tag
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0
```

### On GitHub:
1. Go to **Releases**
2. Click "Create a new release"
3. Select your tag (v1.0.0)
4. Add release notes
5. Click "Publish release"

---

## Collaboration Workflow

### Branch Strategy
1. **main** - production-ready code
2. **develop** - development branch
3. **feature/feature-name** - individual features

### Pull Request Process
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and commit: `git commit -m "Add new feature"`
3. Push: `git push origin feature/new-feature`
4. Create Pull Request on GitHub
5. CI tests run automatically
6. After review, merge to `main`

---

## Adding Collaborators

1. Go to **Settings** → **Collaborators**
2. Click "Add people"
3. Search and invite team members
4. Choose permission level (Maintainer, Write, Read)

---

## Project Documentation Badge

Add this to your README.md:
```markdown
[![CI Tests](https://github.com/your-username/fitness-planner/workflows/CI%20Tests/badge.svg)](https://github.com/your-username/fitness-planner/actions)

[![Deploy Frontend](https://github.com/your-username/fitness-planner/workflows/Deploy%20Frontend/badge.svg)](https://github.com/your-username/fitness-planner/actions)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

