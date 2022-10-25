from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
   
class Student(db.Model):
   __tablename__ = 'student'
   stud_email = db.Column(db.String(40),nullable=False,primary_key=True)
   stud_password = db.Column(db.String(128),nullable=False)
   stud_name = db.Column(db.String(20),nullable=False)
   total_tasks = db.Column(db.Integer)

   def __repr__(self):
       return '<{}>'.format(self.name)

   def set_password(self, password):
       self.stud_password = generate_password_hash(password)

   def check_password(self, password):
       return check_password_hash(self.stud_password, password)
   
class Professor(db.Model):
   __tablename__ = 'professor'
   prof_email = db.Column(db.String(40),nullable=False,primary_key=True)
   prof_password = db.Column(db.String(128),nullable=False)
   prof_name = db.Column(db.String(20),nullable=False)

   def __repr__(self):
       return '<{}>'.format(self.name)

   def set_password(self, password):
       self.prof_password = generate_password_hash(password)

   def check_password(self, password):
       return check_password_hash(self.prof_password, password)
    
class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer,nullable=False,primary_key=True)
    priority = db.Column(db.Integer)
    task_name = db.Column(db.String(40),nullable=False)

    def __repr__(self):
        return '<{}>'.format(self.task_name)

class Course(db.Model):
    __tablename__ = 'course'
    course_number = db.Column(db.Integer,nullable=False,primary_key=True)
    course_name = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<{}>'.format(self.course_name)

class Prof_course(db.Model):
    __tablename__ = 'prof_course'
    prof_email = db.Column(db.String(40),nullable=False, primary_key = True)
    course_number = db.Column(db.Integer,nullable=False, primary_key = True)
    course_name = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<{}>'.format(self.course_name)

class Prof_task(db.Model):
    __tablename__ = 'prof_task'
    prof_email = db.Column(db.String(40),nullable=False, primary_key = True)
    task_id = db.Column(db.Integer,nullable=False, primary_key = True)
    priority = db.Column(db.Integer)
    task_name = db.Column(db.String(40), nullable=False) 

    def __repr__(self):
        return '<{}>'.format(self.task_name)

class Prof_stud(db.Model):
    __tablename__ = 'prof_stud'
    prof_email = db.Column(db.String(40),nullable=False, primary_key = True)
    stud_email = db.Column(db.Integer,nullable=False, primary_key = True)
    stud_name = db.Column(db.String(20)) 

    def __repr__(self):
        return '<{}{}>'.format(self.stud_name, self.stud_email)

class Stud_task(db.Model):
    __tablename__ = 'stud_task'
    stud_email = db.Column(db.String(40),nullable=False, primary_key = True)
    task_id = db.Column(db.Integer,nullable=False, primary_key = True)
    priority = db.Column(db.Integer)
    task_name = db.Column(db.String(40), nullable=False) 
   
    def __repr__(self):
        return '<{}>'.format(self.task_name)

class Stud_course(db.Model):
    __tablename__ = 'stud_course'
    stud_email = db.Column(db.String(40),nullable=False, primary_key = True)
    course_number = db.Column(db.Integer,nullable=False, primary_key = True)
    course_name = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<{}>'.format(self.course_name)

class Assignment(db.Model):
    __tablename__ = 'assignment'
    course_number = db.Column(db.Integer,nullable=False, primary_key = True)
    task_id = db.Column(db.Integer,nullable=False, primary_key = True)
    priority = db.Column(db.Integer)
    task_name = db.Column(db.String(40), nullable=False) 

    def __repr__(self):
        return '<{}>'.format(self.task_name)







    
    
  
   


