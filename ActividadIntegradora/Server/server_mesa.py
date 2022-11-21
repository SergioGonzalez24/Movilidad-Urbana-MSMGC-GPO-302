# Importing all the classes from the agents.py file.
from agents import *
# Importing all the classes from the model.py file.
from model import *
# Importing the CanvasGrid class from the mesa.visualization.modules module.
from mesa.visualization.modules import CanvasGrid
# Importing the ModularServer class from the
# mesa.visualization.ModularVisualization module.
from mesa.visualization.ModularVisualization import ModularServer
# Importing the ChartModule class from the mesa.visualization.modules module.
from mesa.visualization.modules import ChartModule

# ----------------------------------------------------------
# Actividad Integradora server_mesa.py
#
# Date: 21-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------


def agent_portrayal(agent):
    """
    If the agent is red, it's a circle, if it's yellow, it's a circle,
    if it's green, it's a small circle, and if it's blue, it's a small circle
    :param agent: the agent object
    :return: The portrayal of the agent.
    """
    # Creating a dictionary with the properties of the agent.
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    # Checking if the agent's color is 1, if it is, it will set the color
    # to red and the layer to 0.
    if agent.color == 1:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    # Setting the color of the agent to yellow and the layer to 0.
    elif agent.color == 2:
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
    # Setting the color of the agent to green and the layer to 1.
    elif agent.color == 3:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.1
    # Setting the color of the agent to blue and the layer to 1.
    else:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.1
    # Returning the portrayal of the agent.
    return portrayal


# Creating a grid of 15x15 cells, with 30 agents and a size of 750x750 pixels.
width = 15
height = 15
Agentes = 30
grid = CanvasGrid(agent_portrayal, width, height, 750, 750)
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
# Creating a server that will run the IntegradoraModel with the grid and the
# number of agents.
server = ModularServer(IntegradoraModel,
                       [grid, tiempo, compute_agent_moves],
                       "Actividad Integradora",
                       {"width": width, "height": height, "NAgents": Agentes})
# Setting the port to 8521 and launching the server.
server.port = 8521
server.launch()
