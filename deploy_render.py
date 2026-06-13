#!/usr/bin/env python3
"""
Render Deployment Configuration Script

Run: python deploy_render.py
This creates a render.yaml configuration file for deployment on Render.com
"""

import sys
from pathlib import Path

RENDER_CONFIG = """
services:
  - type: web
    name: fitness-planner-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt && python backend/train_model.py
    startCommand: python backend/app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_DEBUG
        value: "false"
    region: oregon
    numInstances: 1
    healthCheckPath: /

  - type: static_site
    name: fitness-planner-frontend
    staticPublishPath: ./frontend
    buildCommand: echo "Frontend ready for deployment"
    routes:
      - path: /
        destination: /index.html
"""

def create_render_config():
    config_path = Path("render.yaml")
    config_path.write_text(RENDER_CONFIG)
    print(f"Created {config_path}")
    print("\nNext steps:")
    print("1. Commit render.yaml to your repository")
    print("2. Push to GitHub")
    print("3. Connect your repository to Render.com")
    print("4. Render will auto-deploy on every push")

if __name__ == "__main__":
    create_render_config()
