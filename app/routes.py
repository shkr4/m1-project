from flask import Flask, render_template, request, flash, Blueprint, current_app, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from .objs import *
from . import db
from .models import *
import os

main_bp = Blueprint('main', __name__)

login_manager = LoginManager()


@main_bp.route('/')
def home():
    return render_template("login.html")


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        role = "customer"
        order = None
        new_user = User(username=username, password=password,
                        name=name, email=email, role=role, phone=phone, address=address, order=order)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully! Please log in.', 'success')
            return redirect(url_for('main.login'))

        except IntegrityError:
            db.session.rollback()  # Rollback the transaction
            flash('Username already exists, please choose another one.', 'error')
            return redirect(url_for('main.register'))

    else:
        return render_template('reg_customer.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and (user.password == password):
            login_user(user)
            flash('Login successful!', 'success')
            return render_template('ex.html', current_user=current_user)
        else:
            flash('Invalid credentials!', 'danger')
            return render_template('login.html')
    else:
        return render_template('login.html')


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', "success")
    return redirect(url_for('main.login'))


@main_bp.route('/reg_professional', methods=['GET', 'POST'])
def reg_professional():
    if current_user.role == "customer":
        if request.method == "GET":
            return render_template("reg_professional.html", ServiceList=ServiceList)

        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        YoE = request.form["exp"]
        services = request.form.getlist("service")
        UpFile = request.files['file']
        pin = request.form["pin"]
        address = request.form["address"]
        username = request.form["username"]

        upload_folder = current_app.config['UPLOAD_FOLDER']

        if UpFile and UpFile.filename.endswith('.pdf'):
            # Save the file
            filepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'], UpFile.filename)
            UpFile.save(filepath)  # Save the file to the upload folder
            # return "File uploaded successfully!", 200
        else:
            flash('Please upload a valid file!', "error")
            return render_template("reg_professional.html", ServiceList=ServiceList)

        file_url = f"uploads/{UpFile.filename}"

        AddUser(name, email, username, password, role)

        return render_template("ex.html", name=name, password=password, email=email, YoE=YoE, services=services,
                               UpFile=file_url, pin=pin, address=address)
    flash("You must be a user and logged in to register as a professional", "error")
    return redirect(url_for('main.login'))


@main_bp.route('/createNew', methods=['POST'])
def createNew():
    ID = request.form['ID']
    username = request.form['username']
    email = request.form['email']
    new_user = User(ID=ID, username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return "<p>ok</p>"


@main_bp.route('/form3')
def form3():
    return render_template('form3.html')
