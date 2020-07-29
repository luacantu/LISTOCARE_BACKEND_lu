from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Login %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class Medicalstaff(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    treatments = db.relationship('Treatment', backref='treatment', lazy=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120)) 
    username = db.Column(db.String(80), unique=True, nullable=False)
    def __repr__(self):
        return '<Medicalstaff %r>' % self.first_name
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'),
        nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'),
        nullable=True)
    diagnostic_id = db.Column(db.Integer, db.ForeignKey('diagnostic.id'),
        nullable=True)
    name = db.Column(db.String(120))
    date = db.Column(db.DateTime, nullable=True)
    hospital = db.Column(db.String(120))
    room = db.Column(db.String(120))
    covidtest = db.Column(db.String(120))
    status = db.Column(db.String(120))
    notes = db.Column(db.String(120))
    def __repr__(self):
        return '<Treatment %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "hospital":self.hospital,
            "covidtest":self.covidtest,
            "status":self.status
        }

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String(120))
    address = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(120))
    id_number = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Patient %r>' % self.first_name
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name":self.last_name,
            "id_number":self.id_number
            # do not serialize the password, its a security breach
        }

class Diagnostic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id =db.Column(db.Integer, db.ForeignKey('patient.id'),
        nullable=True)
    name = db.Column(db.String(120))
    covidtestresult = db.Column(db.String(120))
    date_time = db.Column(db.DateTime, nullable=True)
    admission = db.Column(db.String(120))
    symptoms = db.Column(db.String(120))
    status = db.Column(db.String(120))
    notes = db.Column(db.String(120))
    prescription = db.Column(db.String(120))
    total_cost = db.Column(db.String(120))

    def __repr__(self):
        return '<Diagnostic %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "covidtestresult": self.covidtestresult,
            "admission":self.admission,
            "status": self.status    
        }        
