
# -----------------------------------------------------------
# - Entrega Final -- mesaServer.py
#
# Date: 02-Dec-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Ricardo Ramírez Condado - A01379299
# -----------------------------------------------------------

from agent import *
from model import MapaModel
from model import tiempo, compute_agent_moves
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


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
        portrayal["text_color"] = "black"


    if (isinstance(agent, Destination)):
        portrayal["Shape"] = "./Entregables/Mesa/img/parking.png"
        portrayal["Layer"] = 0
        portrayal["text"] = agent.pos
        portrayal["text_color"] = "black"

    if (isinstance(agent, Semaforo)):
        # Para su visualizacion correcta, revisar que sea la ruta correcta de las imágenes.
        portrayal["Shape"] = "./Entregables/Mesa/img/rojo.png" if not agent.state else "./Entregables/Mesa/img/verde.png"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["text"] = agent.unique_id

    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0

    if (isinstance(agent, Mcqueen)):
        # Para su visualizacion correcta, revisar que sea la ruta correcta de las imágenes.
        portrayal["Shape"] = "./Entregables/Mesa/img/cuchao.png"
        portrayal["Layer"] = 1

        portrayal["text"] = agent.unique_id

    return portrayal


# Setting the width and height of the grid to 0.
width = 0
height = 0

# Reading the file and getting the width and height of the grid.
with open('./Entregables/Mesa/Docs/2022_base.txt') as baseFile: # Para su funcionamiento correcto, revisar que sea la ruta correcta del archivo a leer.
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

# Setting the number of agents and the time of the simulation.

# time == timpo de estado de semaforo
model_params = {"N": 20, "tiempo": 8}

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
