# Importing the necessary libraries for the model to run.
# Importing the Model and DataCollector classes from the mesa module.
from mesa import Model, DataCollector
# Importing the MultiGrid class from the mesa.space module.
from mesa.space import MultiGrid
# Importing the SimultaneousActivation class from the mesa.time module.
from mesa.time import SimultaneousActivation
# Importing the math library.
import math
# Importing all the functions from the agents.py file.
from agents import *

# ----------------------------------------------------------
# Actividad Integradora model.py
#
# Date: 21-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------


def compute_agent_moves(model):
    """
    It counts the number of moves made by all Roomba agents in the model
    :param model: the model object
    :return: The number of movements of all the Roomba agents.
    """
    movements = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Robot_Agent):
            movements += agent.moves
    return movements


def tiempo(model):
    """
    It returns the current time of the model
    :param model: the model object
    :return: The time of the model.
    """
    return model.schedule.time


class IntegradoraModel(Model):
    def __init__(self, width, height, NAgents):
        """
        It creates a grid, places the agents in the grid, and creates a
        data collector. :param width: width of the grid
        :param height: The height of the grid
        :param NAgents: number of boxes
        """
        # Creating a grid of size width x height.
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.picked_boxes = {}
        self.reserved_cells = []
        self.initial_boxes = {}
        self.reserved_boxes = []
        self.pallets = {}
        self.objective_boxes = []
        self.objective_boxes_added = []
        self.picked_objective_boxes = []
        num_pallets = math.ceil(NAgents / 5)
        corners = [(0, 0), (0, height-1), (width-1, height-1), (width-1, 0)]
        # Creating a dictionary of pallets.
        for count in range(num_pallets):
            if count < 4:
                self.pallets[corners[count]] = 0
            else:
                if count % 2 == 0:
                    corner = self.random.choice([0, 2])
                    y = corners[corner][1]
                    while True:
                        x = self.random.randrange(2, self.grid.width-3)
                        if (x, y) not in self.pallets:
                            self.pallets[(x, y)] = 0
                            break
                else:
                    corner = self.random.choice([1, 3])
                    x = corners[corner][0]
                    while True:
                        y = self.random.randrange(2, self.grid.height-3)
                        if (x, y) not in self.pallets:
                            self.pallets[(x, y)] = 0
                            break
        unique_id = 0
        occupied_cells = {}
        # Creating 5 robots and placing them in the grid.
        for _ in range(5):
            robot = Robot_Agent((unique_id), self)
            while True:
                x = self.random.randrange(2, self.grid.width-3)
                y = self.random.randrange(2, self.grid.height-3)
                if (x, y) not in occupied_cells and \
                        (x, y) not in self.pallets:
                    self.grid.place_agent(robot, (x, y))
                    self.schedule.add(robot)
                    occupied_cells[(x, y)] = True
                    break
            unique_id += 1
        # Creating the boxes and placing them in the grid.
        for _ in range(NAgents):
            box = Caja((unique_id), self)
            while True:
                x = self.random.randrange(2, self.grid.width-3)
                y = self.random.randrange(2, self.grid.height-3)
                if (x, y) not in occupied_cells and \
                        (x, y) not in self.pallets:
                    self.grid.place_agent(box, (x, y))
                    self.schedule.add(box)
                    occupied_cells[(x, y)] = True
                    break
            unique_id += 1
        self.datacollector = DataCollector(
            agent_reporters={"Moves": "moves"})
        self.time = 0
        self.datacollector = DataCollector(
            model_reporters={"Movimientos": compute_agent_moves,
                             "Tiempo": tiempo})

    def step(self):
        """
        The function "step" is called every time the model is run.
        It checks if the stack is full, and if it is, it stops the model.
        If it isn't, it adds one to the time variable and collects the data
        :return: The number of agents in the model.
        """
        if llenar_stack(self):
            return
        else:
            self.time += 1
        self.datacollector.collect(self)
        self.schedule.step()
