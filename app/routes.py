from flask import render_template, redirect,session, flash, url_for
from app import app, db, cursor,connection
from app.forms import LoginForm, RegisterForm, AddTaskForm, AddAssignmentForm, EditTaskForm, EditAssignmentForm, AddCourseForm
from app.models import Student, Professor, Task, Course, Prof_course, Prof_task, Prof_stud, Stud_task, Stud_course, Assignment
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.type.data == 'student'):
             user = Student.query.filter_by(stud_email=form.email.data).first()
             email = form.email.data
             type = form.type.data
        elif (form.type.data == 'professor'):
             user = Professor.query.filter_by(prof_email=form.email.data).first()
             email = form.email.data
             type = form.type.data
        if (user is None or not user.check_password(form.password.data)):
            flash('Invalid email or password')
            return redirect(url_for('index'))
        session['USER'] = email
        session['TYPE'] = type
        flash('You were successfully logged in')
        return redirect(url_for('tasklist'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if (form.type.data == 'student'):
             user = Student(stud_email = form.email.data, stud_name=form.name.data, stud_password=form.password.data)
             user.set_password(form.password.data)
             db.session.add(user)
        if(form.type.data == 'professor'):
             user = Professor(prof_email = form.email.data, prof_name=form.name.data, prof_password=form.password.data)
             user.set_password(form.password.data)
             db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('USER',None)
    session.pop('TYPE',None)
    return redirect(url_for('index'))

@app.route('/tasklist', methods=['GET','POST'])
def tasklist():
    tasks = []
    if (session['TYPE'] == 'student'):
        user = Student.query.filter_by(stud_email = session['USER'])
        tasks = Stud_task.query.filter_by(stud_email = session['USER'])
    if (session['TYPE'] == 'professor'):
        user = Professor.query.filter_by(prof_email = session['USER'])
        tasks = Prof_task.query.filter_by(prof_email = session['USER'])
    form = AddTaskForm()
    if form.validate_on_submit():
        t = Task(task_name=form.description.data,priority=form.priority.data)
        db.session.add(t)
        db.session.commit()
        if (session['TYPE'] == 'student'):
            t = Task.query.filter_by(task_name=form.description.data).filter_by(priority=form.priority.data).first()
            id = t.task_id
            email = session['USER']
            task_name = form.description.data
            priority = form.priority.data
            cursor.execute("INSERT INTO stud_task (stud_email,task_id,task_name,priority) values(%s,%s,%s,%s)",(email,id,task_name,priority))
            connection.commit()
            flash('You have successfully added a task!')
            return redirect(url_for('tasklist'))
        if(session['TYPE'] == 'professor'):
            t = Task.query.filter_by(task_name=form.description.data).filter_by(priority=form.priority.data).first()
            id = t.task_id
            email = session['USER']
            task_name = form.description.data
            priority = form.priority.data
            cursor.execute("INSERT INTO prof_task (prof_email,task_id,task_name,priority) values(%s,%s,%s,%s)",(email,id,task_name,priority))
            connection.commit()
            flash('You have successfully added a task!')
            return redirect(url_for('tasklist'))
    return render_template('tasklist.html',form=form,tasks=tasks)

@app.route('/assignmentlist', methods=['GET','POST'])
def assignmentlist():
    if (session['TYPE'] =='student'):
        assignment = []
        courses = Stud_course.query.filter_by(stud_email=session['USER'])
        for c in courses:
            assignments = Assignment.query.filter_by(course_number=c.course_number)
            for a in assignments:
                assignment.append(a)
    if(session['TYPE'] =='professor'):
       assignment = []
       courses = Prof_course.query.filter_by(prof_email=session['USER'])
       for c in courses:
           assignments = Assignment.query.filter_by(course_number=c.course_number)
           for a in assignments:
               assignment.append(a)
    form = AddAssignmentForm()
    if form.validate_on_submit():
        t = Task(task_name=form.description.data)
        db.session.add(t)
        db.session.commit()
        t = Task.query.filter_by(task_name=form.description.data).first()
        ct = Assignment(course_number=form.course_number.data,task_id=t.task_id, task_name=form.description.data)
        db.session.add(ct)
        db.session.commit()
        flash('You have successfully added a task!')
        return redirect(url_for('assignmentlist'))
    form_2 = AddCourseForm()
    if form_2.validate_on_submit():
        if (Course.query.filter_by(course_number=form_2.course_number.data).first() is None):
            c = Course(course_number = form_2.course_number.data, course_name = form_2.course_name.data)
            db.session.add(c)
        if (session['TYPE'] == 'professor'):
            if (Prof_course.query.filter_by(prof_email = session['USER']).filter_by(course_number=form_2.course_number.data).first() is None):
                 pc = Prof_course(prof_email = session['USER'], course_number=form_2.course_number.data, course_name=form_2.course_name.data)
                 db.session.add(pc)
                 flash('You have successfully added a course!')
        if (session['TYPE'] == 'student'):
            if (Stud_course.query.filter_by(stud_email = session['USER']).filter_by(course_number=form_2.course_number.data).first() is None):
                sc = Stud_course(stud_email = session['USER'], course_number=form_2.course_number.data, course_name=form_2.course_name.data)
                db.session.add(sc)
                flash('You have successfully added a course!')
        db.session.commit()
        return redirect(url_for('assignmentlist'))
    return render_template('assignmentlist.html',assignment=assignment, form=form,form_2 = form_2)

@app.route('/delete_task/<int:id>',methods=['POST'])
def delete_task(id):
        cursor.execute('DELETE FROM task WHERE task_id = %s', (id,)) 
        cursor.execute('DELETE FROM prof_task WHERE task_id = %s', (id,)) 
        cursor.execute('DELETE FROM stud_task WHERE task_id = %s', (id,)) 
        connection.commit()
        flash('Your task has been deleted.')
        return redirect(url_for('tasklist'))

@app.route('/delete_task2/<int:id>',methods=['POST'])
def delete_task2(id):
        cursor.execute('DELETE FROM task WHERE task_id = %s', (id,)) 
        cursor.execute('DELETE FROM assignment WHERE task_id = %s', (id,))  
        connection.commit()
        flash('Your assignment has been deleted.')
        return redirect(url_for('assignmentlist'))

@app.route('/update_task/<int:id>', methods=['GET','POST'])
def update_task(id):
    form = EditTaskForm()
    if form.validate_on_submit():
        task_name = form.description.data
        priority = form.priority.data
        cursor.execute('UPDATE task SET task_id = %s, priority = %s, task_name = %s where task_id = %s',(id,priority,task_name,id,))
        connection.commit()
        if (session['TYPE'] == 'student'):
            stud_email = session['USER']
            task_name = form.description.data
            priority = form.priority.data
            cursor.execute('UPDATE stud_task SET stud_email = %s, task_id = %s, priority = %s, task_name = %s where task_id = %s',(stud_email,id,priority,task_name,id,))
            connection.commit()
        if(session['TYPE'] == 'professor'):
            prof_email = session['USER']
            task_name = form.description.data
            priority = form.priority.data
            cursor.execute('UPDATE prof_task SET prof_email = %s, task_id = %s, priority = %s, task_name = %s where task_id = %s',(prof_email,id,priority,task_name,id,))
            connection.commit()  
        return redirect(url_for('tasklist'))
    return render_template('update_task.html', form=form)


@app.route('/update_task2/<int:id>', methods=['GET','POST'])
def update_task2(id):
    form = EditAssignmentForm()
    if form.validate_on_submit():
        t = Task.query.filter_by(task_id = id).first()
        if(t is not None):
            task_name = form.description.data
            cursor.execute('UPDATE task SET task_id = %s, task_name = %s where task_id = %s',(id,task_name,id,))
            connection.commit()
        ct = Assignment.query.filter_by(task_id=id).first() 
        if (ct is not None):
            course_number = form.course_number.data
            task_name = form.description.data
            cursor.execute('UPDATE assignment SET task_id = %s, task_name = %s, course_number = %s where task_id = %s',(id,task_name,course_number,id,))
            connection.commit()  
        return redirect(url_for('assignmentlist'))
    return render_template('update_task2.html', form=form)

@app.route('/sort_priority', methods=['GET','POST'])
def sort_priority():
    if (session['TYPE']=='student'):
        tasks = Stud_task.query.filter_by(stud_email = session['USER']).order_by(Stud_task.priority.asc())
    if (session['TYPE']=='professor'):
        tasks = Prof_task.query.filter_by(prof_email=session['USER']).order_by(Prof_task.priority.asc()) 
    return render_template('sort_priority.html', tasks = tasks)

@app.route('/roster', methods=['GET','POST'])
def roster():
    email = session['USER']
    roster = []
    course = Prof_course.query.filter_by(prof_email=email).all()
    for c in course:
        roster.append(Stud_course.query.filter_by(course_number = c.course_number).all())

    return render_template('roster.html', roster=roster)




