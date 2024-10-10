ServiceList = ['Maid Service', 'Housekeeping', 'Laundry', 'Dry Cleaning', 'Carpet Cleaning', 'Upholstery Cleaning', 'Window Cleaning', 'Plumbing', 'Electrical', 'Hvac', 'Handyman', 'Carpenter', 'Pest Control', 'Lawn Care', 'Grocery Shopping', 'Meal Delivery', 'Dog Walking', 'Pet Sitting', 'House Sitting', 'Errand Running', 'Concierge Service', 'Appliance Repair', 'Furniture Assembly', 'Home Renovation', 'Painting', 'Roofing', 'Flooring', 'Electrical Repair', 'Interior Design', 'Organizing', 'Decluttering', 'Home Staging', 'Move-In/Move-Out Cleaning', 'Yard Work', 'Pool Maintenance', 'Computer Repair', 'Network Setup', 'Smart Home Installation', 'Tv Installation', 'Home Security Systems', 'Wi-Fi Setup', 'Tech Support', 'Personal Shopping', 'Meal Preparation', 'Household Management', 'Elder Care', 'Child Care', 'Event Planning', 'Household Organization']

def FileSave():
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

def AddUser():
    user = User(name = name, password = password, email = email, YoE = YoE, services = services, pin = pin,
    address = address, username = username, role = role)
    db.session.add(user)
    db.session.commit()