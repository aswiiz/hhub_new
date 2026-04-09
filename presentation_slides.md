# Health Care Hub 🏥
## Modern Data-Driven Health Monitoring & Risk Assessment

---

## 1. Project Vision & Overview
*   **Concept**: A comprehensive web application designed to empower users through data-driven health insights.
*   **Mission**: Bridge the gap between raw health metrics and actionable medical intelligence.
*   **Target**: Individuals looking for proactive health management and easy-to-understand risk monitoring.
*   **Goal**: Transform daily habits into clear visual analytics and AI-powered recommendations.

---

## 2. Dynamic UI/UX & Aesthetics
*   **Premium Design**: Modern "Medical Theme" with glassmorphism and smooth micro-animations.
*   **Theme System**: Switch between **Light**, **Dark**, **Nature**, **Royal**, and **Passion** modes.
*   **Responsive**: Fully optimized for Desktop, Tablet, and Mobile screens.
*   **Zero-Flicker**: Instant theme application via early-detection scripts.

---

## 3. Key Feature Set
*   **Secure Auth**: User registration and login with SHA-256 password hashing.
*   **Digital Diary**: Log 8+ health metrics (Sleep, Steps, Exercise, Diet, Smoking, etc.).
*   **Digital Dashboard**: Real-time summary of profile and health history.
*   **AI Health Assistant**: Integrated Chatbot for instant health-related doubts.
*   **Admin Control**: Secure portal for total user and data management.

---

## 4. AI & Machine Learning Core
*   **Predictive Model**: Random Forest Classifier trained on behavior data.
*   **Feature Engineering**: Analyzes Age, Activity, Diet, and Sleep patterns.
*   **Intelligent Analysis**: Aggregates the last 3-7 days of data for stable risk assessment.
*   **Contextual Tips**: Generates top-5 personalized advice based on individual risk factors.

---

## 5. Model Training & Dataset
*   **Dataset**: 150 clinical-style health samples (`datamodeltrain.txt`) covering four major age brackets (10-75+).
*   **Training Strategy**:
    *   Pre-processing of categorical age groups into normalized numeric values (18/30/50/75).
    *   **Algorithm**: Random Forest Classifier with 100 decision trees for maximum robustness.
    *   **Validation**: 80/20 train-test split ensuring model accuracy on unseen data.
*   **Key Features**: holistic set of 9 indicators including Sleep, Step Count, Exercise, Hydration, Junk Food, Smoking, and Alcohol.
*   **Outcome**: High-precision classification into Low, Moderate, or High-risk categories.

---

## 6. The "Analyze" Algorithm (Working)
*   **Step 1**: Triggers from Dashboard across a minimum 3-day log window.
*   **Step 2**: Backend computes BMI and averages all lifestyle metrics.
*   **Step 3**: Weights applied (e.g., High-impact weight for Smoking and Alcohol).
*   **Step 4**: Scikit-Learn prediction combined with rule-based scoring.
*   **Step 5**: Classification into **Low**, **Moderate**, or **High** Risk badges.

---

## 7. AI Health Assistant (Chatbot)
*   **Engine**: SambaNova Cloud (Llama-3.1-8B-Instruct).
*   **Duty**: Answering health doubts, nutrition queries, and lifestyle advice.
*   **Logic**: System-level medical disclaimers included in every interaction.
*   **UI**: Real-time message bubbles with typing indicators and quick suggestions.

---

## 8. Technical Architecture
### Backend & Database
*   **Backend**: Python Flask (Robust & Flexible)
*   **Database**: MongoDB Atlas (Scalable NoSQL)

### AI & Machine Learning Stack
*   **Libraries**: Scikit-Learn, Joblib, NumPy, Pandas
*   **Primary AI**: SambaNova Cloud (Llama-3.1-8B-Instruct) for Chatbot

### Algorithms Used
*   **Random Forest Algorithm**: Used for medical risk prediction.
*   **Rule-Based Health Assessment**: Fallback logic for health scoring.
*   **BMI Calculation Algorithm**: Automated BMI tracking from persistent data.
*   **Data Aggregation Algorithm**: 3-7 day temporal windowing for accuracy.

### Frontend & Security
*   **Frontend**: Vanilla JS (ES6), HTML5, CSS3 Variables (Custom Themes)
*   **Security**: Werkzeug Password Hashing, Flask Session Management

---

## 9. Development & Deployment Workflow
*   **CI/CD**: Git-based workflow with automated deployment.
*   **Configuration**: Environment-driven setup via `.env` and `render.yaml`.
*   **Persistence**: Height persistence for accurate BMI tracking across entries.
*   **Admin Layer**: Direct MongoDB integration for user logs and account oversight.

---

## 10. Future Roadmap & Conclusion
*   **Wearable Integration**: Future support for syncing with Apple Health or Google Fit.
*   **Predictive Trends**: Long-term health trajectory analytics.
*   **Community Support**: Anonymous health forums and peer-to-peer motivation.
*   **Statement**: Health Care Hub is your intelligent companion for a healthier, data-informed future.
