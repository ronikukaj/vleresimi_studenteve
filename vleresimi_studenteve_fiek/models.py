from vleresimi_studenteve_fiek import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(prof_given_id):
    return Profesori.query.get(int(prof_given_id))

class Profesori(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    given_id = db.Column(db.Integer, unique=True)
    emri = db.Column(db.String(20))
    mbiemri = db.Column(db.String(20))
    lenda = db.Column(db.String(50))
    password = db.Column(db.String(30))

class Studenti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    given_id = db.Column(db.Integer, unique=True)
    emri = db.Column(db.String(20))
    mbiemri = db.Column(db.String(20))

    def __repr__(self):
        return f"Studenti('{self.emri}', '{self.mbiemri}', '{self.given_id}')"

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lenda = db.Column(db.String(20))
    studenti_id = db.Column(db.Integer)
    kollokfiumi_1 = db.Column(db.Integer)
    kollokfiumi_2 = db.Column(db.Integer)
    detyra_1 = db.Column(db.Integer)
    detyra_2 = db.Column(db.Integer)
    aktiviteti = db.Column(db.Integer)
    vijueshmeria = db.Column(db.Integer)
    nota_value = db.Column(db.Integer)
