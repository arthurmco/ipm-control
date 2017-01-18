# -*- coding: utf-8 -*-

""" Sistema de controle para a IPM (International Punishment Machines)

	Criado por Arthur Mendes

"""

from flask import Flask, url_for, request, redirect, abort, render_template, session
from models.Database import Database, installDatabase

app = Flask("ipm-control")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

Database.createDatabase(app)
installDatabase(Database.database.db)

from Cliente import Client
from Hardware import Hardware
from Employee import Employee
import hashlib

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

    session['userid'] = emp.ID        
    return redirect(url_for('show_dashboard'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('show_index'))

# Dashboard route
# Here, the employee can search all clients and machines
@app.route('/dashboard')
def show_dashboard():
    return render_template('dashboard.html')


# Client api routes
@app.route("/api/client/add")
def add_client():
    if not 'name' in request.args:
        abort(400)

    cli = Client(request.args.get('name'))
    cli.addIntoDatabase()
    return str(cli.ID)

@app.route("/api/client/<int:clientid>")
def get_client(clientid):
    cli = Client.getClientFromID(clientid)

    if cli == False:
        return 'No client'
            
    return cli.name

@app.route("/api/client/<int:clientid>/remove")
def remove_client(clientid):
    cli = Client.getClientFromID(clientid)

    if cli == False:
        return 'No client'

    cli.removeFromDatabase()
    return "Client %s removed successfully" % cli.name

@app.route("/api/client/<int:clientid>/update/")
def update_client(clientid):
    cli = Client.getClientFromID(clientid)

    if cli == False:
        return 'No client'

    if not 'name' in request.args:
        abort(400)
        
    cli.name = request.args.get('name')
    cli.updateIntoDatabase()
    return "Client {} is now {}".format(str(clientid), cli.name)

# Hardware api routes
@app.route("/api/client/<int:client_id>/hardware/add/")
def add_hardware(client_id):
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
    hw = Hardware.getHardwareByID(hwid)

    if hw == False:
        return "No hardware"

    return hw.name

@app.route("/api/hardware/<int:hwid>/remove/")
def remove_hardware(hwid):
    hw = Hardware.getHardwareByID(hwid)

    if hw == False:
        return "No hardware"

    hw.removeFromDatabase()

@app.route("/api/hardware/<int:hwid>/update")
def update_hardware(hwid):
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


try:
    e = Employee('tester', hashlib.sha256('tester').hexdigest())
    e.insertIntoDatabase()
except:
    print('>>> User already into database')

    
app.secret_key = 'GALLIFREYFALLSNOMORE'

app.run()
