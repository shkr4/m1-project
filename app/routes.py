from flask import Flask, render_template, request, flash, Blueprint, current_app, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .objs import *
from . import db
from .models import *
import os

main_bp = Blueprint('main', __name__)

login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(current_app)

@main_bp.route('/')
def home():
    return render_template("login.html")

@main_bp.route('/lgnrq')
@login_required
def lgnrq():
    return "<p>You are logged in</p>"

# @login_manager.user_loader
# def load_user(user_id):
# 	return User.query.get(int(user_id))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and (user.password == password):
            login_user(user)
            flash('Login successful!', 'success')
            return render_template('ex.html', current_user = current_user)
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/reg_professional')
def reg_professional():
    return render_template("reg_professional.html", ServiceList = ServiceList)

@main_bp.route('/submit', methods=['POST'])
def submit():
    name = request.form["name"]; password = request.form["password"]; email = request.form["email"];
    YoE = request.form["exp"]; services = request.form.getlist("service"); UpFile = request.files['file'];
    pin = request.form["pin"]; address = request.form["address"]; username = request.form["username"];
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    if UpFile and UpFile.filename.endswith('.pdf'):
        # Save the file
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], UpFile.filename)
        UpFile.save(filepath)  # Save the file to the upload folder
        #return "File uploaded successfully!", 200
    else:
        flash('Please upload a valid file!', "error")
        return render_template("reg_professional.html", ServiceList = ServiceList)
        
    file_url = f"uploads/{UpFile.filename}"

    AddUser(name, email, username, password, role)

    return render_template("ex.html", name = name, password = password, email = email, YoE = YoE, services = services,\
    UpFile = file_url, pin = pin, address = address)
    
@main_bp.route('/createNew', methods = ['POST'])
def createNew():
	ID = request.form['ID']
	username = request.form['username']
	email = request.form['email']
	new_user = User(ID = ID, username = username, email= email)
	db.session.add(new_user)
	db.session.commit()
	return "<p>ok</p>"

@main_bp.route('/form3')
def form3():
	return render_template('form3.html')
