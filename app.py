from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import json
import os
from datetime import datetime
from fpdf import FPDF
from flask import make_response

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

@app.route('/admin/download/<entry_id>')
def download_entry_pdf(entry_id):
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "message": "Not authorized"}), 401

    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    entry = next((e for e in data if e.get('id') == entry_id), None)
    if not entry:
        return jsonify({"success": False, "message": "Entry not found"}), 404

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Farm Visit Report', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)

    def add_field(label, value):
        value = str(value) if value not in [None, ''] else 'N/A'
        pdf.set_font('Helvetica', 'B', 12)
        pdf.multi_cell(0, 8, f'{label}: {value}')
        pdf.set_font('Helvetica', '', 12)

    add_field('Farmer Name', entry.get('farmerName', ''))
    add_field('Farm ID', entry.get('farmID', ''))
    add_field('Phone Number', entry.get('phoneNumber', 'N/A'))
    add_field('Location', entry.get('location', 'N/A'))
    add_field('GPS', entry.get('gps', 'N/A'))
    add_field('Farm Size', f"{entry.get('size', 'N/A')} hectares")
    add_field('Farm Type', ', '.join(entry.get('farmType', [])) or 'N/A')
    add_field('Visit Date', entry.get('visitDate', ''))
    add_field('Visit Type', entry.get('visitType', 'N/A'))
    add_field('Officer Name', entry.get('officerName', ''))
    add_field('Time Spent', f"{entry.get('timeSpent', 'N/A')} hours")
    add_field('Main Crops', entry.get('mainCrops', 'N/A'))
    add_field('Crop Stage', entry.get('cropStage', 'N/A'))
    add_field('Livestock Type', entry.get('livestockType', 'N/A'))
    add_field('Animal Count', entry.get('animalCount', '0'))
    add_field('Crop Issues', ', '.join(entry.get('cropIssues', [])) or 'N/A')
    add_field('Livestock Issues', ', '.join(entry.get('livestockIssues', [])) or 'N/A')
    add_field('Advice', entry.get('advice', 'N/A'))
    add_field('Follow-up', 'Needed' if entry.get('followUp') else 'Not Required')
    add_field('Follow-up Date', entry.get('followUpDate', ''))
    add_field('Training', 'Yes' if entry.get('training') else 'No')
    add_field('Referral', 'Yes' if entry.get('referral') else 'No')
    add_field('Additional Notes', entry.get('followUpNotes', ''))
    add_field('Timestamp', entry.get('timestamp', ''))

    pdf_output = pdf.output(dest='S').encode('latin1')
    response = make_response(pdf_output)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename=f"farm_visit_{entry_id}.pdf")
    return response

if __name__ == '__main__':
    ensure_data_file()
    app.run(debug=True) 