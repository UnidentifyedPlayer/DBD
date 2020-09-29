#from app_config import app, db
from model import *

from functions import get_nearest_dates, get_not_empty_dep_1, get_schedules
from dump.filldb import *
from functions import *
from Tables import *

from forms import  *
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import desc

from datetime import *

from flask import Flask, url_for, session, redirect, request,flash
from markupsafe import escape
from flask import request
from flask import render_template

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# TODO: add editing of already existing departments, doctors, consultations and schedules, patients
# TODO: add search by department for doctors and consultations pages, by doctors for schedules page
# TODO: add page for records, implement only deletion function there( we have the insertion already elsewhere)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def index():
    return redirect(url_for('consultations'))

@app.route('/admin/tables/')
@login_required
def tables():
    return render_template('table_views/tables.html')


@app.route('/admin/departments')
@login_required
def departments_table():
    deps_info = department_info()
    return render_template('table_views/department_table.html', deps_info = deps_info)

@app.route('/admin/department/add', methods=["GET", "POST"])
@login_required
def insert_department():
    form = DepartmentInsertForm()
    if form.validate_on_submit():
        dep = Department(name = form.name.data)
        db.session.add(dep)
        db.session.commit()
        return redirect(url_for('departments_table'))
    return render_template('table_views/department_form.html', form = form)



# TODO: проконтроллировать удаелние связанных консультаций/докторов
#  (Возможно, сделать цепочку методов для пользования всеми раутами удаления)
@app.route('/admin/department/delete/<int:department_id>')
@login_required
def delete_department(department_id):
    dep = db.session.query(Department).get(department_id)
    db.session.delete(dep)
    db.session.commit()
    return redirect(url_for('departments_table'))



@app.route('/admin/doctors')
@login_required
def doctor_table():
    docs_info = doctors_info()
    return render_template('table_views/doctors_table.html', docs_info = docs_info)


@app.route('/admin/schedules')
@login_required
def schedules_table():
    schedules = schedules_info()
    return render_template('table_views/schedules.html', schedules = schedules)


@app.route('/admin/consultations')
@login_required
def consultations_table():
    consults_info = consultations_info()
    return render_template('table_views/consultations_table.html', consults_info = consults_info)


@app.route('/admin/patients')
@login_required
def patients_table():
    patients = patients_info()
    return render_template('table_views/patients.html', patients = patients)


@app.route('/admin/records')
@login_required
def records_table():
    records = records_info()
    return render_template('table_views/records.html', records = records)


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    feedback = ''
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        u = db.session.query(User).\
            filter(User.login == form.login.data).\
            filter(User.password == form.password.data).\
            one_or_none()
        if u is None:
            feedback =  "Неверное имя пользователя или пароль"
            flash("Invalid username/password", 'error')
            return redirect(url_for('login'))
        else:
            login_user(u)
            return redirect(url_for('admin'))

    return render_template('login.html', feedback=feedback, form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


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


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


#@app.route('/login')
#def login():
#    return 'login'


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


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


def check_admin():
    admin = db.session.query(User).filter(User.email=="admin_test@mail.com").all()
    if(len(admin)==0):
        print(admin)
        new_admin = User(name="Админ Админович",login="adminlog",
                         email="admin_test@mail.com",password="adminpassw", role ="admin",
                         created_on=datetime.utcnow(), updated_on=datetime.utcnow() )
        db.session.add(new_admin)
        db.session.commit()


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    check_admin()
    # refill_db()

    #update_db()
    # db.session.rollback()
    # d = Department(name='Диабетология')
    # print("shit")
    # db.session.add(d)
    # db.session.commit()
    app.run(debug=True)
