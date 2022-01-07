from flask import render_template, url_for, flash, redirect, request
from vleresimi_studenteve_fiek import app, db, bcrypt
from vleresimi_studenteve_fiek.forms import ProfessorLoginForm, StudentRegistrationForm, StudentEvaluationForm, StudentLoaderForm
from vleresimi_studenteve_fiek.models import Studenti, Nota, Profesori
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/')
def intro():
    return render_template('intro.html', title="Intro Page")

@app.route('/prof-login', methods=['GET', 'POST'])
def prof_login():
    if current_user.is_authenticated:
        return redirect(url_for('registration'))
    form = ProfessorLoginForm()
    if form.validate_on_submit():
        prof = Profesori.query.filter_by(given_id=form.professor_id.data).first()
        if prof and bcrypt.check_password_hash(prof.password, form.professor_password.data):
            login_user(prof, remember=False)
            flash('Jeni kycur me sukses!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('registration'))
        else:
            flash('Kredenciale te gabuara', 'danger')
            return redirect(url_for('prof_login'))
    return render_template('profesor-login.html', title="Qasja", form=form)

@app.route('/prof-logout')
@login_required
def prof_logout():
    logout_user()
    return redirect(url_for('intro'))

@app.route('/profesori-te-dhena')
@login_required
def prof_data():
    return render_template('prof.html', title="Te Dhenat")

@app.route('/regjistrimi-i-studenteve', methods=['GET', 'POST'])
@login_required
def registration():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        studenti_krahasues = Studenti.query.filter_by(given_id=form.given_id.data).first()
        if studenti_krahasues:
            flash('Studenti me kete ID ekziston!', 'danger')
            return redirect(url_for('registration'))
        if not (form.emri.data).isalpha() or not (form.mbiemri.data).isalpha():
            flash('Ju lutem shenoni vetem shkronja!', 'danger')
            return redirect(url_for('registration'))
        studenti = Studenti(given_id=form.given_id.data, emri=form.emri.data, mbiemri=form.mbiemri.data)
        db.session.add(studenti)
        db.session.commit()
        flash('Studenti u regjistrua me sukses', 'success')
        return redirect(url_for('registration'))
    return render_template('regjistrimi_i_studenteve.html', title="Regjistrimi", form=form)

@app.route('/vleresimi-i-studenteve', methods=['GET', 'POST'])
@login_required
def evaluation():
    form = StudentLoaderForm()
    if form.validate_on_submit():
        try:
            a = int(form.id.data)
        except:
            flash('Ju lutem shenoni vetem numra!', 'warning')
            return redirect(url_for('evaluation'))
        studenti_krahasues = Studenti.query.filter_by(given_id=int(form.id.data)).first()
        if not studenti_krahasues:
            flash('Studenti me kete ID nuk ekziston!', 'danger')
            return redirect(url_for('evaluation'))
        studenti = Studenti.query.filter_by(given_id=int(form.id.data)).first()
        return redirect(url_for('student_evaluation', studenti_given_id=studenti.given_id))
    return render_template('vleresimi_i_studenteve.html', title="Vleresimi", form=form)

@app.route('/vleresimi-i-studenteve/<int:studenti_given_id>', methods=['GET', 'POST'])
@login_required
def student_evaluation(studenti_given_id):
    form = StudentEvaluationForm()
    studenti = Studenti.query.filter_by(given_id=studenti_given_id).first()
    form.emri.data = studenti.emri
    form.mbiemri.data = studenti.mbiemri
    form.lenda.data = current_user.lenda
    if form.validate_on_submit():
        try:
            kollokfiumi_1 = int(form.kollokfiumi_1.data)
            kollokfiumi_2 = int(form.kollokfiumi_2.data)
            detyra_1 = int(form.detyra_1.data)
            detyra_2 = int(form.detyra_2.data)
            aktiviteti = int(form.aktiviteti.data)
            vijueshmeria = int(form.vijueshmeria.data)
        except:
            flash('Ju lutem shenoni vetem numra!', 'warning')
            return redirect(url_for('student_evaluation', studenti_given_id=studenti_given_id))
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
        nota = Nota(lenda=current_user.lenda, studenti_id=studenti_given_id, kollokfiumi_1=int(form.kollokfiumi_1.data), kollokfiumi_2=int(form.kollokfiumi_2.data), detyra_1=int(form.detyra_1.data), detyra_2=int(form.detyra_2.data), aktiviteti=int(form.aktiviteti.data), vijueshmeria=int(form.vijueshmeria.data), nota_value=grade)
        db.session.add(nota)
        db.session.commit()
        flash('Studenti eshte notuar me sukses!', 'success')
        return redirect(url_for('evaluation'))
    return render_template('vleresimi_specifik.html', title="Vleresimi", form=form)

@app.route('/te-dhenat')
@login_required
def data():
    studentet = Studenti.query.all()
    return render_template('te_dhenat.html', title="Te Dhenat", studentet=studentet)

@app.route('/te-dhenat/<int:studenti_given_id>/info')
@login_required
def individual_data(studenti_given_id):
    studenti = Studenti.query.filter_by(given_id=studenti_given_id).first()
    notat = Nota.query.filter_by(studenti_id=studenti_given_id)
    return render_template('te_dhenat_specifike.html', title="Te Dhenat", studenti=studenti, notat=notat)
