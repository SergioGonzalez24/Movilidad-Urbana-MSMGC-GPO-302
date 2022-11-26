from mesa import Agent
from random import randint

# Agent that represents the Cars going around the city
class Car(Agent):
    def __init__(self, uniqueID, model, destPos):
        """
        Class initializer (constructor) to create a new Robot agent
        ● Parameters:
            uniqueID: The agent's ID
            model: Model reference for the agent
            destPos: Tuple coordinates of where the car should go
        ● Return: None
        """
        super().__init__(uniqueID, model)
        # Value used know if the car has stopped
        self.isStop = False
        # Attributes to make the agent know where to go 
        self.destination = destPos
        self.tmpDir = ""
        # Attribute used to avoid cycles by keeping a log of the car's
        # positions and its decisions
        self.takenRoute = [[],[]]
        
        self.inDest = False

    def step(self):
        """
        Method that gets executed every time the model updates
        ● Parameters: 
            self: Reference to class' instance
        ● Return: None (Return is used to avoid execution of some sections of the code)
        """
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True, # Boolean for whether to use Moore neighborhood (diagonals) or Von Neumann (up/down/left/right).
            include_center = True) 
        
        getConOfCell = lambda x: self.model.grid.get_cell_list_contents([x])
        getConTypeOfCell = lambda x: [type(i) for i in getConOfCell(x)]
        posStepsCont = [getConOfCell(i) for i in possibleSteps]
        posStepsType = [[type(j) for j in i] for i in posStepsCont]
        currPos = possibleSteps.index(self.pos)
        motion = self.getMotion(possibleSteps)
        
        # If it's already in a Destination, then quits
        if self.pos != self.destination:
            print("Car", self.unique_id, "is at", self.pos, "and is going to", self.destination)
            # Scans to find if there's a destination around
            for neighbor in possibleSteps:
                # If it finds a destination point, it moves there
                if self.destination == neighbor:
                    self.model.grid.move_agent(self, neighbor)
                    self.isStop = False
                    return
    
            # Checks if is on the road (which it is, but is basically to differentiate from the Traffic Light cell)
            if Road == posStepsType[currPos][0]: 

                # Checks if the car is on a "decision section" (intersection)
                if posStepsCont[currPos][0].direction == "Omni":
                    futurePos = possibleSteps[motion[self.tmpDir]]
                    # If the car is moving horizontally then it moves to the possible next coordinates given that axis and direction
                    if self.tmpDir == "Left" or self.tmpDir == "Right":
                        self.makeDecision([(futurePos[0], futurePos[1]+1), futurePos, (futurePos[0], futurePos[1]-1), (self.pos[0], self.pos[1]+1), (self.pos[0], self.pos[1]-1)], getConTypeOfCell, 1)
                    # If the car is moving vertically then it moves to the possible next coordinates given that axis and direction
                    elif self.tmpDir == "Up" or self.tmpDir == "Down":
                        self.makeDecision([(futurePos[0]+1, futurePos[1]), futurePos, (futurePos[0]-1, futurePos[1]), (self.pos[0]+1, self.pos[1]), (self.pos[0]-1, self.pos[1])], getConTypeOfCell, 0)
                else:
                    futurePos = motion[posStepsCont[currPos][0].direction]
                    # If there's a traffic light in front
                    if Traffic_Light == posStepsType[futurePos][0]:
                        if posStepsCont[futurePos][0].state and Car not in posStepsType[futurePos]:
                            self.model.grid.move_agent(self, possibleSteps[futurePos]) 
                            self.tmpDir = posStepsCont[currPos][0].direction
                            self.isStop = False
                        else:
                            self.isStop = True
                    # If there are no cars in front
                    elif Car not in posStepsType[futurePos]:
                        self.model.grid.move_agent(self, possibleSteps[futurePos]) 
                        self.tmpDir = posStepsCont[currPos][0].direction
                        self.isStop = False
                    else:
                        self.isStop = True
                        
            # If the car is in the cell where the traffic light is
            else:
                if Car not in posStepsType[motion[self.tmpDir]]:
                    self.model.grid.move_agent(self, possibleSteps[motion[self.tmpDir]]) 
                    self.isStop = False
                else:
                    self.isStop = True

    def getMotion(self, posSteps):
        """
        Method used to determine the index of the neighborhood list depending on the direction
        of the road in which the car is currently in
        ● Parameters: 
            self: Reference to class' instance
            posSteps: List of neighbor cells with relative of the current position of the car
        ● Return:
            motion: Dictionary containing the indexes of all possible steps given a direction string key
        """
        motion = {}
        for c in range(len(posSteps)):
            if posSteps[c][0] == self.pos[0]+1 and posSteps[c][1] == self.pos[1]:
                motion["Right"] = c
            elif posSteps[c][0] == self.pos[0]-1 and posSteps[c][1] == self.pos[1]:
                motion["Left"] = c
            elif posSteps[c][0] == self.pos[0] and posSteps[c][1] == self.pos[1]+1:
                motion["Up"] = c
            elif posSteps[c][0] == self.pos[0] and posSteps[c][1] == self.pos[1]-1:
                motion["Down"] = c
        return motion

    def getBestMove(self, posDirs, getConTypeOfCell, axis):
        """
        Method used to calculate the best position to go to from all the possible steps (neighbor cells)
        that are also valid (not cars, buildings or traffic lights)
        ● Parameters: 
            self: Reference to class' instance
            posDirs: List of coordinates (tuples) containing the possible steps depending on the 
                     direction where the car is currently heading
            getConTypeOfCell: Lambda function to determine the types of all elements within a cell
            axis: Integer value used to compare if the traffic light and the car are aligned in the axis
                  of the direction where the car is currently heading
        ● Return:
            bestFuture: Integer value which is the index for the coordinate list of possible steps
        """
        # Variable that will contain the minimum distance possible to the destination from a possible step
        minDistSigma = self.model.width*2 + self.model.height*2
        bestFuture = None
        reevaluate = None
        jokerFuture = None
        # If the car is on an intersection repeated (possible cycle) then it finds the index from the logs list
        # of the last time it was in this particular intersection
        if self.pos in self.takenRoute[0]:
            reevaluate = self.takenRoute[0].index(self.pos)
        # Iterates through all the possibilities to find the one which gets the car closer to the destination
        for p in range(len(posDirs)):
            # First verifies if the possible next step is within the map coordinates
            if (self.model.width-1 >= posDirs[p][0] >= 0) and (self.model.height-1 >= posDirs[p][1] >= 0):
                # Second, it verifies if the next cell is either more road or if theres a traffic light cell, is in front of it
                if Road in getConTypeOfCell(posDirs[p]) or (Traffic_Light in getConTypeOfCell(posDirs[p]) and self.pos[axis] == posDirs[p][axis]):
                    # Next, determines if the distante calculation is better than the currently minimum
                    if abs(1+self.destination[0]-posDirs[p][0])+abs(1+self.destination[1]-posDirs[p][1]) < minDistSigma:
                        # If the car was, indeed, on a repeated intersection, then it evaluates if the currently possible next step
                        # wasn't already taken in the past
                        if reevaluate != None:
                            if posDirs[p] not in self.takenRoute[1][reevaluate]:
                                minDistSigma = abs(1+self.destination[0]-posDirs[p][0])+abs(1+self.destination[1]-posDirs[p][1])
                                bestFuture = p
                            jokerFuture = p
                        # if it's the first time, then this one becomes the best option
                        else:
                            minDistSigma = abs(1+self.destination[0]-posDirs[p][0])+abs(1+self.destination[1]-posDirs[p][1])
                            bestFuture = p
        # In case there's a completely unavoidable loop, then it keeps cycling cause the car rather continue its endless
        # path than stopping the entire stream of cars behind who actually know where they're heading to
        if bestFuture == None:
            return jokerFuture
        else:
            return bestFuture

    def makeDecision(self, posDirs, getConTypeOfCell, axis):
        """
        Method used to move the car when it is on an intersection (actually just used because
        it was a repetitive task with minor changes)
        ● Parameters: 
            self: Reference to class' instance
            posDirs: List of coordinates (tuples) containing the possible steps depending on the 
                     direction where the car is currently heading
            getConTypeOfCell: Lambda function to determine the types of all elements within a cell
            axis: Integer value used to compare if the traffic light and the car are aligned in the axis
                  of the direction where the car is currently heading
        ● Return: None
        """
        # Gets the best option from all the possibilities
        dirIndex = self.getBestMove(posDirs, getConTypeOfCell, axis)
        if Car not in getConTypeOfCell(posDirs[dirIndex]):
            # If it's the car's first time on that intersection it keeps a log of that and the decision (coordinate where it went next) it made
            if self.pos not in self.takenRoute[0]:
                self.takenRoute[0].append(self.pos)
                self.takenRoute[1].append([posDirs[dirIndex]])
            # If it had already been there then just adds the decision made to the list of decisions made on that particular coordinate
            else:
                self.takenRoute[1][self.takenRoute[0].index(self.pos)].append(posDirs[dirIndex])
            self.model.grid.move_agent(self, posDirs[dirIndex])
            self.isStop = False
        else:
            self.isStop = True


# Traffic lights that will regulate the traffic of the cars in intersections
class Traffic_Light(Agent):
    def __init__(self, uniqueID, model, state = False, timeToChange = 10):
        """
        Class initializer (constructor) to create a new Robot agent
        ● Parameters: 
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Boolean whether the light green is on or off
            timeToChange: timer to know how much time the light will stay on each state
        ● Return: None
        """
        super().__init__(uniqueID, model)
        self.state = state
        self.timeToChange = timeToChange

# Blocks to where the cars aim to reach
class Destination(Agent):
    def __init__(self, uniqueID, model):
        """
        Class initializer (constructor) to create a new Robot agent
        ● Parameters: 
            unique_id: The agent's ID
            model: Model reference for the agent
        ● Return: None
        """
        super().__init__(uniqueID, model)

# Its called obstacle, but it's actually the buildings
class Obstacle(Agent):
    def __init__(self, uniqueID, model):
        """
        Class initializer (constructor) to create a new Robot agent
        ● Parameters: 
            unique_id: The agent's ID
            model: Model reference for the agent
        ● Return: None
        """
        super().__init__(uniqueID, model)

# The road tiles that build up the streets
class Road(Agent):
    def __init__(self, uniqueID, model, direction= "Left"):
        """
        Class initializer (constructor) to create a new Robot agent
        ● Parameters: 
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: String of the direction allowed for the road
        ● Return: None
        """
        super().__init__(uniqueID, model)
        self.direction = direction
