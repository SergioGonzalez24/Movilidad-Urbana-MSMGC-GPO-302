# Importing the Agent class from the mesa module.
# The above code is importing the random and math modules.
import random
import math
from mesa import Agent

# ----------------------------------------------------------
# Actividad Integradora agents.py
#
# Date: 21-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------
# The Caja class is a subclass of the Agent class. It has a constructor that
# initializes the agent's type, color, next color, not_move, agent_details,
# next_state, picked_up, and moves attributes. It also has a recogida() method
# that returns True if the agent's position is in the list of initial
# boxes, otherwise it returns False. It has an agarrar() method that deletes
# the box from the initial_boxes dictionary and adds it to the picked_boxes
# dictionary. It also changes the agent's next_state to the box's next_state.
# It has a levantada() method that sets the object's picked_up attribute to
# False and sets the next_state  attribute to the object's current position.
# It has a mueve() method that sets the
# agent's picked_up attribute to True, increments the moves attribute by
# 1, and sets the next_state attribute to the agent's current position. It


class Caja(Agent):
    def __init__(self, unique_id, model):
        """
        The function takes in a unique_id and a model, and then sets the type
        of the agent to box, the color of the agent to 0, the next color of
        the agent to 0,
        the not_move variable to False, the
        agent_details to None, the next_state to None, the picked_up variable
        to False, and the moves
        variable to 0.
        :param unique_id: The unique identifier for the agent
        :param model: The model that the agent is in
        """
        super().__init__(unique_id, model)
        self.type = 'box'
        self.color = 0
        self.next_color = 0
        self.not_move = False
        self.agent_details = None
        self.next_state = None
        self.picked_up = False
        self.moves = 0

    def recogida(self):
        """
        If the position of the agent is in the list of initial boxes,
        then return True, otherwise return False
        :return: The position of the agent.
        """
        if self.pos in self.model.initial_boxes:
            return True
        else:
            return False

    def agarrar(self):
        """
        The function agarrar() is called when the agent is in the same
        position as a box. The function deletes the box from the
        initial_boxes dictionary and adds it to the picked_boxes dictionary.
        The function also changes the agent's next_state to the box's
        next_state
        """
        self.agent_details = self.model.initial_boxes[self.pos]
        del self.model.initial_boxes[self.pos]
        self.model.picked_boxes[self.agent_details[0]] = \
            self.agent_details[-1]
        self.next_state = self.agent_details[-1]
        self.picked_up = True

    def levantada(self):
        """
        The function is called when the player picks up the object.
        It sets the object's picked_up attribute to False and sets the
        next_state attribute to the object's current position.
        """
        self.picked_up = False
        self.next_state = self.pos

    def mueve(self):
        """
        The function mueve() is called when the agent is picked up by the
        robot. It sets the agent's picked_up attribute to True, increments
        the moves attribute by 1, and sets the next_state attribute
        to the agent's current position
        """
        self.picked_up = True
        self.moves += 1
        self.next_state = self.model.picked_boxes[
            self.agent_details[0]]

    def step(self):
        """
        If the agent is not moving, it checks if it has an agent_details
        object, if it does, it moves, if it doesn't, it checks if it can pick
        up an object, if it can, it picks it up, if it can't, it does
        nothing
        """
        if not self.not_move:
            if self.agent_details is None:
                if self.recogida():
                    self.agarrar()
                else:
                    self.levantada()
            else:
                self.mueve()
                if self.next_state in self.model.pallets:
                    self.picked_up = False
                    self.not_move = True
        else:
            self.picked_up = False
            self.next_state = self.pos
        if self.picked_up:
            self.next_color = 3
        else:
            self.next_color = 0

    def advance(self):
        """
        The function takes the current state of the agent and the next state
        of the agent and moves the agent from the current state to the next
        state
        """
        self.color = self.next_color
        self.model.grid.move_agent(self, self.next_state)


# The class Robot_Agent is a
# subclass of the Agent class. It has a constructor that initializes the
# attributes of the class Robot_Agent. It has a function neighbors() that
# returns a list of lists, each of which contains the type of object in a cell
# and the cell's coordinates. It has a function puede_soltar() that returns the
# position of the pallet if it is possible to drop the pallet, otherwise it
# returns False. It has a function soltar_caja() that is called when the agent
# has a box and is in the same cell as the dropoff point. It has a function
# tarima_cercana() that takes a list of coordinates (neighbor) and returns the
# closest pallet to the last coordinate in the list. It has a function
# mueve_caja() that returns
class Robot_Agent(Agent):
    def __init__(self, unique_id, model):
        """
        The function __init__ is a constructor that initializes the attributes
        of the class RobotAgent :param unique_id: The unique ID of the agent
        :param model: The model that the agent is in
        """
        super().__init__(unique_id, model)
        self.type = 'robotagent'
        self.color = 1
        self.next_color = None
        self.has_box = False
        self.next_state = None
        self.objective_box = None
        self.moves = 0

    def neighbors(self):
        """
        It returns a list of lists, each of which contains the type of object
        in a cell and the cell's coordinates :return: A list of lists.
        Each list contains the type of object in the cell, the object itself,
        and the position of the cell.
        """
        contenido = []
        neighbors = self.model.grid.get_neighborhood(
                self.pos,
                moore=False,
                include_center=False)
        for neighbor in neighbors:
            if neighbor in self.model.pallets:
                contenido.append(['pallet', self.model.pallets[neighbor],
                                  neighbor])
            else:
                content = self.model.grid.get_cell_list_contents(neighbor)
                if content:
                    robot, box = False, False
                    for object in content:
                        if object.type == 'robot':
                            robot = True
                        elif object.type == 'box':
                            box = True
                    if robot and box:
                        contenido.append(['robot-with-box', neighbor])
                    elif box:
                        contenido.append(['box', neighbor])
                    else:
                        contenido.append(['robot', neighbor])
                else:
                    contenido.append(['empty', neighbor])
        return contenido

    def puede_soltar(self, neighbors_content):
        """
        If there is a pallet in the neighborhood, and it has less than 5 items
        on it, then return the pallet's id. Otherwise, return False
        :param neighbors_content: a list of tuples, each tuple is a neighbor
        of the agent. The tuple contains the type of the neighbor, the number
        of items in the neighbor, and the id of the neighbor :return:
        the position of the pallet if it is possible
        to drop the pallet, otherwise it returns False.
        """
        for neighbor in neighbors_content:
            if neighbor[0] == 'pallet':
                if neighbor[1] < 5:
                    return neighbor[-1]
        return False

    def soltar_caja(self, coordinar):
        """
        The function soltar_caja() is called when the agent has a box and is in
        the same cell as the dropoff point. The function adds one to the
        pallet in the dropoff point, sets the next state to the current state,
        sets the agent's has_box attribute to False,
        and adds the agent's unique_id to the model's picked_boxes dictionary
        :param coordinar: the coordinate of the pallet
        """
        self.model.pallets[coordinar] += 1
        self.next_state = self.pos
        self.has_box = False
        self.model.picked_boxes[self.unique_id] = coordinar

    def tarima_cercana(self, neighbor):
        """
        It takes a list of coordinates (neighbor) and returns the closest
        pallet to the last coordinate in
        the list :param neighbor: a list of coordinates that represent
        the path taken by the agent:return: the closest pallet to the
        last position of the neighbor.
        """
        x1, y1 = neighbor[-1]
        min_distance = float('inf')
        tarima_cercana = 0
        for key in self.model.pallets:
            if self.model.pallets[key] < 5:
                distance = math.sqrt(((key[0] - x1)**2) + ((key[1] - y1)**2))
                if distance < min_distance:
                    tarima_cercana = [key, neighbor[-1], distance]
                    min_distance = distance
        if tarima_cercana:
            return tarima_cercana
        else:
            return False

    def mueve_caja(self, neighbors_content):
        """
        The function returns the position of the closest empty cell to
        the agent, if there is one, and if it is not reserved by another agent
        :param neighbors_content: list of tuples, each tuple contains
        the content of a cell and its position :return:
        The next state of the agent.
        """
        min_distance = float('inf')
        graph = []
        for neighbor in neighbors_content:
            if neighbor[0] == 'empty' and neighbor[-1] not in \
                    self.model.reserved_cells:
                distance = self.tarima_cercana(neighbor)
                if distance:
                    if distance[-1] < min_distance:
                        min_distance = distance[-1]
                        graph = distance
        if graph:
            self.model.reserved_cells.append(graph[1])
            self.next_state = graph[1]
            self.model.picked_boxes[self.unique_id] = self.next_state
            return graph[1]
        else:
            self.next_state = self.pos
            self.model.picked_boxes[self.unique_id] = self.next_state
            return self.pos

    def hay_caja(self, neighbors_content):
        """
        If there is a box in the neighborhood, then add it to the list of
        reserved boxes and return the box. Otherwise, return False
        :param neighbors_content: list of tuples, each tuple is a cell content
        :return: the box that is in the same cell as the agent.
        """
        for neighbor in neighbors_content:
            if neighbor[0] == 'box' and neighbor[-1] not \
                    in self.model.reserved_boxes:
                self.model.reserved_boxes.append(neighbor[-1])
                return neighbor
        return False

    def mover(self, neighbors_content):
        """
        If there is an empty cell in the neighborhood, move to it
        :param neighbors_content: a list of tuples,
        each tuple contains the content of a cell and its position
        :return: a boolean value.
        """
        random.shuffle(neighbors_content)
        for neighbor in neighbors_content:
            if neighbor[0] == 'empty' and neighbor[-1] not in \
                    self.model.reserved_cells:
                self.model.reserved_cells.append(neighbor[-1])
                self.next_state = neighbor[-1]
                self.moves += 1
                return True
        self.next_state = self.pos
        return False

    def recoger(self, box):
        """
        The agent picks up a box and adds it to the list of picked up boxes
        :param box: the box that the agent is picking up
        """
        self.model.picked_objective_boxes.append(box[-1])
        self.model.initial_boxes[box[-1]] = [self.unique_id, self.pos]
        self.next_state = self.pos
        self.has_box = True

    def comunicar(self, box_position):
        """
        The function comunicar() is called when a box is added to
        the objective_boxes list :param box_position: the position of
        the box that the agent is currently on
        """
        if box_position not in self.model.objective_boxes_added:
            self.model.objective_boxes.append(box_position)
            self.model.objective_boxes_added.append(box_position)

    def caja_cerca(self, neighbor):
        """
        It calculates the distance between the objective box and the last box
        in the neighbor list.
        :param neighbor: a list of tuples, each tuple is a coordinate
        :return: The distance between the last point in the neighbor list
        and the objective box.
        """
        x1, y1 = neighbor[-1]
        distancia = math.sqrt(((self.objective_box[0] - x1) ** 2) +
                              ((self.objective_box[1] - y1) ** 2))
        return distancia

    def mover_a_caja(self, neighbors_content):
        """
        If there is an empty cell next to the agent, and that cell is not
        already reserved, then the agent
        will move to that cell
        :param neighbors_content: a list of tuples, each tuple contains the
        content of a cell and its
        position
        :return: The next state of the agent.
        """
        min_distance = float('inf')
        shortest_path = self.pos
        for neighbor in neighbors_content:
            if neighbor[0] == 'empty' and neighbor[-1] not in \
                    self.model.reserved_cells:
                distance = self.caja_cerca(neighbor)
                if distance < min_distance:
                    min_distance = distance
                    shortest_path = neighbor[-1]
        if shortest_path:
            self.moves += 1
            self.model.reserved_cells.append(shortest_path)
            self.next_state = shortest_path
            return shortest_path
        else:
            self.next_state = self.pos
            return self.pos

    def step(self):
        """
        If the agent has a box, it will try to drop it, if it can't, it will
        try to move it, if it can't, it
        will try to communicate with other agents. If the agent doesn't have a
        box, it will try to pick one
        up, if it can't, it will try to move to the box, if it can't, it will
        try to move
        """
        if self.objective_box in self.model.picked_objective_boxes:
            self.objective_box = None
        neighbors_content = self.neighbors()
        is_there_a_box = self.hay_caja(neighbors_content)
        if self.has_box:
            if is_there_a_box:
                self.comunicar(is_there_a_box[-1])
            can_drop_it = self.puede_soltar(neighbors_content)
            if can_drop_it:
                self.soltar_caja(can_drop_it)
            else:
                self.mueve_caja(neighbors_content)
        else:
            if is_there_a_box:
                if self.objective_box:
                    if self.objective_box not in \
                            self.model.picked_objective_boxes:
                        self.model.objective_boxes.append(self.objective_box)
                    self.objective_box = None
                self.recoger(is_there_a_box)
            else:
                if self.model.objective_boxes and not self.objective_box:
                    self.objective_box = self.model.objective_boxes.pop()
                    self.mover_a_caja(neighbors_content)
                elif self.objective_box:
                    self.mover_a_caja(neighbors_content)
                else:
                    self.mover(neighbors_content)
        if self.has_box:
            self.next_color = 2
        else:
            self.next_color = 1

    def advance(self):
        """
        The function takes the current state of the agent, and the next state
        of the agent, and moves the
        agent from the current state to the next state
        """
        self.model.reserved_cells = []
        self.model.reserved_boxes = []
        self.color = self.next_color
        self.model.grid.move_agent(self, self.next_state)


def llenar_stack(model):
    """
    If any of the values in the pallets dictionary are less than 5, return
    False. Otherwise, return True
    :param model: the model object
    :return: a boolean value.
    """
    for value in model.pallets.values():
        if value < 5:
            return False
    return True
