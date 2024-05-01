# MODULE IMPORTS

# Flask modules
from flask import Flask, flash, jsonify, render_template, request, url_for, request, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_talisman import Talisman
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Other modules
from forex_python.converter import CurrencyRates
from urllib.parse import urlparse, urljoin
from datetime import datetime
import configparser
import json
import sys
import os

from pymongo import MongoClient

# Local imports
from user import User, Anonymous
from message import Message
from note import Note
from email_utility import send_email, send_registration_email, send_message_email
from verification import confirm_token
from project import Project

# Create app
app = Flask(__name__)

# Configuration
config = configparser.ConfigParser()
config_file_path = 'configuration.ini'

if not os.path.exists(config_file_path):
    print(f"Required '{config_file_path}'  doesn't exist. Exiting...")
    # Print a list with all existing files.
    print("Existing files:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if config_file_path in file:
                # Print file and abs file path
                print(f"Configuration file path: {os.path.join(root, file)}")
    exit(1)
else:
    config.read(config_file_path)

default = config['DEFAULT']

if not default:
    print("Error at reading default. Exiting...")
    exit(1)

app.secret_key = default['SECRET_KEY']
app.config['MONGO_DBNAME'] = default['DATABASE_NAME']
app.config['MONGO_URI'] = default['MONGO_URI'] #default['MONGO_URI']
app.config['PREFERRED_URL_SCHEME'] = "https"


# create a MongoClient object
mongo = MongoClient('mongodb://localhost:27017/')

# Check if database is initialized and connection is successful
try:
    mongo.db.command("ping")
    print("Database initialized and connection successful!")
except Exception as e:
    print("Error initializing database and/or connecting to database:", e)
    sys.exit(1)

# Create Bcrypt
bc = Bcrypt(app)

# Create Talisman
csp = {
    'default-src': [
        '\'self\'',
        'https://stackpath.bootstrapcdn.com',
        'https://pro.fontawesome.com',
        'https://code.jquery.com',
        'https://cdnjs.cloudflare.com'
    ]
}
talisman = Talisman(app, content_security_policy=csp)

# Create CSRF protect
csrf = CSRFProtect()
csrf.init_app(app)

# Create login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"



# Functions
# TODO: De mutat mai sus / utils si de folosit pt config.ini

def loadJSON (filepath):
    filename = os.path.basename(filepath)
    if os.path.exists(filepath):
        with open(filepath) as f:
            json_structure = json.load(f)
        return json_structure
    else:
        print(f"Required '{filename}' doesn't exist. Exiting...")
        # Print a list with all existing files.
        print("Possible file paths for:")
        for root, dirs, files in os.walk("."):
            for file in files:
                if filename in file:
                    # Print file and abs file path
                    print(f"{os.path.join(root, file)}\n")
        sys.exit(1) 

# ROUTES

# Index
@app.route('/')
def index():
    return render_template('index.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            # Redirect to index if already authenticated
            return redirect(url_for('index'))
        # Render login page
        return render_template('login.html', error=request.args.get("error"))
    # Retrieve user from database
    users = mongo.db.users
    user_data = users.find_one({'email': request.form['email']}, {'_id': 0})
    if user_data:
        # Check password hash
        if bc.check_password_hash(user_data['password'], request.form['pass']):
            # Create user object to login (note password hash not stored in session)
            user = User.make_from_dict(user_data)
            login_user(user)

            # Check for next argument (direct user to protected page they wanted)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)

            # Go to profile page after login
            return redirect(next or url_for('profile'))

    # Redirect to login page on error
    return redirect(url_for('login', error=1))


# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Trim input data
        email = request.form['email'].strip()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        role = request.form['role'].strip()
        roleName = mongo.db.settings.find_one({"settings_id": "roles"})[role]
        password = request.form['pass'].strip()

        users = mongo.db.users
        # Check if email address already exists
        existing_user = users.find_one(
            {'email': email}, {'_id': 0})
        

        if existing_user is None:
            logout_user()
            # Hash password
            hashpass = bc.generate_password_hash(password).decode('utf-8')
            # Create user object (note password hash not stored in session)
            new_user = User(first_name, last_name, [roleName], email)
            # Create dictionary data to save to database
            user_data_to_save = new_user.dict()
            user_data_to_save['password'] = hashpass

            # Insert user record to database
            if users.insert_one(user_data_to_save):
                login_user(new_user)
                # send_registration_email(new_user)
                return redirect(url_for('profile'))
            else:
                # Handle database error
                return redirect(url_for('register', error=2))

        # Handle duplicate email
        return redirect(url_for('register', error=1))
    
    settingsRoles = mongo.db.settings.find({"settings_id": "roles"})
    roles = {}

    for role in settingsRoles:
        for key in role:
            if key != "_id" and key != "settings_id":
                roles[key] = role[key]
    
    # Return template for registration page if GET request
    return render_template('register.html', error=request.args.get("error"), roles=roles.items())


# Confirm email
@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    logout_user()
    try:
        email = confirm_token(token)
        if email:
            if mongo.db.users.update_one({"email": email}, {"$set": {"verified": True}}):
                return render_template('confirm.html', success=True)
    except:
        return render_template('confirm.html', success=False)
    else:
        return render_template('confirm.html', success=False)


# Verification email
@app.route('/verify', methods=['POST'])
@login_required
def send_verification_email():
    if current_user.verified == False:
        send_registration_email(current_user)
        return "Verification email sent"
    else:
        return "Your email address is already verified"

# Profile
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    # Find notes created by the current user
    notes = mongo.db.notes.find({"user_id": current_user.id, "deleted": False}).sort("timestamp", -1)
    
    settingsRoles = mongo.db.settings.find({"settings_id": "roles"})
    roles = {}

    # Do not send out id fields.
    for role in settingsRoles:
        for key in role:
            if key != "_id" and key != "settings_id":
                roles[key] = role[key]

    print("#################### DEBUG ####################")
    print(f"Current user: {current_user.first_name} {current_user.last_name}")
    print(f"Current user roles: {current_user.dict()}")
    print(f"Databse settings roles: {roles}")
    print("###############################################")
          
    return render_template('profile.html', notes=notes, roles=roles.items())
    


# Households
@app.route('/projects', methods=['GET'])
@login_required
def projects():
    # Find projects where the current user is a member
    joined_projects = mongo.db.project.find({"members.id": current_user.id})
    projects_list = mongo.db.project.find()
    project_details = mongo.db.project.find_one({"id": projects_list[0]['id']})
    
    return render_template('projects.html', joined_projects=joined_projects, projects_list = projects_list, selected_project = project_details)

# Messages
@app.route('/messages', methods=['GET'])
@login_required
def messages():
    all_users = mongo.db.users.find(
        {"id": {"$ne": current_user.id}}, {'_id': 0})
    inbox_messages = mongo.db.messages.find(
        {"to_id": current_user.id, "deleted": False}).sort("timestamp", -1)
    sent_messages = mongo.db.messages.find(
        {"from_id": current_user.id, "deleted": False, "hidden_for_sender": False}).sort("timestamp", -1)
    return render_template('messages.html', users=all_users, inbox_messages=inbox_messages, sent_messages=sent_messages)




# Logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# POST REQUEST ROUTES

# Change Name
@app.route('/change_name', methods=['POST'])
@login_required
def change_name():
    
    first_name = request.form['first_name'].strip()
    last_name = request.form['last_name'].strip()

    # Find all project that contain the current user's ID in the members list
    projects = mongo.db.projects.find({"members": current_user.id})

    for project in projects:
        # Update the project's owner info with the new name
        mongo.db.projects.update_one(
            {"_id": projects["_id"]},
            {"$set": {"owner_info.first_name": first_name, "owner_info.last_name": last_name}}
        )

        # Update the member's name in the project's members list
        mongo.db.projects.update_one(
            {"_id": projects["_id"], "members": current_user.id},
            {"$set": {"members.$": {"id": current_user.id, "first_name": first_name, "last_name": last_name}}}
        )

    # Update the user's name in the users collection
    if mongo.db.users.update_one({"email": current_user.email}, {"$set": {"first_name": first_name, "last_name": last_name}}):
        return "User name updated successfully"
    else:
        return "Error! Could not update user name"

# Add note
@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    title = request.form.get("title")
    body = request.form.get("body")
    user_id = current_user.id
    user_name = current_user.display_name()
    note = Note(title, body, user_id, user_name)
    if mongo.db.notes.insert_one(note.dict()):
        return "Success! Note added: " + title
    else:
        return "Error! Could not add note"
    
# TODO: Use jsonLoad function 
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    project_config_file='./settings/base_struct_config.json'
    if os.path.exists(project_config_file):
        with open(project_config_file) as f:
            json_structure = json.load(f)
        return render_template('add_project.html', data=json_structure,isinstance=isinstance)
    else:
        print(f"Required '{project_config_file}' doesn't exist. Exiting...")
        # Print a list with all existing files.
        print("Existing files:")
        for root, dirs, files in os.walk("."):
            for file in files:
                if "base_struct_config" in file:
                    # Print file and abs file path
                    print(f"base_struct_config file path: {os.path.join(root, file)}")
        exit(1)
   
    
# Add project member
@app.route('/add_project_member', methods=['POST'])
@login_required
def add_project_member():
    project_id = request.form.get("project")
    user_id = request.form.get("add_member_id")
    user = mongo.db.users.find_one({"id": user_id})
    
    if user is None:
        return "Error! User not found."

    
    user_data = {
        'id': user["id"],
        'first_name': user["first_name"],
        'last_name': user["last_name"],
        'email': user["email"],
        'verified': user["verified"] 
    }
    
    member_ids = []
    for member in mongo.db.project.find_one({"id": project_id}, {"members": 1})["members"]:
        member_ids.append(member['id'])
    
    if user_id in member_ids:
        flash("Error! Member already exists.")
        return "Error! Member already exists."
    
    if mongo.db.project.update_one({"id": project_id}, {"$push": {"members": user_data}}):
        flash("Success! Member added.")
        return "Success! Member added."
    else:
        flash("Error! Could not add member.")
        return "Error! Could not add member."
   

@app.route('/delete_project_member', methods=['POST'])
@login_required
def delete_project_member():
    project_id = request.form.get("project")
    user_id = request.form.get("remove_member_id")
    print(f"user_id: {user_id}")
    print(f"project_id: {project_id}")
    
    user = mongo.db.users.find_one({"id": user_id})
    print(f"user: {user}")
    
    if user is None:
        return "Error! User not found."
    
    member_ids = []
    for member in mongo.db.project.find_one({"id": project_id}, {"members": 1})["members"]:
        member_ids.append(member['id'])
    
    if user_id not in member_ids:
        return "Error! Member does not exist."
    
    if mongo.db.project.update_one({"id": project_id}, {"$pull": {"members": {"id": user_id}}}):
        return "Success! Member deleted."
    else:
        return "Error! Could not delete member."


   

# Delete note
@app.route('/delete_note', methods=['POST'])
@login_required
def delete_note():
    note_id = request.form.get("note_id")
    if mongo.db.notes.update_one({"id": note_id}, {"$set": {"deleted": True}}):
        return "Success! Note deleted"
    else:
        return "Error! Could not delete note"


# Send message
@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    title = request.form.get("title")
    body = request.form.get("body")
    from_id = current_user.id
    from_name = current_user.display_name()
    to_id = request.form.get("user")
    to_user_dict = mongo.db.users.find_one({"id": to_id})
    to_user = User.make_from_dict(to_user_dict)
    to_name = to_user.display_name()
    message = Message(title, body, from_id, from_name, to_id, to_name)
    if mongo.db.messages.insert_one(message.dict()):
        send_message_email(from_user=current_user,
                           to_user=to_user, message=message)
        return "Success! Message sent to " + to_name + ": " + title
    else:
        return "Error! Could not send message"


# Delete message
@app.route('/delete_message', methods=['POST'])
@login_required
def delete_message():
    message_id = request.form.get("message_id")
    if mongo.db.messages.update_one({"id": message_id}, {"$set": {"deleted": True}}):
        return "Success! Message deleted"
    else:
        return "Error! Could not delete message"


# Hide sent message
@app.route('/hide_sent_message', methods=['POST'])
@login_required
def hide_sent_message():
    message_id = request.form.get("message_id")
    if mongo.db.messages.update_one({"id": message_id}, {"$set": {"hidden_for_sender": True}}):
        return "Success! Message hidden from sender"
    else:
        return "Error! Could not hide message"




# Change Role
@app.route('/change_role', methods=['POST'])
@login_required
def change_role():
    role = request.form['role'].strip()

    roleName = mongo.db.settings.find_one({"settings_id": "roles"})[role]

    # Update the user's name in the users collection
    if mongo.db.users.update_one({"email": current_user.email}, {"$push": {"role": roleName}}):
        return "User name updated successfully"
    else:
        return "Error! Could not update user name"
    
# Clear Roles
@app.route('/clear_roles', methods=['POST'])
@login_required
def clear_roles():
    if mongo.db.users.update_one({"email": current_user.email}, {"$set": {"role": []}}):
        return "Roles cleared successfully"
    else:
        return "Error! Could not clear roles."
    
# Change Role
@app.route('/add_role', methods=['POST'])
@login_required
def add_role():
    role = request.form['role'].strip()
    roleName = mongo.db.settings.find_one({"settings_id": "roles"})[role]

    print("##################################################")
    print("DEBUG:")
    print(f"role: {role}")
    print(f"roleName: {roleName}")
    print("##################################################")
    
    # Update the user's name in the users collection
    if mongo.db.users.update_one({"email": current_user.email}, {"$push": {"role": roleName}}):
        return "Role added successfully"
    else:
        return "Error! Could not add role."


@app.route('/change_project', methods=['POST'])
@login_required
def change_project():
    project_id = request.form.get('project_id')
    # Find projects where the current user is a member
    joined_projects = mongo.db.project.find({"members.id": current_user.id})
    projects_list = mongo.db.project.find()
    project_details = mongo.db.project.find_one({"id": project_id})

    return render_template('projects.html', joined_projects=joined_projects, projects_list = projects_list, selected_project = project_details)
    
    
# Create Household
@app.route('/create_project', methods=['POST'])
@login_required
def create_project():
    name = request.form['name'].strip()
    type = request.form['type'].strip()
    address = request.form['address'].strip()

    # Create object data
    new_project = Project(name, type, address, current_user.dict())

    # Create dictionary data to save to database
    project_data_to_save = new_project.dict()

    print("###################### DEBUG ######################")
    print(f"project_data_to_save: {project_data_to_save}")
    print("###################################################")

    if mongo.db.project.insert_one(project_data_to_save):
        return "Household created successfully"
  
@app.route('/get_project_details', methods=['POST'])
def get_project_details():
    project_id = request.form.get('project_id')
    # Fetch the project details based on the project_id
    # This will depend on how you're storing the project details
    selected_project_details = mongo.db.project.find_one({'id': project_id})
    if selected_project_details is not None and '_id' in selected_project_details:
        selected_project_details['_id'] = str(selected_project_details['_id'])
    print(f"selected_project_details = {selected_project_details}")
    return jsonify(selected_project_details)

@app.route('/delete_project', methods=['POST'])
@login_required
def delete_project():
    project_id = request.form.get('project_id')
    project_name = request.form.get('project_name')

    project = mongo.db.project.find_one({'id': project_id})

    if project is None:
        flash("Error! Household not found.")
        return redirect(url_for('profile'))

    if project['name'] != project_name:
        flash("Error! The project name does not match.")
        return redirect(url_for('profile'))

    if mongo.db.project.delete_one({'id': project_id}):
        flash("Household deleted successfully")
    else:
        flash("Error deleting project")

    return redirect(url_for('profile'))


# Delete Account
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id

    # Deletion flags
    user_deleted = False
    notes_deleted = False
    messages_deleted = False

    # Delete user details
    if mongo.db.users.delete_one({"id": user_id}):
        user_deleted = True
        logout_user()

    # Delete notes
    if mongo.db.notes.delete_many({"user_id": user_id}):
        notes_deleted = True

    # Delete messages
    if mongo.db.messages.delete_many({"$or": [{"from_id": user_id}, {"to_id": user_id}]}):
        messages_deleted = True

    return {"user_deleted": user_deleted, "notes_deleted": notes_deleted, "messages_deleted": messages_deleted}


# LOGIN MANAGER REQUIREMENTS

# Load user from user ID
@login_manager.user_loader
def load_user(userid):
    # Return user object or none
    users = mongo.db.users
    user = users.find_one({'id': userid}, {'_id': 0})

    if user:
        return User.make_from_dict(user)
    return None


# Safe URL
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


# Heroku environment
if os.environ.get('APP_LOCATION') == 'heroku':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
else:
    app.run(host="0.0.0.0", port=8080, debug=True)


