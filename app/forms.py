from flask_wtf import FlaskForm
from app.models import Student, Professor
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError

class LoginForm(FlaskForm):
    type = SelectField('Select Account Type',choices=[('student','student'),('professor','professor')],validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    type = SelectField('Select Account Type',choices=[('student','student'),('professor','professor')],validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,email):
        if (Student.query.filter_by(stud_email=email.data).first() is not None):
           raise ValidationError('This email is already registered')
        elif (Professor.query.filter_by(prof_email=email.data).first() is not None):
           raise ValidationError('This email is already registered')

class EditTaskForm(FlaskForm):
    description = StringField('Task Description', validators=[DataRequired()])
    priority = IntegerField('Priority')
    submit = SubmitField('Update Task')

class AddTaskForm(FlaskForm):
    description = StringField('Task Description', validators=[DataRequired()])
    priority = IntegerField('Priority')
    submit = SubmitField('Add Task')

class AddAssignmentForm(FlaskForm):
    course_number = IntegerField('Course Number', validators=[DataRequired()])
    description = StringField('Task Description', validators=[DataRequired()])
    submit = SubmitField('Add Assignment')

class EditAssignmentForm(FlaskForm):
    course_number = IntegerField('Course Number', validators=[DataRequired()])
    description = StringField('Task Description', validators=[DataRequired()])
    submit = SubmitField('Update Assignment')

class AddCourseForm(FlaskForm):
    course_number = IntegerField('Course Number', validators=[DataRequired()])
    course_name = StringField('Course Name', validators=[DataRequired()])
    submit = SubmitField('Add Course')

