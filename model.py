from app_config import db
from sqlalchemy import Column, Integer, String
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column( db.Integer, primary_key=True)
    policy_num = db.Column(db.Integer, unique=True, nullable=True)
    first_name = db.Column( db.String(50), nullable =False)
    middle_name = db.Column( db.String(120), nullable =True)
    surname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Patient %r %r>' % (self.first_name, self.surname)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column( db.Integer, primary_key=True)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    department = db.relationship('Department', backref=db.backref('doctors', lazy=True))

    first_name = db.Column( db.String(50), nullable =False)
    middle_name = db.Column( db.String(120), nullable =True)
    surname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Doctor %r %r>' % (self.first_name, self.surname)

class Department(db.Model):
    __tablename__='departments'
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(120),unique=True, nullable = False)

    def __repr__(self):
        return '<Отдел %r >' % (self.name)

class ScheduleRecord(db.Model):
    __tablename__='chedule_records'
    id = db.Column(db.Integer, primary_key = True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'),nullable=False)
    doctor = db.relationship('Doctor', backref=db.backref('schedules', lazy=True))

    date = db.Column(db.Date,nullable=False)
    status = db.Column(db.String(40), nullable=False)
    unique_status = db.UniqueConstraint('doctor_id','date')

    # def __repr__(self):
    #     return '<Отдел %r >' % (self.name)

class ConsultationType(db.Model):
    __tablename__='consult_types'
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(120), nullable = False)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    department = db.relationship('Department', backref = db.backref('consultations',lazy = True))

class Appointment(db.Model):
    __tablename__='appointments'
    id = db.Column(db.Integer, primary_key=True)
    record = db.relationship('Record', uselist=False)

    doctor_id= db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    doctor = db.relationship('Doctor')

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    unique_time = db.UniqueConstraint('doctor_id','date','time')

class Record(db.Model):
    __tablename__='records'
    id= db.Column(db.Integer, primary_key = True)

    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    appointment = db.relationship('Appointment')

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'),nullable = False)
    patient = db.relationship('Patient')

    consult_type_id = db.Column(db.Integer, db.ForeignKey('consult_types.id'),nullable=False)
    consult_type = db.relationship('ConsultationType')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    login = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    # Flask-Login Support
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

