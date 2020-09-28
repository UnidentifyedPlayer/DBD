from app_config import app, db
from model import *
from sqlalchemy import func, subquery
from sqlalchemy.orm import aliased
from functions import format_daytime
from datetime import *

def department_info():
    dep_info = db.session.query(Department,func.count(Doctor.id).label('doc_count')).\
        outerjoin(Doctor, Doctor.department_id==Department.id).group_by(Department.id)
    return dep_info.all()


def doctors_info():
    doctors_info = db.session.query(Doctor, Department.name.label('dep_name')).\
        join(Department, Doctor.department_id == Department.id)
    return doctors_info.all()


def consultations_info():
    consult_info = db.session.query(ConsultationType, Department.name.label('dep_name')). \
        join(Department, ConsultationType.department_id == Department.id)
    return consult_info.all()


def schedules_info():
    schedules = db.session.query(ScheduleRecord, Doctor).join(Doctor,Doctor.id == ScheduleRecord.doctor_id)
    return schedules.all()


def patients_info():
    patients = db.session.query(Patient, func.count(Record.id).label('rec_count')).\
        outerjoin(Record).group_by(Patient.id)
    return patients.all()

def records_info():
    records = db.session.query(Record,Patient,Appointment,Doctor,ConsultationType).select_from(Record).\
        join(Patient, ConsultationType.id == Record.patient_id).\
        join(Appointment, Appointment.id == Record.appointment_id). \
        join(Doctor, Doctor.id == Appointment.doctor_id). \
        join(ConsultationType, ConsultationType.id == Record.consult_type_id)
    records = records.all()
    #for record_index in range(len(records)):
    #    print(records[record_index].Appointment.time)
    #    records[record_index].Appointment.time = format_daytime(records[record_index].Appointment.time)
    return records