# Importing the Flask class from the flask module.
from flask import Flask, request, jsonify
# Importing all the classes from the agents.py file.
from agents import *
# Importing all the classes from the model.py file.
from model import *

# ----------------------------------------------------------
# Actividad Integradora server_flask.py
#
# Date: 21-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------


# The number of robots in the model.
NAgents = 1
# The width of the grid.
width = 28
# The height of the grid.
height = 28
# A global variable that is used to store the model.
integradoraModel = None
# A global variable that keeps track of the current step of the model.
currentStep = 0
# Creating a Flask object with the name "Actividad Integradora".
app = Flask("Actividad Integradora")


# A decorator that is used to bind a function to a URL.
@app.route('/', methods=['xPOST', 'GET'])
def helloWorld():
    """
    If the request method is GET, return a JSON object with a message key and
    a value of "Connection with server was successful!"
    :return: A JSON object with a message.
    """
    if request.method == 'GET':
        return jsonify({"message": "Connection with server was successful!"})


@app.route('/init', methods=['POST', 'GET'])
# A decorator that is used to bind a function to a URL.
def initModel():
    """
    It receives the parameters from the frontend, and initiates the model
    with those parameters :return: a json object with the message
    "Parameters received, model initiated.
    """
    global currentStep, integradoraModel, NAgents, width, height
    if request.method == 'POST':
        NAgents = int(request.form.get('NAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0
        integradoraModel = IntegradoraModel(width, height, NAgents)
        return jsonify({"message": "Parameters received, model initiated."})


# A decorator that is used to bind a function to a URL.
@app.route('/getAgentes', methods=['GET'])
def getRobots():
    """
    It returns a JSON object with the positions of all the robots in the grid
    :return: A JSON object with the positions of the robots.
    """
    global integradoraModel
    if request.method == 'GET':
        robotPositions = [{"id": str(obj.unique_id),
                           "x": x, "y": 0, "z": z,
                           "hasBox": obj.has_box}
                          for (a, x, z) in integradoraModel.grid.coord_iter()
                          for obj in a if isinstance(obj, Robot_Agent)]
        return jsonify({'positions': robotPositions})


# A decorator that is used to bind a function to a URL.
@app.route('/getCajas', methods=['GET'])
def getBoxes():
    """
    It returns a JSON object with the positions of all the boxes in the grid
    :return: A list of dictionaries, each dictionary contains the id, x, y, z
    and picked_up status of a box.
    """
    global integradoraModel
    if request.method == 'GET':
        boxesPositions = [{"id": str(obj.unique_id),
                           "x": x, "y": 0, "z": z,
                           "picked_up": obj.picked_up}
                          for (a, x, z) in integradoraModel.grid.coord_iter()
                          for obj in a if isinstance(obj, Caja)]
        return jsonify({'positions': boxesPositions})


# A decorator that is used to bind a function to a URL.
@app.route('/getTarimas', methods=['GET'])
def getTarimas():
    """
    It returns a JSON object with the positions of the pallets in the model
    :return: A JSON object with the positions of the pallets.
    """
    global integradoraModel
    if request.method == 'GET':
        palletsPositionsValues = []
        count = 0
        for x, y in integradoraModel.pallets.keys():
            palletsPositionsValues.append({"id": count,
                                           "x": x,
                                           "y": 0,
                                           "z": y,
                                           "value": integradoraModel.pallets[
                                            (x, y)]})
            count += 1
        return jsonify({'positions': palletsPositionsValues})


# A decorator that is used to bind a function to a URL.
@app.route('/update', methods=['GET'])
def updateModel():
    """
    It updates the model to the next step and returns a message with the
    current step :return: a json object with the message and the current step.
    """
    global currentStep, integradoraModel
    if request.method == 'GET':
        integradoraModel.step()
        currentStep += 1
        return jsonify({'message': f'Model updated to step {currentStep}.',
                        'currentStep': currentStep})


# Running the app on the localhost on port 8585.
if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)
