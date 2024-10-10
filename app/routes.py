from flask import Flask, render_template, request, flash, Blueprint, current_app
from .services import ServiceList
from . import db
from .models import *
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template("login.html")


@main_bp.route('/pr')
def pr():
    return render_template("reg_professional.html", ServiceList = ServiceList)

@main_bp.route('/submit', methods=['POST'])
def submit():
    name = request.form["name"]; password = request.form["password"]; email = request.form["email"];
    YoE = request.form["exp"]; services = request.form.getlist("service"); UpFile = request.files['file'];
    pin = request.form["pin"]; address = request.form["address"];
    
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
