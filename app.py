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
    

app.run()
