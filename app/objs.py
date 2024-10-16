import os
ServiceList = ['Maid Service', 'Housekeeping', 'Laundry', 'Dry Cleaning', 'Carpet Cleaning', 'Upholstery Cleaning', 'Window Cleaning', 'Plumbing', 'Electrical', 'Hvac', 'Handyman', 'Carpenter', 'Pest Control', 'Lawn Care', 'Grocery Shopping', 'Meal Delivery', 'Dog Walking', 'Pet Sitting', 'House Sitting', 'Errand Running', 'Concierge Service', 'Appliance Repair', 'Furniture Assembly', 'Home Renovation', 'Painting', 'Roofing',
               'Flooring', 'Electrical Repair', 'Interior Design', 'Organizing', 'Decluttering', 'Home Staging', 'Move-In/Move-Out Cleaning', 'Yard Work', 'Pool Maintenance', 'Computer Repair', 'Network Setup', 'Smart Home Installation', 'Tv Installation', 'Home Security Systems', 'Wi-Fi Setup', 'Tech Support', 'Personal Shopping', 'Meal Preparation', 'Household Management', 'Elder Care', 'Child Care', 'Event Planning', 'Household Organization']


def SaveFile(UpFile, current_app, current_user):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(
        current_app.config['UPLOAD_FOLDER'], UpFile.filename+f'__{current_user.id}')
    try:
        UpFile.save(filepath)
    except:
        pass
