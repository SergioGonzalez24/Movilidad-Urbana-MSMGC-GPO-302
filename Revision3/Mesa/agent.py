from mesa import Agent
from random import randint
import random
import math
class Car(Agent):
    def __init__(self, uniqueID, model, destPos):


        super().__init__(uniqueID, model)
        self.isStop = False 
        self.destination = destPos
        self.tmpDir = ""
        self.takenRoute = [[],[]]
        self.numOfCars = self.model.num_agents
        self.colision = False

    def step(self):

        # print("Car", self.unique_id, "is at", self.pos)
        # print("Car", self.unique_id, "is heading to", self.destination)
        
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True) 
        
        getConOfCell = lambda x: self.model.grid.get_cell_list_contents([x])
        getConTypeOfCell = lambda x: [type(i) for i in getConOfCell(x)]
        posStepsCont = [getConOfCell(i) for i in possibleSteps]
        posStepsType = [[type(j) for j in i] for i in posStepsCont]
        currPos = possibleSteps.index(self.pos)
        motion = self.getMotion(possibleSteps)
        
        if self.pos == self.destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.numOfCars-= 1
            return
        
        
        if self.pos != self.destination:
            for neighbor in possibleSteps:
                if self.destination == neighbor:
                    self.model.grid.move_agent(self, neighbor)
                    self.isStop = False
                    return
    
            if Road == posStepsType[currPos][0]: 
                
                if posStepsCont[currPos][0].direction == "Omni":
                    futurePos = possibleSteps[motion[self.tmpDir]]
                     
                     
                    if Car in getConTypeOfCell(futurePos):
                        print("--------------------Car", self.unique_id, "is avoiding collision-----------------------")
                        self.colision = True
                        self.model.grid.move_agent(self, self.avoidCollision(possibleSteps, getConTypeOfCell, self.tmpDir))
                               
                    if self.tmpDir == "Left" or self.tmpDir == "Right":
                        self.makeDecision([(futurePos[0], futurePos[1]+1), futurePos, (futurePos[0], futurePos[1]-1), (self.pos[0], self.pos[1]+1), (self.pos[0], self.pos[1]-1)], getConTypeOfCell, 1)
                    elif self.tmpDir == "Up" or self.tmpDir == "Down":
                        self.makeDecision([(futurePos[0]+1, futurePos[1]), futurePos, (futurePos[0]-1, futurePos[1]), (self.pos[0]+1, self.pos[1]), (self.pos[0]-1, self.pos[1])], getConTypeOfCell, 0)
                        
                 
                else:
                    futurePos = motion[posStepsCont[currPos][0].direction]
                    if Traffic_Light == posStepsType[futurePos][0]:
                        if posStepsCont[futurePos][0].state and Car not in posStepsType[futurePos]:
                            self.model.grid.move_agent(self, possibleSteps[futurePos]) 
                            self.tmpDir = posStepsCont[currPos][0].direction
                            self.isStop = False
                        else:
                            self.isStop = True
                    elif Car not in posStepsType[futurePos]:
                        self.model.grid.move_agent(self, possibleSteps[futurePos]) 
                        self.tmpDir = posStepsCont[currPos][0].direction
                        self.isStop = False
                    else:
                        self.isStop = True
                        
            else:
                if Car not in posStepsType[motion[self.tmpDir]]:
                    self.model.grid.move_agent(self, possibleSteps[motion[self.tmpDir]]) 
                    self.isStop = False
                else:
                    self.isStop = True
                    
    def avoidCollision(self, possibleSteps, getConTypeOfCell, axis):

        
        
        carToAvoid = [i for i in possibleSteps if Car in getConTypeOfCell(i)][0]
        try:
            if axis == "Left" or axis == "Right":
                cell = [i for i in possibleSteps if i != carToAvoid and i[1] == self.pos[1]][0]
                return cell
            elif axis == "Up" or axis == "Down":
                cell = [i for i in possibleSteps if i != carToAvoid and i[0] == self.pos[0]][0]
                return cell
            else:
                cell = [i for i in possibleSteps if i != carToAvoid][0]
                return cell
        except:
            
            cell = [i for i in possibleSteps if i != carToAvoid][0]
            return cell
                     
    def getMotion(self, posSteps):

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

        minDistSigma = self.model.width*2 + self.model.height*2
        bestFuture = None
        reevaluate = None
        jokerFuture = None
        if self.pos in self.takenRoute[0]:
            reevaluate = self.takenRoute[0].index(self.pos)
        for p in range(len(posDirs)):
            if (self.model.width-1 >= posDirs[p][0] >= 0) and (self.model.height-1 >= posDirs[p][1] >= 0):
                if Road in getConTypeOfCell(posDirs[p]) or (Traffic_Light in getConTypeOfCell(posDirs[p]) and self.pos[axis] == posDirs[p][axis]):
                    if abs(1+self.destination[0]-posDirs[p][0])+abs(1+self.destination[1]-posDirs[p][1]) < minDistSigma:
                        if reevaluate != None:
                            if posDirs[p] not in self.takenRoute[1][reevaluate]:
                                minDistSigma = abs(1+self.destination[0]-posDirs[p][0])+abs(1+self.destination[1]-posDirs[p][1])
                                bestFuture = p
                            jokerFuture = p
                        else:
                            minDistSigma = abs(1+self.destination[0]-posDirs[p][0])+abs(1+self.destination[1]-posDirs[p][1])
                            bestFuture = p
        if bestFuture == None:
            return jokerFuture
        else:
            return bestFuture

    def makeDecision(self, posDirs, getConTypeOfCell, axis):
 

        dirIndex = self.getBestMove(posDirs, getConTypeOfCell, axis)
        if Car not in getConTypeOfCell(posDirs[dirIndex]):
            if self.pos not in self.takenRoute[0]:
                self.takenRoute[0].append(self.pos)
                self.takenRoute[1].append([posDirs[dirIndex]])
            else:
                self.takenRoute[1][self.takenRoute[0].index(self.pos)].append(posDirs[dirIndex])
            self.model.grid.move_agent(self, posDirs[dirIndex])
            self.isStop = False
        else:
            self.isStop = True


class Traffic_Light(Agent):
    def __init__(self, uniqueID, model, state = False, timeToChange = 10):

        super().__init__(uniqueID, model)
        self.state = state
        self.timeToChange = timeToChange


class Destination(Agent):
    def __init__(self, uniqueID, model):

        super().__init__(uniqueID, model)

class Obstacle(Agent):
    def __init__(self, uniqueID, model):

        super().__init__(uniqueID, model)


class Road(Agent):
    def __init__(self, uniqueID, model, direction= "Left"):

        super().__init__(uniqueID, model)
        self.direction = direction