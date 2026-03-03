import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Create synthetic data for training
def generate_samples(n=1000):
    np.random.seed(42)
    
    # Features: age, bmi, sleep, steps, exercise, junk, smoking, alcohol, family_history
    # range: age(18-80), bmi(15-45), sleep(4-10), steps(1000-15000), exercise(0-120), junk(0-5), smoking(0-1), alcohol(0-10), family_history(0-1)
    
    data = []
    for _ in range(n):
        age = np.random.randint(18, 80)
        bmi = np.random.uniform(15, 45)
        sleep = np.random.uniform(4, 10)
        steps = np.random.randint(1000, 15000)
        exercise = np.random.randint(0, 120)
        junk = np.random.randint(0, 5)
        smoking = np.random.choice([0, 1], p=[0.7, 0.3])
        alcohol = np.random.uniform(0, 10)
        family_history = np.random.choice([0, 1], p=[0.8, 0.2])
        
        # Simple rule-based risk calculation for label generation
        risk_score = 0
        if family_history: risk_score += 1.5
        if bmi < 18.5 or bmi > 25: risk_score += 1
        if bmi > 30: risk_score += 1.5
        if sleep < 7: risk_score += 1
        if steps < 5000: risk_score += 1
        if exercise < 20: risk_score += 1
        if junk >= 2: risk_score += 1
        if smoking: risk_score += 2
        if alcohol > 2: risk_score += 1
        if age > 50: risk_score += 0.5
        
        if risk_score <= 2.5:
            label = 0 # Low
        elif risk_score <= 5.5:
            label = 1 # Moderate
        else:
            label = 2 # High
            
        data.append([age, bmi, sleep, steps, exercise, junk, smoking, alcohol, family_history, label])
        
    return pd.DataFrame(data, columns=['age', 'bmi', 'avg_sleep', 'avg_steps', 'avg_exercise', 'avg_junk', 'smoking_freq', 'avg_alcohol', 'family_history', 'label'])

def load_user_data(filepath='datamodeltrain.txt'):
    # Load dataset
    df = pd.read_csv(filepath)
    
    # Mapping for Age_Group strings to numeric values as requested:
    # 10–18 → 18, 19–30 → 30, 31–50 → 50, 51–75 → 75
    age_group_map = {
        '10-18': 18,
        '19-30': 30,
        '31-50': 50,
        '51-75': 75
    }
    
    # Normalize the string keys just in case
    df['Age_Group_Numeric'] = df['Age_Group'].map(age_group_map)
    
    # Features: Age, Age_Group_Numeric, Sleep_Hours, Steps_Walked, Exercise_Minutes, 
    # Water_Intake_Liters, Junk_Food_Intake, Smoking, Alcohol_Units
    processed_data = pd.DataFrame({
        'age': df['Age'],
        'age_group': df['Age_Group_Numeric'],
        'sleep': df['Sleep_Hours'],
        'steps': df['Steps_Walked'],
        'exercise': df['Exercise_Minutes'],
        'water': df['Water_Intake_Liters'],
        'junk': df['Junk_Food_Intake'],
        'smoking': df['Smoking'],
        'alcohol': df['Alcohol_Units']
    })
    
    # Target: Disease_Risk (0 or 1)
    processed_data['label'] = df['Disease_Risk']
    
    return processed_data

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train():
    # Load and process the user-provided data
    if os.path.exists('datamodeltrain.txt'):
        print("Loading data from datamodeltrain.txt...")
        df = load_user_data()
    else:
        print("datamodeltrain.txt not found.")
        return
        
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Split data to evaluate accuracy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Calculate accuracy
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    # Retrain on full data for production
    model.fit(X, y)
    
    joblib.dump(model, 'health_model.pkl')
    print(f"Model trained on {len(df)} samples.")
    print(f"Model Accuracy: {acc*100:.2f}%")

if __name__ == "__main__":
    train()
