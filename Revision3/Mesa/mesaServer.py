# Importing the modules that are needed to run the program.
from agent import *
from model import MapaModel
from model import tiempo, compute_agent_moves
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
# mesa.visualization.ModularVisualization module.
from mesa.visualization.ModularVisualization import ModularServer
# Importing the ChartModule class from the mesa.visualization.modules module.
from mesa.visualization.modules import ChartModule

# ----------------------------------------------------------
# Revisión 3 - 60% -- mesaServer.py
#
# Date: 28-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------


def agent_portrayal(agent):
    """
    If the agent is a Ruta66, then it's a grey rectangle with the agent's position as text. If the agent
    is a Destination, then it's a parking lot image with the agent's position as text. If the agent is a
    Semaforo, then it's a red or green image depending on the agent's state. If the agent is an
    Obstacle, then it's a blue rectangle. If the agent is a Mcqueen, then it's a cuchao image with the
    agent's unique_id as text
    
    :param agent: the agent to be portrayed
    :return: The portrayal of the agent.
    """
    if agent is None: return

    portrayal = {"Shape": "rect",
                 "Filled": "true", 
                 "w": 1, "h": 1}

    if (isinstance(agent, Ruta66)):
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

    if (isinstance(agent, Semaforo)):
        portrayal["Shape"] = "./Revision3/Mesa/img/rojo.png" if not agent.state else "./Revision3/Mesa/img/verde.png"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0

    if (isinstance(agent, Mcqueen)):
        portrayal["Shape"] = "./Revision3/Mesa/img/cuchao.png"
        portrayal["Layer"] = 1

        portrayal["text"] = agent.unique_id

    return portrayal


# Setting the width and height of the grid to 0.
width = 0
height = 0

# Reading the file and getting the width and height of the grid.
with open('./Revision3/Mesa/Docs/2022_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

# Setting the number of agents and the time of the simulation.
model_params = {"N": 20, "tiempo": 10}

# Creating a grid with the width and height of the grid, and the width and height of the grid.
grid = CanvasGrid(agent_portrayal, width, height, 700, 700)

# Creating a chart that will be displayed in the Mesa server.
compute_agent_moves = ChartModule(
        [{
            "Label": "Movimientos",
            "Color": "Green",
        }],
        data_collector_name='datacollector'
            )
tiempo = ChartModule(
        [{
            "Label": "Tiempo",
            "Color": "Purple"
        }],
        data_collector_name='datacollector'
            )

# Creating a server that will run the model MapaModel, with the grid, tiempo 
# and compute_agent_moves
# charts, with the name "Traffic Base" and with the model_params parameters.
server = ModularServer(MapaModel, [grid, tiempo, compute_agent_moves],
                       "Traffic Base", model_params)
# Setting the port to 8521 and launching the server.
server.port = 8521
server.launch()
