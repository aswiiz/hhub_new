# Health Care Hub 🏥

A modern, data-driven health tracking and risk assessment web application built with Python Flask and MongoDB.

## 🚀 Features

- **AI-Powered Risk Prediction**: Uses a trained Machine Learning model (Random Forest) to predict health risks based on lifestyle patterns.
- **Enhanced Recommendations**: Dynamic, context-aware health advice based on sleep, activity, BMI, and smoking habits.
- **User Authentication**: Secure registration and login (Username/Phone) with password hashing.
- **Health Dashboard**: Personalized summary of user profile and family history.
- **Daily Health Log**: Log sleep, steps, exercise, water, junk food, smoking, alcohol, and weight.
- **Health Analysis**: Aggregated health assessments with BMI calculation and machine learning predictions.
- **Admin Portal**: Complete user management (View Logs, Edit Details, Delete Users) for administrators.
- **Responsive Design**: Premium medical aesthetic optimized for both desktop and mobile.

## 🧠 Algorithms & Logic

### 1. Machine Learning Risk Prediction
The application features a built-in Random Forest classifier trained on health behavior data:
- **Feature Set**: Age, Age Group (18/30/50/75), Average Sleep, Steps, Exercise, Water, Junk Food, Smoking (Binary), and Alcohol.
- **Data Aggregation**: Predictions are most accurate when based on the user's last 3-7 days of logged health data.
- **Fallback Logic**: If the model is unavailable, a robust rule-based scoring system ensures continuous service.

### 2. Health Assessment Algorithm (Rule-Based Fallback)
- **Aggregation**: Averages the last 7 entries for key metrics.
- **BMI Factor**: Calculates BMI from the latest weight and stored height.
- **Scoring**:
  - `+1` for BMI outside optimal range (18.5 - 25).
  - `+1` for low sleep (< 7h) or low steps (< 5000).
  - `+1` for high junk food or alcohol consumption.
  - `+2` for smoking.
  - `+1` for a positive "Family History" profile.

### 3. Height Persistence
Height is collected once and stored in the database. All subsequent logs automatically use this height for BMI calculation unless manually updated by an admin.

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Machine Learning**: Scikit-Learn (Random Forest), Joblib, NumPy
- **Database**: MongoDB (Atlas)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6)
- **Security**: Werkzeug Password Hashing, Flask Sessions
- **Deployment**: Render (Auto-build via `render.yaml`)

## 📂 Project Structure

```bash
├── app.py              # Main Flask application & routes
├── database.py         # MongoDB connection logic
├── train_model.py      # ML model training script
├── health_model.pkl    # Serialized Random Forest model
├── requirements.txt    # Python dependencies
├── render.yaml         # Deployment configuration
├── static/
│   ├── css/style.css   # Custom "Medical Theme" styling
│   └── js/main.js      # Frontend logic & API handling
└── templates/          # HTML Templates (Jinja2)
    ├── admin/          # Admin Portal pages
    └── ...             # User pages (Diary, Analyze, etc.)
```

## ⚙️ Workflow

1. **User Registration**: User creates a permanent health profile.
2. **Daily Logging**: User enters health data in the Diary section.
3. **Analysis**: Once 3 entries exist, the Analyze page provides an AI-driven risk assessment and top-5 personalized recommendations.
4. **Admin Oversight**: Administrators can manage accounts and view detailed log histories.

## 🌐 Deployment

To host this on Render:
1. Push code to GitHub.
2. Create a "Blueprint" instance on Render.
3. Set the `MONGO_URI` environment variable in the dashboard.

---
**Disclaimer**: This system provides lifestyle-based risk estimation using Machine Learning only and is not a medical diagnosis.
