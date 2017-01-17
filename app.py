""" Sistema de controle para a IPM (International Punishment Machines 

	Criado por Arthur Mendes

"""

from flask import Flask, url_for
app = Flask("ipm-control")

@app.route("/")
def show_index():
	return "index"


app.run()
