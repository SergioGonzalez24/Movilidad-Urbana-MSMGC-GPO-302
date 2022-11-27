from agent import *
from model import TrafficModel
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return

    portrayal = {"Shape": "rect",
                 "Filled": "true", 
                 "w": 1, "h": 1, 
                 "Layer": 0}

    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["text"] = agent.pos
        portrayal["text_color"] = "black"
        portrayal["text_size"] = 1
        
    if (isinstance(agent, Destination)):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0
        portrayal["text"] = agent.pos
        portrayal["text_color"] = "black"

    if (isinstance(agent, Traffic_Light)):
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 0


    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0


    if (isinstance(agent, Car)):
        portrayal["Color"] = "#0000FF"
        portrayal["Layer"] = 1
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["text"] = agent.unique_id
        portrayal["text_color"] = "black"

    return portrayal

width = 0
height = 0

with open('2022_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

model_params = {"N":2, "lightSpan": 10}

grid = CanvasGrid(agent_portrayal, width, height, 900, 900)

server = ModularServer(TrafficModel, [grid], "Traffic Base", model_params)
                       
server.port = 8521 # The default
server.launch()
