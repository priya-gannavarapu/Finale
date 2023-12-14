# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(15), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professorname = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)


class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number', validators=[DataRequired()])
    course_id = IntegerField('Course ID', validators=[DataRequired()])


class ProfessorForm(FlaskForm):
    professorname = StringField('Professor Name', validators=[DataRequired()])
    course_id = IntegerField('Course ID', validators=[DataRequired()])


@app.route('/')
def index():
    students = Student.query.all()
    professors = Professor.query.all()
    return render_template('index.html', students=students, professors=professors)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(
            name=form.name.data,
            phoneNumber=form.phoneNumber.data,
            course_id=form.course_id.data
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html', form=form)


@app.route('/add_professor', methods=['GET', 'POST'])
def add_professor():
    form = ProfessorForm()
    if form.validate_on_submit():
        new_professor = Professor(
            professorname=form.professorname.data,
            course_id=form.course_id.data
        )
        db.session.add(new_professor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_professor.html', form=form)


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.phoneNumber = form.phoneNumber.data
        student.course_id = form.course_id.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html', form=form)


@app.route('/edit_professor/<int:id>', methods=['GET', 'POST'])
def edit_professor(id):
    professor = Professor.query.get(id)
    form = ProfessorForm(obj=professor)
    if form.validate_on_submit():
        professor.professorname = form.professorname.data
        professor.course_id = form.course_id.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_professor.html', form=form)


@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_professor/<int:id>')
def delete_professor(id):
    professor = Professor.query.get(id)
    db.session.delete(professor)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
