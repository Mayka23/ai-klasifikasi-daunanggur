from flask import Flask, render_template, request, redirect, url_for, Response, jsonify, session
from flask_bcrypt import Bcrypt 
from werkzeug.utils import secure_filename
import os
from PIL import Image
import re
from models.AuthModel import db, Users, Prediksi

import sys
import numpy as np
from datetime import datetime
from util import base64_to_pil
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import get_file
import json


app = Flask(__name__)
    
app.config['SECRET_KEY'] = 'mayka'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/klasifikasi'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

bcrypt = Bcrypt(app) 

db.init_app(app)

with app.app_context():
    db.create_all()


app.config['UPLOAD_FOLDER'] = 'static/images'
    
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods = ['GET', 'POST'])
def main():
	return render_template("login.html")

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        fullname = request.form['name']
        password = request.form['password']
        email = request.form['email']

        user_exists = Users.query.filter_by(email=email).first() is not None

        if user_exists:
            mesage = 'Email Tersedia !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Alamat Email Salah'
        elif not fullname or not password or not email:
            mesage = 'Isi Data'
        else:
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = Users(name=fullname, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            mesage = 'Akun Berhasil Terdaftar'
    elif request.method == 'POST':
        mesage = 'Isi Data Tersebut'
    return render_template('register.html', mesage = mesage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == '' or password == '':
            message = 'Masukkan Email Dan Password'
        else:
            user = Users.query.filter_by(email=email).first()

            if user is None:
                message = 'Email tidak terdaftar. Silakan cek kembali.'
            else:
                if not bcrypt.check_password_hash(user.password, password):
                    message = 'Password salah. Silakan cek kembali.'
                else:
                    session['loggedin'] = True
                    session['userid'] = user.id
                    session['name'] = user.name
                    session['email'] = user.email

                    if user.role == 'admin':
                        return redirect(url_for('dashboard'))
                    else:
                        return redirect(url_for('user'))

    return render_template('login.html', message=message)

# load model prediksi
model = load_model('models/model_0.980_0.913.h5')

def model_predict(img, model):
    img = img.resize((224, 224))         
    
    x = image.img_to_array(img)
    x = x.reshape(-1, 224, 224, 3)
    x = x.astype('float32')
    x = x / 255.0
    preds = model.predict(x)
    return preds

@app.route("/user", methods=['GET', 'POST'])
def user():
        
    return render_template("users/home.html")

def store_prediction(jenis, akurasi, user):
    new_prediction = Prediksi(jenis=jenis, akurasi=float(akurasi), user=user)
    db.session.add(new_prediction)
    db.session.commit()

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        img = base64_to_pil(request.json)

        # Buat Prediksi
        preds = model_predict(img, model)

        target_names = ['auxerrois', 'cabernet_franc', 'cabernet_sauvignon', 'chardonnay', 'merlot', 'muller_thurgau', 'pinot_noir', 'riesling', 'sauvignon_blanc', 'syrah', 'tempranillo']  

        hasil_label = target_names[np.argmax(preds)]
        hasil_prob = "{:.2f}".format(100* np.max(preds))
        
        user = Users.query.filter_by(name=session['name']).first()

        if user:
            base_folder = "D:\\anggur\\tes"
            type_folder = hasil_label.lower().replace(" ", "_")
            folder_path = os.path.join(base_folder, type_folder)
            os.makedirs(folder_path, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"uploaded_image_{timestamp}.png"

            img.save(os.path.join(folder_path, filename))
            
            store_prediction(hasil_label, hasil_prob, user)
            return jsonify(result=hasil_label, probability=hasil_prob)
        else:
            return jsonify(error="Pengguna tidak ditemukan.")

    return jsonify(error="Invalid request method")

@app.route("/dashboard", methods =['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:        
        return render_template("admin/dashboard.html")
    return redirect(url_for('login')) 

@app.route("/pengguna", methods =['GET', 'POST'])
def pengguna():
    if 'loggedin' in session:  
        data = Users.query.all()      
        return render_template("admin/user.html", data=data)

@app.route("/data", methods=['GET', 'POST'])
def data():
    if 'loggedin' in session:
        data = Prediksi.query.all()
        if request.method == 'POST':
            show_modal = True
        else:
            show_modal = False
        return render_template("admin/data.html", data=data, show_modal=show_modal)

@app.route('/tambah_user', methods=['GET', 'POST'])
def tambah_user():
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = Users(name=name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('pengguna', successMessage='Data berhasil ditambahkan'))

    return render_template("admin/user.html")

@app.route('/tambah_data', methods=['GET', 'POST'])
def tambah_data():
    if request.method == 'POST':
        
        user = request.form['user']
        jenis = request.form['jenis']
        akurasi = request.form['akurasi']
                
        new_user = Prediksi(user=user, jenis=jenis, akurasi=akurasi)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('data', successMessage='Data berhasil ditambahkan'))

    return render_template("admin/data.html")

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = Users.query.get(user_id)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user.name = name
        user.email = email
        user.password = hashed_password

        db.session.commit()

        return redirect(url_for('pengguna', successMessage='Data berhasil diperbarui'))

    return render_template("admin/user.html")

@app.route('/update_data/<int:data_id>', methods=['POST'])
def update_data(data_id):
    data = Prediksi.query.get(data_id)

    if request.method == 'POST':
        new_user = request.form['user']
        new_jenis = request.form['jenis']
        new_akurasi = request.form['akurasi']

        data.user = new_user
        data.jenis = new_jenis
        data.akurasi = new_akurasi

        db.session.commit()

    return redirect(url_for('data', successMessage='Data berhasil diperbarui'))


@app.route('/get_user/<int:user_id>')
def get_user(user_id):
    user = Users.query.get(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'password': user.password
    })


@app.route("/hapus_user/<int:data_id>", methods=['GET'])
def hapus_user(data_id):
    data = db.session.get(Users, data_id)
    if data:
        db.session.delete(data)
        db.session.commit()
    else:
        return "Data Kosong", 404

    return redirect(url_for('pengguna'))

@app.route("/hapus_data/<int:data_id>", methods=['GET'])
def hapus_data(data_id):
    data = db.session.get(Prediksi, data_id)
    if data:
        db.session.delete(data)
        db.session.commit()
    else:
        return "Data Kosong", 404

    return redirect(url_for('data'))

@app.route("/home", methods =['GET', 'POST'])
def home():
    if 'loggedin' in session:        
        return render_template("users/user_dashboard.html")  

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)