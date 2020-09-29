from wtforms import StringField, SubmitField, TextAreaField,  BooleanField, PasswordField, SelectField, DateField, HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()

class DepartmentInsertForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    submit = SubmitField("Добавить")

class DepartmentUpdateForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    submit = SubmitField("Сохранить")

class DoctorInsertForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    department_id = SelectField(u'Отдел')
    submit = SubmitField("Сохранить")

class ScheduleInsertForm(FlaskForm):
    date =  DateField('Дата')
    status = SelectField(u'Статус')
    doctor_id = HiddenField()