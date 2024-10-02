from flask import Flask, render_template, request, flash
from services import ServiceList
from flask_admin import Admin
import os

app = Flask(__name__)

app.secret_key = '_5#y2L"F4Q8zxec]'

UPLOAD_FOLDER = '/home/vivek/.rmp'  # Ensure this folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

admin = Admin(app)
# Add administrative views here
@app.route('/')
def home():
    return render_template("login.html")

@app.route('/pr')
def pr():
    return render_template("reg_professional.html", ServiceList = ServiceList)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form["name"]; password = request.form["password"]; email = request.form["email"];
    YoE = request.form["exp"]; services = request.form.getlist("service"); file = request.files['file'];
    pin = request.form["pin"]; address = request.form["address"];
    
    if file and file.filename.endswith('.pdf'):
        # Save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        #return "File uploaded successfully!", 200
    else:
        flash('Please upload a valid file!', "error")
        return render_template("reg_professional.html", ServiceList = ServiceList)

    return render_template("ex.html", name = name, password = password, email = email, YoE = YoE, services = services,\
    file = file, pin = pin, address = address)

app.run()
