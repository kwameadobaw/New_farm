from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production

DATA_FILE = 'data.json'
ADMIN_PASSWORD = 'admin123'  # Change this in production

# Ensure data file exists
def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        data = {
            "farmerName": request.form.get('farmerName', ''),
            "farmID": request.form.get('farmID', ''),
            "phoneNumber": request.form.get('phoneNumber', ''),
            "location": request.form.get('location', ''),
            "gps": request.form.get('gps', ''),
            "size": request.form.get('size', ''),
            "farmType": request.form.getlist('farmType'),
            "visitDate": request.form.get('visitDate', ''),
            "visitType": request.form.get('visitType', ''),
            "officerName": request.form.get('officerName', ''),
            "timeSpent": request.form.get('timeSpent', ''),
            "mainCrops": request.form.get('mainCrops', ''),
            "cropStage": request.form.get('cropStage', ''),
            "cropIssues": request.form.getlist('cropIssues'),
            "livestockType": request.form.get('livestockType', ''),
            "animalCount": request.form.get('animalCount', ''),
            "livestockIssues": request.form.getlist('livestockIssues'),
            "advice": request.form.get('advice', ''),
            "followUp": 'followUp' in request.form,
            "followUpDate": request.form.get('followUpDate', ''),
            "training": 'training' in request.form,
            "referral": 'referral' in request.form,
            "followUpNotes": request.form.get('followUpNotes', ''),
            "timestamp": datetime.now().isoformat(),
            "id": datetime.now().strftime("%Y%m%d%H%M%S")  # Simple ID generation
        }
        
        # Read existing data
        ensure_data_file()
        with open(DATA_FILE, 'r') as f:
            existing = json.load(f)
        
        existing.append(data)
        
        # Save back to file
        with open(DATA_FILE, 'w') as f:
            json.dump(existing, f, indent=4)
        
        return jsonify({"success": True, "message": "Farm visit data saved successfully!"})
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error saving data: {str(e)}"}), 500

@app.route('/admin')
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    password = request.form.get('password', '')
    if password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid password!', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    return render_template('admin_dashboard.html', entries=data)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "message": "Not authorized"}), 401
    
    try:
        ensure_data_file()
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        
        # Find and remove the entry
        data = [entry for entry in data if entry.get('id') != entry_id]
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({"success": True, "message": "Entry deleted successfully!"})
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error deleting entry: {str(e)}"}), 500

if __name__ == '__main__':
    ensure_data_file()
    app.run(debug=True) 