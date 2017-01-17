""" Sistema de controle para a IPM (International Punishment Machines 

	Criado por Arthur Mendes

"""

from flask import Flask, url_for
from models.Database import Database

app = Flask("ipm-control")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
Database.createDatabase(app)

@app.route("/")
def show_index():
    return "index"


app.run()
