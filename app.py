from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ================= CONFIG =================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "medflow-secret-key"

db = SQLAlchemy(app)

# ================= MODELS =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float,)

    chronic_disease = db.Column(db.String(200))
    allergy = db.Column(db.String(200))
    blood_pressure = db.Column(db.String(20))
    heart_rate = db.Column(db.String(20))
    blood_type = db.Column(db.String(20))
    imaging = db.Column(db.String(255))
    case_desc = db.Column(db.Text)
    diagnosis = db.Column(db.Text)

    color_code = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Waiting")
    prescription = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

# ================= LOGIN ( / ) =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("pass")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= DASHBOARD ( /dashboard ) =================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    return render_template("dashboard.html", role=session.get("role"))


# ================= ADD PATIENT =================
@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.form
    imaging_list = request.form.getlist("imaging[]")
    imaging = ",".join(imaging_list)

    patient = Patient(
        patient_id=data.get("patient_id"),
        name=data.get("name"),
        surname=data.get("surname"),
        sex=data.get("sex"),
        age=data.get("age"),
        height=data.get("height"),
        weight=data.get("weight"),

        chronic_disease=data.get("chronic_disease"),
        allergy=data.get("allergy"),
        blood_pressure=data.get("blood_pressure"),
        heart_rate=data.get("heart_rate"),
        blood_type=data.get("blood_type"),
        imaging=imaging,
        case_desc=data.get("case_desc"),
        diagnosis=data.get("diagnosis"),

        color_code=data.get("color_code"),
        status=data.get("status"),
        prescription=data.get("prescription"),
    )

    db.session.add(patient)
    db.session.commit()
    return redirect("/dashboard")


# ================= SEARCH =================
@app.route("/search_patient")
def search_patient():
    q = request.args.get("q", "")

    patient = Patient.query.filter(
        (Patient.patient_id.ilike(f"%{q}%")) |
        (Patient.name.ilike(f"%{q}%"))
    ).first()

    if not patient:
        return jsonify(None)

    return jsonify({c.name: getattr(patient, c.name) for c in patient.__table__.columns})


# ================= UPDATE =================
@app.route("/update_patient", methods=["POST"])
def update_patient():
    data = request.json
    patient = Patient.query.get(data["id"])

    if not patient:
        return jsonify({"success": False})
    
    allowed_fields = [
        "patient_id","name","surname","sex","age","height","weight",
        "chronic_disease","allergy","blood_pressure","heart_rate",
        "blood_type","case_desc","diagnosis",
        "color_code","status","prescription"
    ]

    for field in allowed_fields:
        if field in data:
            setattr(patient, field, data[field])

    db.session.commit()
    return jsonify({"success": True})

@app.route("/stats")
def stats():
    total = Patient.query.count()
    waiting = Patient.query.filter_by(status="Waiting").count()
    done = Patient.query.filter_by(status="Finish").count()

    colors = {}
    for c in ["Red", "Yellow", "Green", "White", "Black"]:
        colors[c] = Patient.query.filter_by(color_code=c).count()

    return jsonify({
        "total": total,
        "waiting": waiting,
        "done": done,
        "colors": colors
    })

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already exists")

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/dashboard")

    return render_template("register.html")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)