from model import *

#from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import desc

from datetime import *
from flask_sqlalchemy import *


def get_not_empty_dep():
    all_depart = db.session.query(Department)
    all_depart.add_column(db.Column('has_consultations', db.Boolean, nullable=False))
    all_depart_list = all_depart.all()
    consult_dep_ids = db.session.query(ConsultationType.department_id).group_by(ConsultationType.department_id).all()
    for depart in all_depart_list:
        depart.has_consultations = False
        for consult_dep_id in consult_dep_ids:
            if (consult_dep_id.department_id == depart.id):
                depart.has_consultations = True
                break
    return all_depart_list


def get_not_empty_dep_1():
    query = db.session.query(Department)
    query.add_column(db.Column('has_consultations', db.Boolean, nullable=False))
    results = query.all()
    for result in results:
        if len(result.consultations):
            result.has_consultations = True
        else:
            result.has_consultations = False
    return results


def get_schedules( depart_id):
    cur_date = datetime.now().date()
    cur_time = datetime.now().time()
    query_1 = db.session.query(Appointment).filter_by(Appointment.date > cur_date).filter_by(
        Appointment.time > cur_time). \
        group_by(Appointment.date, Appointment.doctor_id)
    query_1.add_column('has_appointments', db.Boolean, nullable=False)
    result_1 = query_1.all()
    query_2 = db.session.query(Appointment).filter_by(Appointment.date > cur_date).filter_by(
        Appointment.time > cur_time)
    result_2 = query_2.all()
    for doctor_date in result_1:
        doctor_date.has_appointments = False
        for appoint in result_2:
            if len(appoint.record):
                doctor_date.has_appointments = True
                break
    return result_1


def get_nearest_dates():
    cur_date = datetime.now().date()
    cur_time = datetime.now().time()
    date_limit = date.fromordinal(cur_date.toordinal() + 7)
    dates = db.session.query(ScheduleRecord.date).filter(ScheduleRecord.date >= cur_date,
                                                         ScheduleRecord.date < date_limit).group_by(ScheduleRecord.date)
    return dates.all()


def get_schedule_records(depart_id):
    cur_date = datetime.now().date()
    cur_time = datetime.now().time()
    date_limit = date.fromordinal(cur_date.toordinal() + 7)
    doctors = db.session.query(Doctor.id).filter(Doctor.department_id == depart_id).all()
    doctors_schedule = dict()
    for doctor in doctors:
        doctors_schedule[doctor.id] = dict()
        schedules = db.session.query(ScheduleRecord).filter(ScheduleRecord.date >= cur_date,
                                                          ScheduleRecord.date < date_limit,
                                                          ScheduleRecord.doctor_id == doctor.id).all()
        doc = db.session.query(Doctor).get(doctor.id)
        for schedule in schedules:
            doctors_schedule[doc.id][schedule.date.toordinal()] = schedule
    return doctors_schedule


def get_doctors(depart_id):
    query_1 = db.session.query(Doctor).filter(Doctor.department_id == depart_id)
    return query_1.all()


def get_day_schedule(doctor_id, date):
    cur_time = datetime.now().time()
    day_appointments = db.session.query(Appointment).filter(Appointment.date == date, Appointment.doctor_id == doctor_id)
    day_appointments.add_column(db.Column('has_appointments', db.Boolean,nullable=False))
    appointments = day_appointments.all()
    for appointment in appointments:
        appointment.has_appointments = (appointment.record is not None)
    return appointments


def insert_appointment_record(form_data, consult_id, appointment_id):
    patient_id = get_patient_id(form_data)
    record = Record(appointment_id=appointment_id, consult_type_id=consult_id, patient_id=patient_id)
    db.session.add(record)
    db.session.commit()


def search_patient(form_data):
    patient_id = db.session.query(Patient.id).filter(Patient.first_name == form_data["first_name"],
                                                     Patient.middle_name == form_data["middle_name"],
                                                     Patient.surname == form_data["surname"],
                                                     Patient.policy_num == form_data["policy_num"]).first()
    return patient_id


def get_patient_id(form_data):
    patient_id = search_patient(form_data)
    if patient_id is None:
        db.session.add(Patient(first_name=form_data["first_name"],
                               middle_name=form_data["middle_name"],
                               surname=form_data["surname"],
                               policy_num=form_data["policy_num"]))
        db.session.commit()
        patient_id = search_patient(form_data)
    return patient_id[0]

def get_record_info(record_id):
    record = db.session.query(Record).filter(Record.id == record_id).first()
    appointment = record.appointment
    doctor = appointment.doctor
    consultation = record.consult_type.name
    time = format_daytime(appointment.time)
    patient = record.patient
    return {'doctor': doctor, 'consultation': consultation ,
            'time': time, 'date': appointment.date, 'record_id': record_id, 'patient': record.patient}

def edit_dates(appointments):
    for appointment in appointments:
        appointment.time = format_daytime(appointment.time)

def format_daytime(time):
    return format_int(time.hour)+":" +format_int(time.minute)

def format_int(time):
    t = str(time)
    if(len(t)==1):
        t = "0" + t
    return t

