# Importing the necessary libraries.
from model import TrafficModel
from agent import *
from flask import Flask, request, jsonify
import os


# Defining the variables that will be used in the code.
carsNumber = 20
lightSpan = 10
carModel = None


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
    global trafficModel, carsNumer, lightSpan

    if request.method == "POST":
        carsNumber = int(request.form.get("carsNumber"))
        lightSpan = int(request.form.get("lightSpan"))

        print(request.form)
        trafficModel = TrafficModel(carsNumber, lightSpan)

        return jsonify({"message": "Parameters received, model initiated."})


# A decorator that is used to define the route of the function.
@app.route('/getCars', methods=['GET'])
def getCars():
    """
    For each car in the grid, get the x, y, z coordinates and whether or
    not the car is stopped
    :return: A list of dictionaries.
    """
    global trafficModel

    if request.method == "GET":
        carPositions = [{"x":x,"y":0,"z":z,"w":e.isStop,"id":e.unique_id} for (a,x,z) in trafficModel.grid.coord_iter() for e in a if isinstance(e, Car)]

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
    global trafficModel

    if request.method == "GET":
        trafficModel.step()
        return jsonify({"message": "Model Updated!"})


# A decorator that is used to define the route of the function.
@app.route("/getSemaforos", methods=['GET'])
def update_traffic_light():
    """
    It takes the traffic light objects from the model, sorts them by their
    unique ID, and returns a JSON
    object containing the positions and states of the traffic lights
    :return: A JSON object with two keys: positions and states.
    """
    states = [{"x":x, "y":1, "z":z,"state":b.state, "id":b.unique_id} for (a, x, z) in trafficModel.grid.coord_iter() for b in a if isinstance(b, Traffic_Light)]
    states.sort(key=sortByID)
    sorted_points = [{"x": i["x"], "y":1, "z":i["z"]} for i in states]
    sorted_states = [i["state"] for i in states]
    print(sorted_states)
    return jsonify({"positions": sorted_points, "states": sorted_states})


# A way to run the app only if the file is run directly.
if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=True)
