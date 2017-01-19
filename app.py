# -*- coding: utf-8 -*-

""" Sistema de controle para a IPM (International Punishment Machines)

	Criado por Arthur Mendes

"""

from flask import Flask, url_for, request, redirect, abort, render_template, session
from models.Database import Database, installDatabase

app = Flask("ipm-control")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['IPM_LICENSE_FOLDER'] = '/tmp/licenses'

Database.createDatabase(app)
installDatabase(Database.database.db)

from Cliente import Client
from Hardware import Hardware
from Employee import Employee
import hashlib
import datetime

Client.LicenseFolder = app.config['IPM_LICENSE_FOLDER']

def check_if_logged():
    if not 'userid' in session:
        return False

    return True


@app.route("/")
def show_index():
    return render_template("index.html")

# Login route
@app.route("/login", methods=['GET', 'POST'])
def do_login():
    if request.method == 'GET':
        return redirect(url_for('show_index'))

    if not 'username' in request.form:
        return redirect(url_for('show_index'))

    # Be careful, the password is unencrypted here
    # I think I may send the password encrypted, but only if I enforce Javascript?
    if not 'password' in request.form:
        return redirect(url_for('show_index'))

    username = request.form.get('username')
    password = hashlib.sha256(request.form.get('password')).hexdigest()

    emp = Employee.getUserByUsername(username)
    if emp == False:
        return redirect(url_for('show_index', err='INVALID_USERNAME'))

    if emp.checkPassword(password) == False:
        return redirect(url_for('show_index', err='INVALID_PASSWORD'))

    session['username'] = emp.username
    session['userid'] = emp.ID
    session['login_time'] = datetime.datetime.now()
    return redirect(url_for('show_dashboard'))

# Logout route
@app.route('/logout')
def logout():
    # Register logout
    emp = Employee.getUserByID(session['userid'])
    emp.registerEmployeeTime(session['login_time'], datetime.datetime.now())    

    session.pop('username')
    session.pop('userid', None)
    return redirect(url_for('show_index'))

# Dashboard route
# Here, the employee can search all clients and machines
@app.route('/dashboard')
def show_dashboard():
    if check_if_logged() == False:
        return redirect(url_for('show_index'))
    
    return render_template('dashboard.html')

# Client add
@app.route('/dashboard/client/add')
def dashboard_client_add():
    if check_if_logged() == False:
        return redirect(url_for('show_index'))
    
    return render_template('dashboard_client_add.html')

# Client find
@app.route('/dashboard/client/find')
def dashboard_client_find():
    if check_if_logged() == False:
        return redirect(url_for('show_index'))
    
    text = request.args.get('client_name')
    return render_template('dashboard_client_find.html', client=text)

# Client get
@app.route('/dashboard/client/<int:clientid>/')
def dashboard_client_get(clientid):
    if check_if_logged() == False:
        return redirect(url_for('show_index'))
    
    # Do not load the client now, let the javascript code load it
    return render_template('dashboard_client.html', client_id=clientid)


import json

# Client api routes
@app.route("/api/client/add")
def add_client():

    if check_if_logged() == False:
        abort(403)    
    
    if not 'name' in request.args:
        abort(400)

    cli = Client(request.args.get('name'))
    cli.addIntoDatabase()
    return json.dumps(cli.getObjects())

@app.route("/api/client/<int:clientid>")
def get_client(clientid):
    
    if check_if_logged() == False:
        abort(403)    
    
    cli = Client.getClientFromID(clientid)

    if cli == False:
        return "{}";
            
    return json.dumps(cli.getObjects())

@app.route("/api/client/search/")
def search_client():    
    if check_if_logged() == False:
        abort(403)    
    
    if not 'name' in request.args:
        abort(400)

    name = request.args.get('name')
    if len(name) < 3:
        return "[]" # Too short

    json_list = []   
    clis = Client.getClientFromName(name)

    if clis == False:
        return "[]" # No clients

    for cli in clis:
        json_list.append(cli.getObjects())

    return json.dumps(json_list)
    
    

@app.route("/api/client/<int:clientid>/remove")
def remove_client(clientid):
    if check_if_logged() == False:
        abort(403)    

    cli = Client.getClientFromID(clientid)

    if cli == False:
        return '{}'

    cli.removeFromDatabase()
    return "Client %s removed successfully" % cli.name

@app.route("/api/client/<int:clientid>/update/")
def update_client(clientid):
    if check_if_logged() == False:
        abort(403)    

    cli = Client.getClientFromID(clientid)

    if cli == False:
        return '{}'

    if not 'name' in request.args:
        abort(400)
        
    cli.name = request.args.get('name')
    cli.updateIntoDatabase()
    return "Client {} is now {}".format(str(clientid), cli.name)

@app.route("/api/client/<int:clientid>/license_file")
def get_license_file(clientid):
    if check_if_logged() == False:
        abort(403)    

    cli = Client.getClientFromID(clientid)

    if cli == False:
        abort(404)

    cfile = cli.readLicenseFile()

    if cfile == False:
        abort(404)

    return cfile, 200, {'Content-Type': 'application/x-ipm-license'}


# Hardware api routes
@app.route("/api/client/<int:client_id>/hardware/")
def get_hardware_by_client(client_id):
    if check_if_logged() == False:
        abort(403)    
    
    cli = Client.getClientFromID(client_id)
    if cli == False:
        return "[]"

    hws = Hardware.getHardwaresByClient(cli)
    if hws == False:
        return "[]"

    hw_list = []
    for hw in hws:
        hw_list.append(hw.getObjects())
    
    return json.dumps(hw_list)


@app.route("/api/client/<int:client_id>/hardware/add/")
def add_hardware(client_id):
    if check_if_logged() == False:
        abort(403)    
    
    if not 'name' in request.args:
        abort(400)

    cli = Client.getClientFromID(client_id)
    if cli == False:
        return "No client"

    name = request.args.get('name')
    desc = request.args.get('desc')
        
    hw = Hardware(cli, name, desc)
    hw.addIntoDatabase()
    return str(hw.ID)

@app.route("/api/hardware/<int:hwid>/")
def get_hardware(hwid):
    if check_if_logged() == False:
        abort(403)
        
    hw = Hardware.getHardwareByID(hwid)

    if hw == False:
        return "No hardware"

    return hw.name

@app.route("/api/hardware/<int:hwid>/remove/")
def remove_hardware(hwid):
    if check_if_logged() == False:
        abort(403)
    
    hw = Hardware.getHardwareByID(hwid)

    if hw == False:
        return "No hardware"

    hw.removeFromDatabase()

@app.route("/api/hardware/<int:hwid>/update")
def update_hardware(hwid):
    if check_if_logged() == False:
        abort(403)
        
    hw = Hardware.getHardwareByID(hwid)

    if hw == False:
        return "No hardware"

    name = request.args.get('name')
    desc = request.args.get('desc')
    if not name is None:
        hw.name = name

    if not desc is None:
        hw.desc = desc

    hw.updateIntoDatabase()

# Show employee's time logging information
@app.route("/api/employee/<int:employeeid>/log")
def show_employee_time_log(employeeid):
    if check_if_logged() == False:
        abort(403)
        
    emp = Employee.getUserByID(employeeid)

    if emp == False:
        return "[]"

    return json.dumps(emp.getEmployeeTime())
    

try:
    e = Employee('tester', hashlib.sha256('tester').hexdigest())
    e.insertIntoDatabase()
except:
    print('>>> User already into database')

Database.database.db.session.rollback()
    
app.secret_key = 'GALLIFREYFALLSNOMORE'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
