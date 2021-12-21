from flask import render_template, url_for, flash, redirect, request
from vleresimi_studenteve_fiek import app, db
from vleresimi_studenteve_fiek.forms import ProfessorLoginForm, StudentRegistrationForm, StudentEvaluationForm, StudentLoaderForm
from vleresimi_studenteve_fiek.models import Studenti, Nota

@app.route('/')
def intro():
    return render_template('intro.html', title="Intro Page")

@app.route('/prof-login', methods=['GET', 'POST'])
def prof_login():
    form = ProfessorLoginForm()
    if form.validate_on_submit():
        if form.professor_id.data == '100100' and form.professor_password.data == '1234':
            flash('Jeni kycur me sukses!', 'success')
            return redirect(url_for('registration'))
        else:
            flash('Kredenciale te gabuara', 'danger')
            return redirect(url_for('prof_login'))
    return render_template('profesor-login.html', title="Qasja", form=form)

@app.route('/regjistrimi-i-studenteve', methods=['GET', 'POST'])
def registration():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        studenti_krahasues = Studenti.query.filter_by(given_id=form.given_id.data).first()
        if studenti_krahasues:
            flash('Studenti me kete ID ekziston!', 'danger')
            return redirect(url_for('registration'))
        studenti = Studenti(given_id=form.given_id.data, emri=form.emri.data, mbiemri=form.mbiemri.data)
        db.session.add(studenti)
        db.session.commit()
        flash('Studenti u regjistrua me sukses', 'success')
        return redirect(url_for('registration'))
    return render_template('regjistrimi_i_studenteve.html', title="Regjistrimi", form=form)

@app.route('/vleresimi-i-studenteve', methods=['GET', 'POST'])
def evaluation():
    form = StudentLoaderForm()
    if form.validate_on_submit():
        studenti_krahasues = Studenti.query.filter_by(given_id=int(form.id.data)).first()
        if not studenti_krahasues:
            flash('Studenti me kete ID nuk ekziston!', 'danger')
            return redirect(url_for('evaluation'))
        studenti = Studenti.query.filter_by(given_id=int(form.id.data)).first()
        return redirect(url_for('student_evaluation', studenti_given_id=studenti.given_id))
    return render_template('vleresimi_i_studenteve.html', title="Vleresimi", form=form)

@app.route('/vleresimi-i-studenteve/<int:studenti_given_id>', methods=['GET', 'POST'])
def student_evaluation(studenti_given_id):
    form = StudentEvaluationForm()
    studenti = Studenti.query.filter_by(given_id=studenti_given_id).first()
    form.emri.data = studenti.emri
    form.mbiemri.data = studenti.mbiemri
    if form.validate_on_submit():
        grade = 0
        piket = int(form.kollokfiumi_1.data) + int(form.kollokfiumi_2.data) + int(form.detyra_1.data) + int(form.detyra_2.data) + int(form.aktiviteti.data) + int(form.vijueshmeria.data)
        if piket > 100:
            flash('Jepni vlerat shuma e te cilave te jete me e vogel se 100!', 'warning')
            return redirect(url_for('student_evaluation', studenti_given_id=studenti_given_id))
        elif piket > 0 and piket < 50:
            grade = 5
        elif piket >= 50 and piket < 60:
            grade = 6
        elif piket >= 60 and piket < 70:
            grade = 7
        elif piket >= 70 and piket < 80:
            grade = 8
        elif piket >= 80 and piket < 90:
            grade = 9
        elif piket >= 90 and piket <= 100:
            grade = 10

        nota_krahasuese = Nota.query.filter_by(lenda=form.lenda.data, studenti_id=studenti_given_id).first()
        if(nota_krahasuese):
            flash('Ky student eshte i notuar ne kete lende!', 'danger')
            return redirect(url_for('student_evaluation', studenti_given_id=studenti_given_id))
        nota = Nota(lenda=form.lenda.data, studenti_id=studenti_given_id, kollokfiumi_1=int(form.kollokfiumi_1.data), kollokfiumi_2=int(form.kollokfiumi_2.data), detyra_1=int(form.detyra_1.data), detyra_2=int(form.detyra_2.data), aktiviteti=int(form.aktiviteti.data), vijueshmeria=int(form.vijueshmeria.data), nota_value=grade)
        db.session.add(nota)
        db.session.commit()
        flash('Studenti eshte notuar me sukses!', 'success')
        return redirect(url_for('evaluation'))
    return render_template('vleresimi_specifik.html', title="Vleresimi", form=form)

@app.route('/te-dhenat')
def data():
    studentet = Studenti.query.all()
    return render_template('te_dhenat.html', title="Te Dhenat", studentet=studentet)

@app.route('/te-dhenat/<int:studenti_given_id>/info')
def individual_data(studenti_given_id):
    studenti = Studenti.query.filter_by(given_id=studenti_given_id).first()
    notat = Nota.query.filter_by(studenti_id=studenti_given_id)
    return render_template('te_dhenat_specifike.html', title="Te Dhenat", studenti=studenti, notat=notat)
