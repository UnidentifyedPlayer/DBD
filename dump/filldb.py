from app_config import app, db
from model import *
from flask_sqlalchemy import *
from datetime import *
from datetime import time


week_days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
time_points = time()

def add_obj( instance):
    try:
        db.session.add(instance)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True

def add_base_schedule( doctor,days):
    # try:
    # g = Doctor.query.\
    #     filter_by(first_name = doctor.first_name, middle_name = doctor.middle_name, surname = doctor.surname).one_or_none()
    # except:
    #     return 'multiple doctor identities were found'
    # if g is None:
    #     return 'no doctor identities were found'
    cur_date = datetime.now().toordinal()
    for days_num in range(days):
        next_date = datetime.fromordinal(cur_date+days_num)
        if(next_date.weekday()!=6):
            record = ScheduleRecord(date = next_date,status = 'Работает', doctor_id = doctor.id)
            db.session.add(record)
            db.session.commit()
            #add_obj(db, record)
            add_appointments(next_date,doctor)
            #schedule_rec= ScheduleRecord.query.filter_by(date = next_date, doctor_id = doctor.id)

    return 'insertion proceeded without exceptions'

def add_appointments(next_date,doctor):
    time_points = [time(10,0),time(11,30),time(13,00),time(14,30),time(16,00),time(17,30)]
    for point in time_points:
        new_appointment = Appointment(doctor_id= doctor.id, date = next_date, time = point)
        db.session.add(new_appointment)
        db.session.commit()
        #add_obj(db, new_appointment)

def update_db():
    print("doctors:\n")
    doctors = db.session.query(Doctor).all()
    for doctor in doctors:
        print(doctor)
        log_str = add_base_schedule( doctor, 7)

def recreate_db():
    db.drop_all()
    db.create_all()

def refill_db():
    d1 = Department(name='Гастроэнтерология')
    d2 = Department(name='Андрология')
    d3 = Department(name='Кардиология')
    add_obj(db, d1)
    add_obj(db, d3)
    add_obj(db, d2)
    g = Department.query.filter_by(name='Гастроэнтерология').first().id
    doc1 = Doctor(department_id=g, first_name='Никита',middle_name='Романович',surname='Антонов')
    doc2 = Doctor(department_id=g, first_name='Рафаэль', middle_name='Вартанович', surname='Асатрян')
    con_t1 = ConsultationType(name='Консультация врача-гастроэнтеролога первичная',department_id=g)
    con_t2 = ConsultationType(name='Консультация врача-гастроэнтеролога повторная', department_id=g)
    # u = User(name='admin', email='admin@localhost')
    # db.session.add(u)
    # db.session.commit()
    add_obj(db, doc1)
    add_obj(db, doc2)
    add_obj(db, con_t1)
    add_obj(db, con_t2)


# Create scheme if not exists
if __name__ == '__main__':
    g = 't'