from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "fake_doctors_secure_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
db = SQLAlchemy(app)

# --- 1. Database Model (ปรับตามหน้า UI ของคุณ) ---
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True, nullable=False) # Assign ID
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    
    # ข้อมูลอาการ (Symptom)
    chronic_disease = db.Column(db.String(200))
    allergy = db.Column(db.String(200))
    blood_pressure = db.Column(db.String(20))
    heart_rate = db.Column(db.String(20))
    case_desc = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    
    # สถานะและการจัดการ
    color_code = db.Column(db.String(20)) # Green, Blue, Yellow, Red, Black
    status = db.Column(db.String(20), default='Waiting') # Waiting / Finish
    prescription = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- 2. Routes (เชื่อมโยงตามหน้าเว็บ) ---

@app.route('/')
def login_page():
    return render_template('login.html')

# Page 2: Dashboard
@app.route('/dashboard')
def dashboard():
    # ดึงสถิติจำนวนคนไข้แยกตามสี
    stats = {
        'green': Patient.query.filter_by(color_code='green').count(),
        'blue': Patient.query.filter_by(color_code='blue').count(),
        'yellow': Patient.query.filter_by(color_code='yellow').count(),
        'red': Patient.query.filter_by(color_code='red').count(),
        'black': Patient.query.filter_by(color_code='black').count(),
        'total_waiting': Patient.query.filter_by(status='Waiting').count()
    }
    return render_template('dashboard.html', stats=stats)

# Page 3: Add Patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        new_p = Patient(
            patient_id=request.form.get('patient_id'),
            name=request.form.get('name'),
            surname=request.form.get('surname'),
            sex=request.form.get('sex'),
            age=request.form.get('age'),
            color_code=request.form.get('color_code'), # จากปุ่มสีที่คุณทำไว้
            status='Waiting'
        )
        db.session.add(new_p)
        db.session.commit()
        flash('เพิ่มข้อมูลคนไข้ใหม่เรียบร้อยแล้ว')
        return redirect(url_for('dashboard'))
    return render_template('add_patient.html')

# Page 4: Edit Information
@app.route('/edit_patient/<pid>', methods=['GET', 'POST'])
def edit_patient(pid):
    patient = Patient.query.filter_by(patient_id=pid).first()
    if request.method == 'POST' and patient:
        patient.name = request.form.get('name')
        # ... อัปเดตฟิลด์อื่นๆ ตามฟอร์ม ...
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit.html', patient=patient)

# Page 5: Update Status (หน้าจ่ายยา/ปิดเคส)
@app.route('/update_status', methods=['GET', 'POST'])
def update_status():
    patient = None
    if request.method == 'POST':
        search_id = request.form.get('search_id')
        patient = Patient.query.filter_by(patient_id=search_id).first()
        
        if 'update_action' in request.form: # เมื่อกดปุ่ม Update
            patient.prescription = request.form.get('prescription')
            patient.status = request.form.get('status_btn') # Waiting หรือ Finish
            db.session.commit()
            return redirect(url_for('dashboard'))
            
    return render_template('status.html', patient=patient)

if __name__ == '__main__':
    app.run(debug=True)