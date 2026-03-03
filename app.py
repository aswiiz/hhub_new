from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import get_db
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

app = Flask(__name__)
# Get secret key from environment or generate a random one for development
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper to format MongoDB documents for JSON response
def format_entry(entry):
    return {
        'id': str(entry['_id']),
        'date': entry['date'] if isinstance(entry['date'], str) else entry['date'].strftime('%Y-%m-%d'),
        'sleep_hours': entry.get('sleep_hours'),
        'steps': entry.get('steps'),
        'exercise_mins': entry.get('exercise_mins'),
        'water_liters': entry.get('water_liters'),
        'junk_food': entry.get('junk_food'),
        'smoking': 'Yes' if entry.get('smoking') else 'No',
        'alcohol_units': entry.get('alcohol_units'),
        'weight_kg': entry.get('weight_kg'),
        'height_cm': entry.get('height_cm')
    }

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    user = db.users.find_one({'_id': ObjectId(session['user_id'])})
    return render_template('dashboard.html', user=user)

@app.route('/diary')
@login_required
def diary():
    return render_template('diary.html')

@app.route('/analyze')
@login_required
def analyze():
    return render_template('analyze.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        db = get_db()
        
        if db.users.find_one({'$or': [{'username': data.get('username')}, {'phone': data.get('phone')}, {'email': data.get('email')}]}):
            return render_template('register.html', error="Username, Email or Phone already registered.")
            
        new_user = {
            'username': data.get('username'),
            'password': generate_password_hash(data.get('password')),
            'name': data.get('name'),
            'email': data.get('email'),
            'age': int(data.get('age')),
            'gender': data.get('gender'),
            'phone': data.get('phone'),
            'family_history': data.get('family_history') == 'Yes',
            'created_at': datetime.utcnow()
        }
        db.users.insert_one(new_user)
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')
        db = get_db()
        
        user = db.users.find_one({'$or': [{'username': identifier}, {'phone': identifier}]})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
            
        return render_template('login.html', error="Invalid credentials.")
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/diary', methods=['GET'])
@login_required
def get_diary():
    db = get_db()
    user_id = ObjectId(session['user_id'])
    entries = db.daily_health_log.find({'user_id': user_id}).sort('date', -1)
    
    formatted_entries = []
    for entry in entries:
        formatted_entries.append(format_entry(entry))
        
    return jsonify(formatted_entries)

@app.route('/api/diary', methods=['POST'])
@login_required
def add_diary():
    data = request.json
    db = get_db()
    user_id = ObjectId(session['user_id'])
    
    existing_entry = db.daily_health_log.find_one({'user_id': user_id, 'height_cm': {'$exists': True}})
    height = data.get('height')
    if not height and existing_entry:
        height = existing_entry.get('height_cm')

    new_entry = {
        'user_id': user_id,
        'date': data.get('date'),
        'sleep_hours': float(data.get('sleep_hours', 0)),
        'steps': int(data.get('steps', 0)),
        'exercise_mins': int(data.get('exercise_mins', 0)),
        'water_liters': float(data.get('water_liters', 0)),
        'junk_food': int(data.get('junk_food', 0)),
        'smoking': data.get('smoking') == True,
        'alcohol_units': int(data.get('alcohol_units', 0)),
        'weight_kg': float(data.get('weight', 0)),
        'height_cm': float(height) if height else None
    }
    
    db.daily_health_log.insert_one(new_entry)
    return jsonify({"success": True}), 201

@app.route('/api/height', methods=['GET'])
@login_required
def get_height():
    db = get_db()
    user_id = ObjectId(session['user_id'])
    entry = db.daily_health_log.find_one({'user_id': user_id, 'height_cm': {'$exists': True, '$ne': None}})
    if entry:
        return jsonify({'height': entry['height_cm']})
    return jsonify({'height': None})

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/login.html', error="Invalid admin credentials.")
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()
    users = list(db.users.find())
    return render_template('admin/dashboard.html', users=users)

@app.route('/admin/user/delete/<user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    db = get_db()
    db.users.delete_one({'_id': ObjectId(user_id)})
    db.daily_health_log.delete_many({'user_id': ObjectId(user_id)})
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/user/edit/<user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    db = get_db()
    if request.method == 'POST':
        data = request.form
        db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {
            'name': data.get('name'),
            'email': data.get('email'),
            'age': int(data.get('age')),
            'gender': data.get('gender'),
            'phone': data.get('phone'),
            'family_history': data.get('family_history') == 'Yes'
        }})
        return redirect(url_for('admin_dashboard'))
    
    user = db.users.find_one({'_id': ObjectId(user_id)})
    return render_template('admin/user_edit.html', user=user)

@app.route('/admin/user/logs/<user_id>')
@admin_required
def admin_user_logs(user_id):
    db = get_db()
    user = db.users.find_one({'_id': ObjectId(user_id)})
    logs = list(db.daily_health_log.find({'user_id': ObjectId(user_id)}).sort('date', -1))
    
    # Optional: Calculate a current analysis result for the admin to see
    analysis_result = "N/A"
    if len(logs) >= 3:
        # Take last 3 entries for averaging
        recent_logs = logs[:3]
        avg_sleep = sum(l.get('sleep_hours', 0) for l in recent_logs) / len(recent_logs)
        avg_steps = sum(l.get('steps', 0) for l in recent_logs) / len(recent_logs)
        avg_exercise = sum(l.get('exercise_mins', 0) for l in recent_logs) / len(recent_logs)
        avg_junk = sum(l.get('junk_food', 0) for l in recent_logs) / len(recent_logs)
        avg_alcohol = sum(l.get('alcohol_units', 0) for l in recent_logs) / len(recent_logs)
        smoking_days = sum(1 for l in recent_logs if l.get('smoking'))
        smoking_freq = smoking_days / len(recent_logs)
        
        latest_weight = logs[0].get('weight_kg', 70)
        height = logs[0].get('height_cm')
        bmi = None
        if height:
            bmi = latest_weight / ((height/100)**2)
            
        score = 0
        if user.get('family_history'): score += 1
        if bmi and (bmi < 18.5 or bmi > 25): score += 1
        if bmi and bmi > 30: score += 1
        if avg_sleep < 7: score += 1
        if avg_steps < 5000: score += 1
        if avg_exercise < 20: score += 1
        if avg_junk >= 2: score += 1
        if smoking_freq > 0.3: score += 2
        if avg_alcohol > 2: score += 1

        if score <= 2: analysis_result = "Low Chance"
        elif score <= 5: analysis_result = "Moderate Chance"
        else: analysis_result = "High Chance"

    return render_template('admin/user_logs.html', user=user, logs=logs, analysis_result=analysis_result)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))
@login_required
def predict():
    data = request.json
    db = get_db()
    user = db.users.find_one({'_id': ObjectId(session['user_id'])})
    
    score = 0
    
    # Family History Risk
    if user.get('family_history'):
        score += 1

    bmi = data.get('bmi', 22)
    if bmi < 18.5 or bmi > 25: score += 1
    if bmi > 30: score += 1
    if data.get('avg_sleep', 8) < 7: score += 1
    if data.get('avg_steps', 8000) < 5000: score += 1
    if data.get('avg_exercise', 30) < 20: score += 1
    if data.get('avg_junk', 1) >= 2: score += 1
    if data.get('smoking_freq', 0) > 0.3: score += 2
    if data.get('avg_alcohol', 0) > 2: score += 1

    if score <= 2: result = "Low Chance"
    elif score <= 5: result = "Moderate Chance"
    else: result = "High Chance"

    return jsonify({"chance": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
