""" Sistema de controle para a IPM (International Punishment Machines 

	Criado por Arthur Mendes

"""

from flask import Flask, url_for, request, abort
from models.Database import Database, installDatabase

app = Flask("ipm-control")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

Database.createDatabase(app)
installDatabase(Database.database.db)

from Cliente import Client
from Hardware import Hardware

@app.route("/")
def show_index():
    return "index"

# Client api routes
@app.route("/api/client/add")
def add_client():
    if not 'name' in request.args:
        abort(400)

    cli = Client(request.args.get('name'))
    cli.addIntoDatabase()
    return str(cli.ID)

@app.route("/api/client/get/<int:clientid>")
def get_client(clientid):
    cli = Client.getClientFromID(clientid)

    if cli == False:
        return 'No client'
            
    return cli.name

@app.route("/api/client/remove/<int:clientid>")
def remove_client(clientid):
    cli = Client.getClientFromID(clientid)

    if cli == False:
        return 'No client'

    cli.removeFromDatabase()
    return "Client %s removed successfully" % cli.name

@app.route("/api/client/update/<int:clientid>/")
def update_client(clientid):
    cli = Client.getClientFromID(clientid)

    if cli == False:
        return 'No client'

    if not 'name' in request.args:
        abort(400)
        
    cli.name = request.args.get('name')
    cli.updateIntoDatabase()
    return "Client {} is now {}".format(str(clientid), cli.name)


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
    
    



app.run()
