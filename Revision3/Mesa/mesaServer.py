from agent import *
from model import TrafficModel
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return

    portrayal = {"Shape": "rect",
                 "Filled": "true", 
                 "w": 1, "h": 1}

    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["text"] = agent.pos
        # portrayal["text"] = agent.direction
        portrayal["text_color"] = "black"

        
    if (isinstance(agent, Destination)):
        portrayal["Shape"] = "./Revision3/Mesa/img/parking.png"
        portrayal["Layer"] = 0
        portrayal["text"] = agent.pos
        portrayal["text_color"] = "black"

    if (isinstance(agent, Traffic_Light)):
        portrayal["Shape"] = "./Revision3/Mesa/img/rojo.png" if not agent.state else "./Revision3/Mesa/img/verde.png"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        


    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0


    if (isinstance(agent, Car)):
        portrayal["Shape"] = "./Revision3/Mesa/img/cuchao.png"
        portrayal["Layer"] = 1

        portrayal["text"] = agent.unique_id
        
    return portrayal

width = 0
height = 0

with open('./Revision3/Mesa/Docs/2022_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

model_params = {"N":20, "lightSpan": 10}

grid = CanvasGrid(agent_portrayal, width, height, 900, 900)

server = ModularServer(TrafficModel, [grid], "Traffic Base", model_params)
                       
server.port = 8521 
server.launch()
