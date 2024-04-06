from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, unique=True)
    email = db.Column(db.String(150), index=True, unique=True)
    password = db.Column(db.String(255), index=True, unique=True)
    role = db.Column(db.String(20)) 
    def __repr__(self):
        return f"{self.name}"
    
class Prediksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jenis = db.Column(db.String(255), nullable=False)
    akurasi = db.Column(db.Float, nullable=False)
    user = db.Column(db.String(255), nullable=False)