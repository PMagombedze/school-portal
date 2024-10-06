"""Flask-SQLAlchemy models
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    password = db.Column(String(128), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    role = db.Column(String(10), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Subject(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100), nullable=False)

class Mark(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(Integer, ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    score = db.Column(Integer, nullable=False)
    student = db.relationship('User', foreign_keys=[student_id])
    subject = db.relationship('Subject')
    teacher = db.relationship('User', foreign_keys=[teacher_id])