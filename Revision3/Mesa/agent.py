from mesa import Agent
from random import *

# -----------------------------------------------------------
# Revisión 3 - 60% -- agent.py
#
# Date: 28-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# -----------------------------------------------------------

class Mcqueen(Agent):
    def __init__(self, uniqueID, model, destPos):
        """
        The function __init__ is a constructor that initializes the class
        :param uniqueID: The unique ID of the car
        :param model: the model that the agent is in
        :param destPos: The destination position of the car
        """
        # Calling the constructor of the parent class.
        super().__init__(uniqueID, model)
        # Used to check if the car is stopped or not.
        self.detenido = False
        # Setting the final destination of the car.
        self.destino = destPos
        # A variable that is used to store the direction of the car.
        self.Direccion = ""
        # A list of lists that stores the coordinates of the car and 
        # the coordinates of the cells that
        # the car has visited.
        self.Coordenadas = [[], []]
        # A variable that is used to check if the car is avoiding a collision.
        self.numOfCars = self.model.num_agents
        # A variable that is used to check if the car is avoiding a collision.
        self.colision = False

    def step(self):
        """
        If the car is not in its destination, it checks if the destination is in its neighborhood, if it is,
        it moves to it, if not, it checks if the next cell is a road, if it is, it checks if the road is an
        intersection, if it is, it checks if the intersection is an omni-directional intersection, if it is,
        it checks if the next cell is a car, if it is, it avoids the collision, if not, it checks if the
        direction is left or right, if it is, it checks if the next cell is a car, if it is, it avoids the
        collision, if not, it checks if the next cell is a car, if it is, it avoids the collision, if not,
        it checks if the next cell is a car, if it is, it avoids the collision, if not, it checks if the
        next cell is a car, if it is, it avoids the collision, if not,
        :return: the position of the agent in the grid.
        """
        # Getting the neighborhood of the agent.
        checa_entorno = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        # A lambda function that returns the contents of the cell.
        ver_celdasiguiente = lambda x: self.model.grid.get_cell_list_contents([x])
        obtener_celda = lambda x: [type(i) for i in ver_celdasiguiente(x)]
        # Getting the contents of the cells in the neighborhood of the agent.
        mover_celda = [ver_celdasiguiente(i) for i in checa_entorno]
        # Creating a list of lists that contains the type of the objects in the cells of the
        # neighborhood of the agent.
        pasos = [[type(j) for j in i] for i in mover_celda]
        # Getting the index of the position of the agent in the neighborhood of the agent.
        posicion_actual = checa_entorno.index(self.pos)
        # Creating a dictionary that contains the index of the position of the agent in the
        # neighborhood of the agent.
        movimiento = self.obtenMovimiento(checa_entorno)
        # Checking if the car is in its destination, if it is, it removes the car from the grid and
        # the schedule.
        if self.pos == self.destino:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.numOfCars -= 1
            return
        # Checking if the car is in its destination, if it is, it removes the car from the grid and
        # the schedule.
        if self.pos != self.destino:
            for vecino_carro in checa_entorno:
                if self.destino == vecino_carro:
                    self.model.grid.move_agent(self, vecino_carro)
                    self.detenido = False
                    return
            # Checking if the cell that the agent is in is a road.
            if Ruta66 == pasos[posicion_actual][0]:  # Cuchao
                # Checking if the direction of the road is omni-directional, if it is, it gets the
                # next cell in the direction of the car.
                if mover_celda[posicion_actual][0].direction == "Omni":
                    f_paso = checa_entorno[movimiento[self.Direccion]]
                    # Checking if the next cell is a car, if it is, it avoids the collision.
                    if Mcqueen in obtener_celda(f_paso):
                        print("--------------------Mcqueen", self.unique_id, "evadió colisión-----------------------")
                        self.colision = True
                        self.model.grid.move_agent(self, self.Esquivar(checa_entorno, obtener_celda, self.Direccion))
                    # Checking if the direction of the car is left or right, if it is, it is checking
                    # if the next cell is a car, if it is, it avoids the collision, if not, it checks
                    if self.Direccion == "Left" or self.Direccion == "Right":
                        self.elige_ruta([(f_paso[0], f_paso[1]+1), f_paso,
                                         (f_paso[0], f_paso[1]-1),
                                         (self.pos[0], self.pos[1]+1),
                                         (self.pos[0], self.pos[1]-1)],
                                        obtener_celda, 1)
                    # Checking if the direction of the car is up or down, if it is, it is checking if the next cell is a
                    # car, if it is, it avoids the collision, if not, it checks if the next cell is a car, if it is, it
                    # avoids the collision, if not, it checks if the next cell is a car, if it is, it avoids the
                    # collision, if not, it checks if the next cell is a car, if it is, it avoids the collision, if not,
                    # it checks if the next cell is a car, if it is, it avoids the collision, if not, it checks if the
                    # next cell is a car, if it is, it avoids the collision, if not, it checks if the next cell is a car,
                    # if it is, it avoids the collision, if not, it checks if the next cell is a car, if it is, it avoids
                    # the collision, if not, it checks if the next cell is a car, if it is, it avoids the collision, if
                    # not, it checks if the next cell is a car, if it is, it avoids the collision, if not, it
                    elif self.Direccion == "Up" or self.Direccion == "Down":
                        self.elige_ruta([(f_paso[0]+1, f_paso[1]), f_paso,
                                         (f_paso[0]-1, f_paso[1]),
                                         (self.pos[0]+1, self.pos[1]),
                                         (self.pos[0]-1, self.pos[1])],
                                        obtener_celda, 0)
                # Checking if the agent is in the same cell as the light and if the light is green. If
                # so, it moves the agent to the next cell.
                else:
                    f_paso = movimiento[mover_celda[posicion_actual][0].direction]
                    if Semaforo == pasos[f_paso][0]:
                        if mover_celda[f_paso][0].state and Mcqueen not in pasos[f_paso]:
                            self.model.grid.move_agent(self,
                                                       checa_entorno[f_paso])
                            self.Direccion = mover_celda[posicion_actual][0].direction
                            self.detenido = False
                        # Checking if the program is running on Windows or Linux.
                        else:
                            self.detenido = True
                    # The above code is checking if the agent is in the same cell as the agent that is
                    # being followed. If it is, then the agent will move to the next cell in the list
                    # of cells that the agent is following.
                    elif Mcqueen not in pasos[f_paso]:
                        self.model.grid.move_agent(self, checa_entorno[f_paso])
                        self.Direccion = mover_celda[posicion_actual][0].direction
                        self.detenido = False
                    # Checking if the program is running on Windows or Linux.
                    else:
                        self.detenido = True
            # The above code is checking if the agent is in the same cell as the McQueen agent. If it
            # is, then the agent will not move. If it is not, then the agent will move.
            else:
                if Mcqueen not in pasos[movimiento[self.Direccion]]:
                    self.model.grid.move_agent(self, checa_entorno[movimiento[self.Direccion]])
                    self.detenido = False
                # A class that is used to create a thread.
                else:
                    self.detenido = True

    def Esquivar(self, pasos, obten_celda, ejes):
        """
        If the car is in the way, move to the side of the car
        :param pasos: list of possible moves
        :param obten_celda: This is a function that returns the contents of a cell
        :param ejes: The direction of the car
        :return: the next position of the car.
        """
        esquiva = [i for i in pasos if Mcqueen in obten_celda(i)][0]
        try:
            if ejes == "Left" or ejes == "Right":
                celda = [i for i in pasos if i != esquiva and i[1] == self.pos[1]][0]
                return celda
            elif ejes == "Up" or ejes == "Down":
                celda = [i for i in pasos if i != esquiva and i[0] == self.pos[0]][0]
                return celda
            else:
                celda = [i for i in pasos if i != esquiva][0]
                return celda
        except:
            # move anywhere else if it can't move to the side of the car
            celda = [i for i in pasos if i != esquiva][0]
            return celda

    def obtenMovimiento(self, siguiente_paso):
        """
        It takes a list of tuples (coordinates) and returns a dictionary with
        the keys being the direction of the next step and the values being the
        index of the next step in the list:param siguiente_paso: This is the
        list of all possible moves that the agent can make
        :return: A dictionary with the possible moves.
        """
        # Creating a dictionary called movimiento.
        movimiento = {}
        for i in range(len(siguiente_paso)):
           # Checking if the next step is to the right of the current position.
            if siguiente_paso[i][0] == self.pos[0]+1 and siguiente_paso[i][1] == self.pos[1]:
                movimiento["Right"] = i
            # Assigning a value to a dictionary.
            elif siguiente_paso[i][0] == self.pos[0]-1 and siguiente_paso[i][1] == self.pos[1]:
                movimiento["Left"] = i
            # Checking if the next step is in the same position as the current position. If it is, it
            # will return the index of the next step.
            elif siguiente_paso[i][0] == self.pos[0] and siguiente_paso[i][1] == self.pos[1]+1:
                movimiento["Up"] = i
           # Checking if the next step is in the same position as the current position.
            elif siguiente_paso[i][0] == self.pos[0] and siguiente_paso[i][1] == self.pos[1]-1:
                movimiento["Down"] = i
        return movimiento

    def CalcularRuta(self, Direcciones, obten_celda, ejes):
        """
        It calculates the best route to take to get to the destination
        :param Direcciones: A list of the possible directions the car can go
        :param obten_celda: This is a function that returns the contents of a
        cell :param ejes: 0 for x, 1 for y:return: The index of the best route.
        """
        # Setting the initial value of the variable menor_distancia to the sum of the width and height
        # of the model.
        menor_distancia = self.model.width*2 + self.model.height*2
        # Creating a variable called mejor_ruta and assigning it the value None.
        mejor_ruta = None
        # Creating a variable called re_calcular and assigning it the value of None.
        re_calcular = None
        # Creating a variable called peor_escenario and assigning it the value of None.
        peor_escenario = None
        # Checking if the position of the player is in the list of coordinates.
        if self.pos in self.Coordenadas[0]:
            re_calcular = self.Coordenadas[0].index(self.pos)
        # Finding the best route to the destination.
        for i in range(len(Direcciones)):
            # Checking if the position is within the boundaries of the grid.
            if (self.model.width-1 >= Direcciones[i][0] >= 0) and (self.model.height-1 >= Direcciones[i][1] >= 0):
                # Checking if the car is in the same row or column as the traffic light.
                if Ruta66 in obten_celda(Direcciones[i]) or (Semaforo in obten_celda(Direcciones[i]) and self.pos[ejes] == Direcciones[i][ejes]):
                    # Checking if the distance between the current position and the destination is
                    # less than the current minimum distance.
                    if abs(1+self.destino[0]-Direcciones[i][0])+abs(1+self.destino[1]-Direcciones[i][1]) < menor_distancia:
                        # Checking if the user has entered a value for the variable re_calcular. If
                        # the user has entered a value, then the code will execute the code below.
                        if re_calcular != None:
                            # Checking if the current position is in the list of coordinates. If it is, it will check if the next
                            # position is in the list of coordinates. If it is, it will check if the next position is in the list
                            # of coordinates. If it is, it will check if the next position is in the list of coordinates. If it
                            # is, it will check if the next position is in the list of coordinates. If it is, it will check if the
                            # next position is in the list of coordinates. If it is, it will check if the next position is in the
                            # list of
                            if Direcciones[i] not in self.Coordenadas[1][re_calcular]:
                                menor_distancia = abs(1+self.destino[0]-Direcciones[i][0])+abs(1+self.destino[1]-Direcciones[i][1])
                                mejor_ruta = i
                            peor_escenario = i
                        # Finding the best route to the destination.
                        else:
                            menor_distancia = abs(1+self.destino[0]-Direcciones[i][0])+abs(1+self.destino[1]-Direcciones[i][1])
                            mejor_ruta = i
        # Checking if the best route is None, if it is, it returns the worst scenario.
        if mejor_ruta == None:
            return peor_escenario
        # A function that returns the best route for a given graph.
        else:
            return mejor_ruta

    def elige_ruta(self, Direcciones, obten_celda, ejes):
        """
        The function chooses the next cell to move to based on the distance
        to the nearest car :param Direcciones: A list of the possible 
        directions the agent can move in :param obten_celda: This is a
        function that returns the contents of a cell :param ejes: 
        The number of rows and columns in the grid
        """
        punto_referencia = self.CalcularRuta(Direcciones, obten_celda, ejes)
        if Mcqueen not in obten_celda(Direcciones[punto_referencia]):
            if self.pos not in self.Coordenadas[0]:
                self.Coordenadas[0].append(self.pos)
                self.Coordenadas[1].append([Direcciones[punto_referencia]])
            else:
                self.Coordenadas[1][self.Coordenadas[0].index(self.pos)].append(Direcciones[punto_referencia])
            self.model.grid.move_agent(self, Direcciones[punto_referencia])
            self.detenido = False
        else:
            self.detenido = True


class Semaforo(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change 
            color
        """
        self.state = state
        self.timeToChange = timeToChange


class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Ruta66(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, uniqueID, model, direction = "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(uniqueID, model)
        self.direction = direction
