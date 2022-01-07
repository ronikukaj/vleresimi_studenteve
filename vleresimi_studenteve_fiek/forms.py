from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from vleresimi_studenteve_fiek.models import Studenti

class ProfessorLoginForm(FlaskForm):
    professor_id = StringField('ID', validators=[DataRequired()])
    professor_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Kycu')

class StudentRegistrationForm(FlaskForm):
    given_id = StringField("ID", validators=[DataRequired()])
    emri = StringField('Emri', validators=[DataRequired(), Length(min=2, max=20)])
    mbiemri = StringField('Mbiemri', validators=[DataRequired()])
    submit = SubmitField('Regjistro')

    def validate_student(self, given_id):
        studenti = Studenti.query.filter_by(given_id=given_id.data).first()
        if studenti:
            raise ValidationError('Kjo ID ekziston!')

class StudentLoaderForm(FlaskForm):
    id = StringField('ID e studentit', validators=[DataRequired()])
    submit = SubmitField('Kerko')

class StudentEvaluationForm(FlaskForm):
    emri = StringField('Emri', render_kw={'readonly': True})
    mbiemri = StringField('Mbiemri', render_kw={'readonly': True})
    lenda = StringField('Lenda', render_kw={'readonly': True})
    kollokfiumi_1 = StringField('Kollokfiumi 1', validators=[DataRequired()])
    kollokfiumi_2 = StringField('Kollokfiumi 2', validators=[DataRequired()])
    detyra_1 = StringField('Detyra 1', validators=[DataRequired()])
    detyra_2 = StringField('Detyra 2', validators=[DataRequired()])
    aktiviteti = StringField('Aktiviteti', validators=[DataRequired()])
    vijueshmeria = StringField('Vijueshmeria', validators=[DataRequired()])
    submit = SubmitField('Vlereso')
