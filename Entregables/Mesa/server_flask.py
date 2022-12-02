# Importing the necessary libraries.
from model import MapaModel
from agent import *
from flask import Flask, request, jsonify
import os

# ----------------------------------------------------------
# - Entrega Final --- model.py
#
# Date: 02-Dec-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------

# Defining the variables that will be used in the code.
obtenerMcqueens = 20
tiempo = 10


def sortByID(e):
    """
    It returns the value of the 'id' key in the dictionary
    :param e: The element in the list
    :return: The ID of the element.
    """
    return e['id']


# Creating a Flask app.
trafficModel = None
port = int(os.getenv("PORT", 8000))

app = Flask("Traffic Base")


@app.route('/init', methods=['POST', 'GET'])
def initModel():
    """
    It takes the values from the form and uses them to create a new instance
    of the TrafficModel class
    :return: a JSON object with a message.
    """
    global trafficModel, obtenerMcqueens, tiempo

    if request.method == "POST":
        obtenerMcqueens = int(request.form.get("Mcqueens"))
        tiempo = int(request.form.get("tiempo"))

        print(request.form)
        trafficModel = MapaModel(obtenerMcqueens, tiempo)

        return jsonify({"message": "Parameters received, model initiated."})


# A decorator that is used to define the route of the function.
@app.route('/getMcqueen', methods=['GET'])
def getCars():
    """
    For each car in the grid, get the x, y, z coordinates and whether or
    not the car is stopped
    :return: A list of dictionaries.
    """
    global trafficModel

    if request.method == "GET":
        carPositions = [{"x":x,"y":0,"z":z,"w":e.detenido,"id":e.unique_id} for (a,x,z) in trafficModel.grid.coord_iter() for e in a if isinstance(e, Mcqueen)]

        carPositions.sort(key=lambda x: x["id"])
        return jsonify({"positions": carPositions})


# A decorator that is used to define the route of the function.
@app.route('/update', methods=['GET'])
def updateModel():
    """
    The function is called when the user clicks the "Update Model" button
    on the web page. The function updates the model by calling the step()
    function of the trafficModel object.
    The function returns a JSON object with a message.
    The message is displayed on the web page.
    :return: a JSON object with a message.
    """
    if request.method == "GET":
        trafficModel.step()
        return jsonify({"message": "Model Updated!"})


# A way to run the app only if the file is run directly.
if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=True)