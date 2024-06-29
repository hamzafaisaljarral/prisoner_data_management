from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Crime(db.Model):
    crime_id = db.Column(db.Integer, primary_key=True)
    crime_name = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'crime_id': self.crime_id,
            'crime_name': self.crime_name
        }


class Prison(db.Model):
    prison_id = db.Column(db.Integer, primary_key=True)
    prison_name = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'prison_id': self.prison_id,
            'prison_name': self.prison_name
        }


class Prisoner(db.Model):
    prisoner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)  # Changed from Date to Integer to match your CSV
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    crime_id = db.Column(db.Integer, db.ForeignKey('crime.crime_id'), nullable=False)
    sentence_years = db.Column(db.Integer, nullable=False)
    prison_id = db.Column(db.Integer, db.ForeignKey('prison.prison_id'), nullable=False)

    crime = db.relationship('Crime', backref=db.backref('prisoners', lazy=True))
    prison = db.relationship('Prison', backref=db.backref('prisoners', lazy=True))

    def to_dict(self):
        return {
            'prisoner_id': self.prisoner_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'crime': self.crime.to_dict(),
            'sentence_years': self.sentence_years,
            'prison': self.prison.to_dict()
        }
