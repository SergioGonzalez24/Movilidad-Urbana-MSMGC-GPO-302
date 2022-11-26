from agent import *
from model import TrafficModel
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return

    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "w": 1,
                 "h": 1}

    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
    
    if (isinstance(agent, Destination)):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if (isinstance(agent, Traffic_Light)):
        portrayal["Shape"] = "./Revision3/revision3_test/rojo.png" if not agent.state else "./Revision3/revision3_test/verde.png"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Car)):
        portrayal["Shape"] = "./Revision3/revision3_test/cuchao.png" 
        portrayal["Layer"] = 1
        

    return portrayal

width = 0
height = 0

with open('./Revision3/revision3_test/base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

model_params = {"N":20, "carAutoRegenerate": 2, "lightSpan": 10}

grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

server = ModularServer(TrafficModel, [grid], "Traffic Base", model_params)
                       
server.port = 8521 # The default
server.launch()
