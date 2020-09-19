from app_config import app, db
from model import *

from functions import get_nearest_dates, get_not_empty_dep_1, get_schedules
from dump.filldb import *
from functions import *

#from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import desc

from datetime import *

from flask import Flask, url_for, session, redirect, request
from markupsafe import escape
from flask import request
from flask import render_template

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return redirect(url_for('consultations'))


@app.route('/appointments', methods=['POST', 'GET'])
def user_appointments():
    if request.method == "POST":
        if request.form['cmd']=="Удалить":
            record_id = int(request.form['record_id'])
            for appointment in session['appointments']:
                if appointment == record_id:
                    session['appointments'].remove(appointment)
                    session.modified = True
                    db.session.query(Record).filter(Record.id == record_id).delete()
                    db.session.commit()
            print(session['appointments'])
    if 'appointments' in session:
        appointments_data = list()
        #     appointments_data = list()
        #     for appointment_id in session['appointments']:
        #         appointment_data = dict()
        #         appointment_data['record_id'] = appointment_id
        for record_id in session['appointments']:
            appointments_data.append(get_record_info(record_id))
        print(appointments_data)
        print(session['appointments'])
        return render_template("appointments.html", appointments_data=appointments_data)

    return render_template("appointments.html")


@app.route('/consultations')
def consultations():
    departments = db.session.query(Department).order_by(Department.id).all()
    return render_template('consultations.html', departments=departments)


@app.route('/departments/<int:department_id>')
def department_consults(department_id):
    consult_types = db.session.query(ConsultationType). \
        filter(ConsultationType.department_id == department_id). \
        order_by(ConsultationType.id).all()
    return render_template('department_consults.html', depart_id=department_id, consultations=consult_types)


@app.route('/departments/<int:department_id>/<int:consultation_id>/schedule')
def show_timetable(department_id, consultation_id):
    schedule_records = get_schedule_records(department_id)
    doctors = get_doctors(department_id)
    dates = get_nearest_dates()
    # schedules = get_schedules(db, department_id)
    # doctors = list()
    # doc_count = len(Department.doctors)
    # for doc_idx in range(doc_count):
    #     doc_schedule = list()
    #     for day in range(7):
    #         for schedule in schedules:
    #             if(datetime.now().date().toordinal()+day == schedule.date)&&()
    # for doc in range(doc_count):
    #     doctors.append(list())
    # for doc in range(doc_count):
    return render_template('department_schedule.html', consult_id=consultation_id, doctors=doctors, dates=dates,
                           records=schedule_records, day_c=len(dates), doc_c=len(doctors))


@app.route('/department/<int:consultation_id>/<int:doctor_id>/<int:schedule_record_id>/schedule')
def show_day_schedule(schedule_record_id, consultation_id, doctor_id):
    schedule_record = db.session.query(ScheduleRecord).get(schedule_record_id)
    appointments = get_day_schedule(schedule_record.doctor_id, schedule_record.date)
    edit_dates(appointments)
    return render_template('day_schedule.html', appointments=appointments, schedule_record=schedule_record,
                           consult_id=consultation_id, doctor = schedule_record.doctor)


@app.route('/<int:appointment_id>/<int:consultation_id>/form', methods=['POST', 'GET'])
def sign_up(appointment_id, consultation_id):
    errors = list()
    if request.method == 'POST':
        is_form_valid = True
        try:
            print(type(request.form['day']))
            birth_date = date(int(request.form['year']), int(request.form['month']), int(request.form['day']))
        except:
            is_form_valid = False
            errors.append("Неверная дата рождения")
        if is_form_valid:
            insert_appointment_record(request.form, consultation_id, appointment_id)
            record_id = db.session.query(Record.id).filter(Record.appointment_id == appointment_id).first()
            print(record_id[0])
            if ('appointments' not in session):
                print("no array registered, creationg one")
                records = list()
                records.append(record_id[0])
                session['appointments'] = records
            else:
                print("array found")
                session['appointments'].append(record_id[0])
                session.modified = True
            print("session array:")
            print(session['appointments'])
            return redirect(url_for('index'))
    return render_template('form.html', appointment_id=appointment_id, consultation_id=consultation_id, errors=errors)


#@app.route('/hello')
#def hello():
#    return 'Hello, World'


#@app.route('/login')
#def login():
#    return 'login'


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


#@app.route('/test')
#def test():
#    list = []
#    list1 = [1, 4, 5, 6, 6, 7, 8]
#    list2 = [31, 42, 0, 9, 9, 4, 2]
#    list.append(list1)
#    list.append(list2)
#    return render_template('test_template.html', list=list, len=len(list))


def add_obj(instance):
    try:
        db.session.add(instance)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     session.remove()



if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # refill_db()

    #update_db()
    # db.session.rollback()
    # d = Department(name='Диабетология')
    # print("shit")
    # db.session.add(d)
    # db.session.commit()
    app.run(debug=True)
