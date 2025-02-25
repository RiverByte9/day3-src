from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Bind SQLAlchemy directly

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    attendance = db.relationship('Attendance', backref='student', lazy=True)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    new_student = Student(name=name)
    db.session.add(new_student)
    db.session.commit()
    return redirect('/')

@app.route('/attendance', methods=['POST'])
def mark_attendance():
    student_id = request.form['student_id']
    status = request.form['status']
    new_attendance = Attendance(student_id=student_id, status=status)
    db.session.add(new_attendance)
    db.session.commit()
    return redirect('/')

# Initialize DB inside app context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
