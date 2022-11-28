from model import TrafficModel
from agent import *
from flask import Flask, request, jsonify
import os

# This parameters will be providen by Unity
carsNumber = 20
lightSpan = 10

def sortByID(e):
    return e['id']

# Internal parameters
trafficModel = None
port = int(os.getenv("PORT", 8000))

app = Flask("Traffic Base")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global trafficModel, carsNumer, lightSpan

    if request.method == "POST":
        carsNumber = int(request.form.get("carsNumber"))
        lightSpan = int(request.form.get("lightSpan"))

        print(request.form)
        trafficModel = TrafficModel(carsNumber, lightSpan)

        return jsonify({"message": "Parameters received, model initiated."})

@app.route('/getCars', methods=['GET'])
def getCars():
    global trafficModel

    if request.method == "GET":
        carPositions = [{"x":x,"y":0,"z":z,"w":e.isStop,"id":e.unique_id} for (a,x,z) in trafficModel.grid.coord_iter() for e in a if isinstance(e, Car)]

        carPositions.sort(key=lambda x: x["id"])
        return jsonify({"positions": carPositions})
    
@app.route('/update', methods=['GET'])
def updateModel():
    global trafficModel

    if request.method == "GET":
        trafficModel.step()
        return jsonify({"message": "Model Updated!"})
    
    
@app.route("/getSemaforos", methods=['GET'])
def update_traffic_light():
    states = [{"x":x, "y":1, "z":z,"state":b.state, "id":b.unique_id} for (a, x, z) in carModel.grid.coord_iter() for b in a if isinstance(b, Traffic_Light)]
    states.sort(key=sortByID)
    sorted_points = [{"x": i["x"], "y":1, "z":i["z"]} for i in states]
    sorted_states = [i["state"] for i in states]
    print(sorted_states)
    return jsonify({"positions": sorted_points, "states": sorted_states})


if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=True)
