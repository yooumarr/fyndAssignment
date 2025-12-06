# LLM-Powered Feedback System Assignment

## Project Overview
This repository contains two tasks demonstrating LLM applications:
1. **Task 1**: Rating prediction via prompting on Yelp reviews
2. **Task 2**: Two-dashboard AI feedback web application

##Live Deployments

### Task 2 Dashboards:
- **User Dashboard**: [Streamlit Link User](https://user-dashboard.streamlit.app)
- **Admin Dashboard**: [Streamlit Link Admin](https://admin-dashboard.streamlit.app)

*Note: Replace with your actual deployment URLs*

## Repository Structure

### Task 1: Rating Prediction
- `task1/yelp_rating_prediction.ipynb` - Complete Jupyter notebook


### Task 2: Web Application
- `task2/user_dashboard.py` - Public user interface
- `task2/admin_dashboard.py` - Admin analytics interface
- `task2/database.py` - MongoDB Atlas integration
- `task2/llm_utils.py` - Gemini API utilities
- `task2/requirements.txt` - Python dependencies

## Setup Instructions

### Local Development
```bash
# Clone repository
git clone https://github.com/yooumarr/fyndAssignment.git
cd llm-feedback-assignment
pip install -r requirements.txt

# Task 1: Run Jupyter notebook
cd task1
jupyter notebook yelp_rating_prediction.ipynb

# Task 2: Setup and run
cd task2
cp .env.example .env  # Add your API keys
streamlit run user_dashboard.py
streamlit run admin_dashboard.py