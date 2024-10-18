from flask import Flask, render_template, request, flash, Blueprint, current_app, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from .objs import *
from . import db
from .models import *
import os
from datetime import datetime


main_bp = Blueprint('main', __name__)

login_manager = LoginManager()


@main_bp.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        return redirect(url_for('main.dashboard'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and (user.password == password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
            return render_template('login.html')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        else:
            return render_template('login.html')


@main_bp.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return render_template('login.html')
    elif current_user.role == "customer":
        ThisUsersOrders = Order.query.order_by(Order.booked_at.desc()).all()
        return render_template('c_dash.html', orders=ThisUsersOrders)
    elif current_user.role == "professional":
        professional = Professionals.query.filter_by(
            user_id=current_user.id).first()
        if professional.status == "blocked":
            return "<p>Your Services are blocked. Contact Admin</p>"
        professional_id = professional.id
        orders = Order.query.filter_by(professional_id=professional_id).order_by(
            Order.booked_at.desc()).all()
        return render_template('pro_dash.html', professional=professional, orders=orders)
    elif current_user.role == "admin":
        return render_template('admin/index.html')

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
        new_user = User(username=username, password=password,
                        name=name, email=email, role=role, phone=phone, address=address)

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

@main_bp.route('/userInfo', methods=['GET'])
@login_required
def userInfo():
    return render_template("user_info.html")

@main_bp.route('/user_info_edit', methods=["POST"])
@login_required  # Ensure the user is logged in
def userInfoEdit():
    formData = request.form

    for key, value in formData.items():
        if value:  # Only update if there's a value
            if key == "username":
                # Check if the username is already taken
                if User.query.filter_by(username=value).first():
                    flash("The username is not available. Try something else", "error")
                    return redirect(url_for('main.userInfo'))
            
            # Update the user's attribute
            setattr(current_user, key, value)  # Use setattr to set the attribute

    db.session.commit()  # Save changes to the database

    flash("Data updated successfully!", "success")
    return redirect(url_for('main.userInfo'))








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
        # Gather data from the form
        YoE = request.form["exp"]
        Bname = request.form["b_name"]
        UpFile = request.files['file']
        pin = request.form["pin"]
        address = request.form["address"]
        user_id = current_user.id
        orders = []
        services = {}

        for service in request.form.getlist('service'):
            price = request.form.get(f'price_{service}')
            description = request.form.get(f'description_{service}')
            services[service] = [price, description]

        # Update user role in user table to "professional"

        current_user.role = "professional"

        # Add the this user as a professional in professional database

        NewPro = Professionals(user_id=user_id, business_name=Bname,
                               pin=pin, address=address, orders=orders,
                               ServiceOffered=services, YoE=YoE,
                               status="active")

        db.session.add(NewPro)
        db.session.commit()
        # services in the Services Table

        serviceProvider = Professionals.query.filter_by(
            user_id=user_id).first().id
        for item in services.keys():
            ser = item
            price = services[item][0]
            description = services[item][1]

            newService = Services(service=ser, price=price,
                                  description=description,
                                  serviceProvider=serviceProvider)
            db.session.add(newService)

        db.session.commit()

        # Save the uploaded file in /static/uploads

        if UpFile and UpFile.filename.endswith('.pdf'):
            SaveFile(UpFile, current_app, current_user)
        else:
            flash('Please upload a valid file!', "error")
            return render_template("reg_professional.html", ServiceList=ServiceList)

        file_url = "temp"  # f"uploads/{UpFile.filename}"

        return render_template("pro_dash.html", professional=Professionals.query.filter_by(
            user_id=user_id).first())
    elif current_user.role in ["professional", "admin"]:
        return redirect(url_for('main.dashboard'))
    else:
        flash("You must be a user and logged in to register as a professional", "error")
        return redirect(url_for('main.login'))


@main_bp.route('/accept_reject_it', methods=['POST'])
def AcceptRejectIt():
    val = request.form.get("b_value")
    order_id = request.form.get("order_id")

    if not val or not order_id:
        return redirect(url_for('main.dashboard'))

    order = Order.query.filter_by(order_id=order_id).first()  # Fetch the order

    if order:  # Ensure the order exists
        if val == "Accept":
            order.status = "accepted"
            order.accepted_at = datetime.utcnow()  # Correct usage
        elif val == "Reject":
            order.status = "rejected"
            order.closed_by = "professional"
            order.closed_at = datetime.utcnow()  # Correct usage

        db.session.commit()  # Commit changes to the database

    return redirect(url_for('main.dashboard'))


@main_bp.route('/close_it', methods=['POST'])
def closeIt():
    order_id = request.form["if_close"]
    rating = request.form["rating"]
    remark = request.form["remark"]
    order = Order.query.get(order_id)
    order.status = "close"
    order.rating = float(rating)
    order.remark_by_customer = remark
    order.closed_at = datetime.utcnow()
    order.closed_by = "customer"
    db.session.commit()

    return redirect(url_for('main.dashboard'))


@main_bp.route('/FindService', methods=['POST'])
@login_required
def FindService():
    req_service = request.form["req_service"]
    # Search for services that match the requested service
    avlbleService = Services.query.join(Professionals, Services.serviceProvider == Professionals.id) \
        .filter(
        Services.service.like(f'%{req_service}%'),
        Professionals.status == 'active'
    ).all()

    # Services.query.filter(
    #     Services.service.like(f'%{req_service}%')).all()  # Get all matches

    # Pass both the requested service and the results to the template
    return render_template('find_service_result.html', req_service=req_service, services=avlbleService)


@main_bp.route('/PlaceOrder', methods=['POST'])
@login_required
def PlaceOrder():
    user_id = request.form["customer"]
    professional_id = request.form["professional_id"]

    new_order = Order(user_id=user_id, professional_id=professional_id,
                      status="requested", rating=0.0,
                      )
    db.session.add(new_order)
    db.session.commit()

    return redirect(url_for('main.dashboard'))
