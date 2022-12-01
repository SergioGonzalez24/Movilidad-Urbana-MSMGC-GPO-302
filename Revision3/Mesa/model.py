# Importing the necessary libraries for the program to run.
from mesa import Model, DataCollector
from agent import Mcqueen
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json
from random import choice, randrange

# -----------------------------------------------------------
# Revisión 3 - 60% -- model.py
#
# Date: 28-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Ricardo Ramírez Condado - A01379299
# -----------------------------------------------------------


def compute_agent_moves(model):
    """
    This function counts the number of moves made by all the 
    Mcqueen agents in the model
    :param model: the model object
    :return: The number of movements of the agent.
    """
    movements = 0
    for agent in model.schedule.agents:
        if isinstance(Mcqueen):
            movements += agent.moves
    return movements


def tiempo(model):
    """
    It returns the current time of the model
    :param model: the model object
    :return: The time of the model.
    """
    return model.schedule.time


class MapaModel(Model):
    def __init__(self, N, tiempo):
        """
        It creates a grid, places agents on the grid, and then runs the model
        for a specified number of
        steps
        :param N: number of agents
        :param tiempo: The time that the simulation will run for
        """
        self.coordenadas_destino = []
        self.ID_Mcqueen = 0
        self.tiempo = tiempo
        self.conductores = 0
        # Loading the dictionary from the json file.
        Diccionario = json.load(open("./Revision3/Mesa/Docs/mapDictionary.json"))
        # Reading the file and creating the grid.
        with open('./Revision3/Mesa/Docs/2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            self.grid = MultiGrid(self.width, self.height, torus = False)
            self.schedule = RandomActivation(self)
            # Iterating through the lines of the file.
            for r, row in enumerate(lines):
                # Iterating through the lines of the file.
                for c, columna in enumerate(row):
                    # Creating a new agent of type Ruta66 and placing it in 
                    # the grid.
                    if columna in ["v", "^", ">", "<"]:
                        agent = Ruta66(f"r{r*self.width+c}", self, Diccionario[columna])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Creating a semaphore agent and placing it in the grid.
                    elif columna in ["S", "s"]:
                        agent = Semaforo(f"tl{r*self.width+c}", self, False if columna == "S" else True, int(Diccionario[columna]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Creating an obstacle agent and placing it in the grid.
                    elif columna == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Creating a destination agent and placing it in the grid.
                    elif columna == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.coordenadas_destino.append((c, self.height - r - 1))
                    # Creating a new agent of type Ruta66 and placing it in the grid.
                    elif columna == '.':
                        agent = Ruta66(f"r{r*self.width+c}", self, Diccionario[columna])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
        # Setting the number of agents and the running state of the model.
        self.num_agents = N
        self.running = True

        # Creating a new Mcqueen agent and placing it in a random position in the grid.
        for i in range(self.num_agents):
            AgenteMcqueen = Mcqueen(self.ID_Mcqueen, self, choice(self.coordenadas_destino))
            inicio = (randrange(0, self.width), randrange(0, self.height))
            contenido = [type(i) for i in self.grid.get_cell_list_contents([inicio])]
            Cruzar = True
            # Checking if the cell is empty and if it is not, it will generate a new random position.
            while Ruta66 not in contenido or Mcqueen in contenido or Cruzar:
                inicio = (randrange(0, self.width), randrange(0, self.height))
                contenido = [type(i) for i in self.grid.get_cell_list_contents([inicio])]
                # Checking if the cell is empty and if it is not, it will generate a new random
                # position.
                if Ruta66 in contenido:
                    Cruzar = self.grid.get_cell_list_contents([inicio])[0].direction == "Omni"
            # Adding a new agent to the grid and to the schedule.
            self.grid.place_agent(AgenteMcqueen, inicio)
            self.schedule.add(AgenteMcqueen)
            self.ID_Mcqueen += 1
            
            # Collecting the data from the model.
            self.datacollector = DataCollector(
                agent_reporters={"Moves": "moves"})
            self.time = 0
            self.datacollector = DataCollector(
                model_reporters={"Movimientos": compute_agent_moves,
                                 "Tiempo": tiempo})

    def step(self):
        """
        It creates a new car agent, places it on the grid, and adds it to the schedule.
        """
        self.schedule.step()
        # Changing the state of the semaphores every `self.tiempo` steps.
        if self.schedule.steps % self.tiempo == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Semaforo):
                        agent.state = not agent.state

        self.conductores = len([agent for agent in self.schedule.agents if isinstance(agent, Mcqueen)])

        # Creating a new Mcqueen agent and placing it in a random position in the grid.
        if (self.conductores < self.num_agents):
            carAgent = Mcqueen(self.ID_Mcqueen, self,
                               choice(self.coordenadas_destino))
            self.grid.place_agent(carAgent, (choice([0, self.width-1]),
                                             choice([0, self.height-1])))
            self.schedule.add(carAgent)
            self.ID_Mcqueen += 1
