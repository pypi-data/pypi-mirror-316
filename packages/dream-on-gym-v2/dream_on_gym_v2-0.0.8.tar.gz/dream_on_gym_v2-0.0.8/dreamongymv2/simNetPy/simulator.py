# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 15:40:47 2022

@author: redno
"""
from .controller import Controller
from .bitRate import BitRate
from .network import Network
from .event import Event
from .event import EventType
from .connectionEvent import ConnectionEvent
# import simulator.source.uniformVariable as uniformVariable  # ???
from .uniformVariable import UniformVariable
# import expVariable  # es el otro archivo o una libreria?
from .expVariable import ExpVariable
import math
from datetime import datetime


class Simulator:
    __events = None
    __arriveVariable = None
    __departVariable = None
    __srcVariable = None
    __dstVariable = None
    __bitRateVariable = None
    __controller = None
    __currentEvent = None
    __bitRates = None
    __confidence = 0.0
    __zScore = 0.0
    __initReady = False
    __lambda = 0.0
    __mu = 0.0
    __seedArrive = 0
    __seedDeparture = 0
    __seedSrc = 0
    __seedDst = 0
    __seedBitRate = 0
    __numberOfEvents = 0
    __goalConnections = 0
    __nextEventTime = 0.0
    __allocationStatus = 0.0
    __rtnAllocation = 0.0
    __connectionEvent = ConnectionEvent()
    __src = 0
    __dst = 0
    __bitRate = 0
    __bitRatesDefault = None
    __blockingProbability = 0.0
    __columnWidth = 0

    __startingTime = None
    __checkTime = None
    __timeDuration = None
    

    def __init__(self, networkFile="", pathFilename="", bitrateFilename=""):
        #Set default values.
        self.defaultValues()
        self.__clock = 0
        self.__controller = Controller()
        if (networkFile != ""):
            self.__controller.network = Network(networkFile)
        if (pathFilename != ""):
            self.__controller.setPaths(pathFilename)
        self.__events = []
        #If has bit rate file is loaded, but else load default values.
        if (bitrateFilename != ""):
            self.__bitRatesDefault = BitRate().readBitRateFile(bitrateFilename)
        else:
            self.__bitRatesDefault = []
            auxB = BitRate(10.0)
            auxB.addModulation("BPSK", 1, 5520)
            self.__bitRatesDefault.append(auxB)
            auxB = BitRate(40.0)
            auxB.addModulation("BPSK", 4, 5520)
            self.__bitRatesDefault.append(auxB)
            auxB = BitRate(100.0)
            auxB.addModulation("BPSK", 8, 5520)
            self.__bitRatesDefault.append(auxB)
            auxB = BitRate(400.0)
            auxB.addModulation("BPSK", 32, 5520)
            self.__bitRatesDefault.append(auxB)
            auxB = BitRate(1000.0)
            auxB.addModulation("BPSK", 80, 5520)
            self.__bitRatesDefault.append(auxB)
        self.__lastConnectionIsAllocated = Controller.Status.N_A   # Return error when Status is private in Controller
        #This functions are optionals
        self.__agentAction = None
        self.__truncatedFunc = None
        self.__terminatedFunc = None
        # self._ //falta algo aca???

    def setLambda(self, lambdaValue):
        if (self.__initReady):
            raise "You can not set lambda parameter AFTER calling init simulator method."
        self.__lambda = lambdaValue

    def setMu(self, mu):
        if (self.__initReady):
            raise "You can not set lambda parameter AFTER calling init simulator method."
        self.__mu = mu

    def setSeedArrive(self, seed):
        if (self.__initReady):
            raise "You can not set seed arrive parameter AFTER calling init simulator method."
        self.__seedArrive = seed

    def setSeedDeparture(self, seed):
        if (self.__initReady):
            raise "You can not set seed departure parameter AFTER calling init simulator method."
        self.__seedDeparture = seed

    def setSeedBitRate(self, seed):
        if (self.__initReady):
            raise "You can not set seed bitrate parameter AFTER calling init simulator method."
        self.__seedBitRate = seed

    def setSeedSrc(self, seed):
        if (self.__initReady):
            raise "You can not set seed source parameter AFTER calling init simulator method."
        self.__seedSrc = seed

    def setSeedDst(self, seed):
        if (self.__initReady):
            raise "You can not set seed destiny parameter AFTER calling init simulator method."
        self.__seedDst = seed

    def setGoalConnections(self, goal):
        if (self.__initReady):
            raise "You can not set goal connections parameter AFTER calling init simulator method."
        self.__goalConnections = goal

    def setBitRates(self, bitRates):
        if (self.__initReady):
            raise "You can not set bitrates parameter AFTER calling init simulator method"
        self.__bitRatesDefault = bitRates

    def setAllocator(self, algorithm):
        self.__controller.allocator = algorithm

    def setConfidence(self, c):
        if (c <= 0 or c >= 1):
            raise "You can't set a confidence interval with confidence equal/higher than 1 or equal/lower than 0."
        self.__confidence = c

    #If verbose is activated, show the simulation details status.
    def printInitialInfo(self):
        print("Nodes: ", end='')
        print(self.__controller.network.getNumberOfNodes())
        print("Links: ", end='')
        print(self.__controller.network.getNumberOfLinks())
        print("Goal Connections: ", end='')
        print(self.__goalConnections)
        print("Lambda: ", end='')
        print(self.__lambda)
        print("Mu: ", end='')
        print(self.__mu)
        print('+', end='')
        for i in range(0, 7):
            print('{:->11}'.format('+'), end='')
        print("\n|", end='')
        print('{: >11}'.format('progress |'), end='')
        print('{: >11}'.format('arrives |'), end='')
        print('{: >11}'.format('blocking |'), end='')
        print('{: >11}'.format('time(s) |'), end='')
        print('{: >11}'.format('Wald CI |'), end='')
        print('{: >11}'.format('A-C. CI |'), end='')
        print('{: >11}'.format('Wilson CI |'))
        print('+', end='')
        for i in range(0, 7):
            print('{:->11}'.format('+'), end='')
        print("")
        self.__startingTime = datetime.now()

    #If verbose is activated, show the simulation details status.
    def printRow(self, percentage):
        self.__checkTime = datetime.now()
        self.__timeDuration = self.__checkTime - self.__startingTime
        print('|', end='')
        print('{: >11}'.format(str(percentage)+'% |'), end='')
        print('{: >11}'.format(str(self.__numberOfConnections - 1)+' |'), end='')
        print('{: >11}'.format("{0:.6f}".format(self.getBlockingProbability())+' |'), end='')
        print('{: >11}'.format(str(self.__timeDuration).split(".")[0]+' |'), end='')
        print('{: >11}'.format("{0:.6f}".format(self.waldCI())+' |'), end='')
        print('{: >11}'.format("{0:.6f}".format(self.agrestiCI())+' |'), end='')
        print('{: >11}'.format("{0:.6f}".format(self.wilsonCI())+' |'))
        print('+', end='')
        for i in range(0, 7):
            print('{:->11}'.format('+'), end='')
        print("")

    #Create a simulation connection.
    def createEventConnection(self):
        self.__connectionEvent.source = self.__srcVariable.getNextIntValue()
        self.__connectionEvent.destination = self.__dstVariable.getNextIntValue()

        while (self.__connectionEvent.source == self.__connectionEvent.destination):
            self.__connectionEvent.destination = self.__dstVariable.getNextIntValue()
        self.__connectionEvent.bitRate = self.__bitRateVariable.getNextIntValue()

        # Se redondea porque no se puede buscar un flotante en un arreglo
        self.__connectionEvent.bitRate = round(self.__connectionEvent.bitRate)
        
    #Is called when start the simulation and when the agent is training.
    def eventRoutine(self, action):
        self.__currentEvent = self.__events[0]
        self.__rtnAllocation = Controller.Status.N_A
        self.__clock = self.__currentEvent.getTime()
        if (self.__currentEvent.getType().name == EventType.Arrive.name):
            self.__nextEventTime = self.__clock + self.__arriveVariable.getNextValue()
            for pos in range(len(self.__events)-1, -1, -1):
                if (self.__events[pos].getTime() < self.__nextEventTime):
                    self.__numberOfConnections += 1
                    self.__events.insert(pos+1, Event(
                        EventType.Arrive, self.__nextEventTime, self.__numberOfConnections))
                    break
            if (action is None):
                self.createEventConnection()
            self.__src = self.__connectionEvent.source
            self.__dst = self.__connectionEvent.destination
            self.__bitRate = self.__connectionEvent.bitRate

            self.__rtnAllocation = self.__controller.assignConnection(
                self.__src, self.__dst, self.__bitRates[self.__bitRate], self.__currentEvent.getIdConnection(), action)
            if (self.__rtnAllocation.name == Controller.Status.Allocated.name):
                self.__nextEventTime = self.__clock + self.__departVariable.getNextValue()
                for pos in range(len(self.__events)-1, -1, -1):
                    if (self.__events[pos].getTime() < self.__nextEventTime):
                        self.__events.insert(pos+1, Event(
                            EventType.Departure, self.__nextEventTime, self.__currentEvent.getIdConnection()))
                        break
                self.__allocatedConnections += 1
        else:
            if (self.__currentEvent.getType().name == EventType.Departure.name):
                self.__controller.unassignConnection(
                    self.__currentEvent.getIdConnection())
        self.__events.pop(0)
        self.__lastConnectionIsAllocated = self.__rtnAllocation
        return self.__rtnAllocation

    def init(self):
        self.__initReady = True
        self.__clock = 0
        self.__arriveVariable = ExpVariable(
            self.__seedArrive, self.__lambda)
        self.__departVariable = ExpVariable(
            self.__seedDeparture, self.__mu)
        self.__srcVariable = UniformVariable(
            self.__seedSrc, self.__controller.network.getNumberOfNodes())
        self.__dstVariable = UniformVariable(
            self.__seedDst, self.__controller.network.getNumberOfNodes())
        self.__bitRateVariable = UniformVariable(
            self.__seedBitRate, len(self.__bitRatesDefault))
        # numberOfConnections a 0. Considerar como cantidad de conexiones previas al evento
        self.__numberOfConnections = 0
        self.__events.append(Event(
            EventType.Arrive, self.__arriveVariable.getNextValue(), self.__numberOfConnections))
        self.__bitRates = self.__bitRatesDefault
        self.initZScore()

    def run(self, verbose=False):
        timesToShow = 20 #Aqui se modifica la frecuencia del muestreo de datos
        arrivesByCicle = self.__goalConnections / timesToShow
        verbose and self.printInitialInfo()
        for i in range(1, timesToShow):
            while(self.__numberOfConnections <= (i * arrivesByCicle)):
                self.__currentEvent = self.__events[0]
                self.eventRoutine(None)
                verbose and self.printRow((100 / timesToShow) * i)

    def forwardDepartures(self):
        self.__currentEvent = self.__events[0]
        while self.__currentEvent.getType() == EventType.Departure:
            self.eventRoutine(None)
            self.__currentEvent = self.__events[0]

    def step(self, action):
        self.__currentEvent = self.__events[0]
        if (self.__currentEvent.getType() == EventType.Arrive):
            self.eventRoutine(action)
        else:
            assert("No puede ocurrir esto")

    def getTimeDuration(self):
        return self.__timeDuration.count()

    def getBlockingProbability(self):
        return 1 - self.__allocatedConnections / self.__numberOfConnections

    def getAllocatedProbability(self):
        return self.__allocatedConnections / self.__numberOfConnections

    def waldCI(self):
        np = self.getAllocatedProbability()
        p = 1 - np
        n = self.__numberOfConnections
        sd = math.sqrt((np * p) / n)
        return self.__zScore * sd

    def agrestiCI(self):
        np = self.getAllocatedProbability()
        n = self.__numberOfConnections
        if self.__allocatedConnections != 0:
            np = np * ((n * (self.__allocatedConnections + 2)) /
                   (self.__allocatedConnections * (n + 4)))
        p = 1 - np
        sd = math.sqrt((np * p) / (n + 4))
        return self.__zScore * sd

    def wilsonCI(self):
        np = self.getAllocatedProbability()
        p = 1 - np
        n = self.__numberOfConnections
        denom = (1 + (math.pow(self.__zScore, 2) / n))
        k = p + math.pow(self.__zScore, 2) / (2 * n)
        sd = math.sqrt(((np * p) / n) +
                       ((math.pow(self.__zScore, 2)) / (4 * math.pow(n, 2))))
        return (self.__zScore * sd) / denom

    def initZScore(self):
        actual = 0.0
        step = 1.0
        covered = 0.0
        objetive = self.__confidence
    #     # con 1e-2 funciona, no es la idea por ningun motivo pero sirve para probar por mientras (1e-6)
        epsilon = 1e-2
        while (math.fabs(objetive - covered) > epsilon):

            meta = math.fabs(objetive - covered)

            print("meta: {}".format(meta))
            print("objetivo: {} covered: {} epsilon: {}".format(
                 objetive, covered, epsilon))

            if(objetive > covered):
                actual += step
                covered = ((1 + math.erf(actual / math.sqrt(2))) -
                           (1 + math.erf(-actual / math.sqrt(2)))) / 2
                if (covered > objetive):
                    step /= 2
            else:
                actual -= step
                convered = ((1 + math.erf(actual / math.sqrt(2))) -
                            (1 + math.erf(-actual / math.sqrt(2)))) / 2
                if (convered < objetive):
                    step /= 2
        self.__zScore = actual

    def defaultValues(self):
        self.__initReady = False
        self.__lambda = 1000
        self.__mu = 100
        self.__seedArrive = 12345
        self.__seedDeparture = 12345
        self.__seedSrc = 12345
        self.__seedDst = 12345
        self.__seedBitRate = 12345
        self.__numberOfConnections = 0
        self.__numberOfEvents = 0
        self.__goalConnections = 10000
        self.__columnWidth = 10
        self.__confidence = 0.95
        self.__allocatedConnections = 0
        
    def lastConnectionIsAllocated(self):
        return self.__lastConnectionIsAllocated
    
    def setAgentAction(self, action):
        self.__agentAction = action
    
    def TruncatedFunc(self):
        self.__truncatedFunc
        
    def getTruncatedFunc(self):
        return self.__truncatedFunc
    
    def setTruncatedFunc(self, truncatedFunc):
        self.__truncatedFunc = truncatedFunc

    def terminatedFunc(self):
        self.__terminatedFunc

    def getTerminatedFunc(self):
        return self.__terminatedFunc
    
    def setTerminatedFunc(self, terminatedFunc):
        self.__terminatedFunc = terminatedFunc    


    ''' '''
    @property
    def events(self):
        return self.__events

    @events.setter
    def events(self,events):
        self.__events = events

    ''' '''
    @property
    def srcVariable(self):
        return self.__srcVariable

    @srcVariable.setter
    def srcVariable(self,seed,nodes):
        self.__srcVariable = UniformVariable(seed,nodes)

    ''' '''
    @property
    def dstVariable(self):
        return self.__dstVariable

    @dstVariable.setter
    def dstVariable(self,seed,nodes):
        self.__dstVariable = UniformVariable(seed,nodes)
    
    ''' '''
    @property
    def bitRateVariable(self):
        return self.__bitRateVariable

    @bitRateVariable.setter
    def bitRateVariable(self,seed,bitRatesSize):
        self.__bitRateVariable = UniformVariable(seed,bitRatesSize)
       
    ''' '''
    @property
    def controller(self):
        return self.__controller

    @controller.setter
    def controller(self,controller):
        self.__controller = controller

    ''' '''
    @property 
    def bitRates(self):
        return self.__bitRates

    @bitRates.setter
    def bitRates(self,bitrateFilename):
        self.__bitRates = BitRate().readBitRateFile(bitrateFilename)

    ''' '''
    @property
    def confidence(self):
        return self.__confidence

    @confidence.setter
    def confidence(self,confidence):
        if (confidence <= 0 or confidence >= 1):
            raise "You can't set a confidence interval with confidence equal/higher than 1 or equal/lower than 0."
        self.__confidence = confidence

    ''' '''
    @property
    def zScore(self):
        return self.__zScore

    @zScore.setter
    def zScore(self,actualScore):
        self.__zScore = actualScore


    ''' Example of getter and setter for goalConnections'''
    @property
    def goalConnections(self):
        return self.__goalConnections

    @goalConnections.setter
    def goalConnections(self,goalConnections):
        self.__goalConnections = goalConnections

    ''' '''
    @property
    def numberOfEvents(self):
        return self.__numberOfEvents
    
    @numberOfEvents.setter
    def numberOfEvents(self,value):
        self.__numberOfEvents = value

    ''' '''
    @property
    def numberOfConnections(self):
        return self.__numberOfConnections
    
    @property
    def connectionEvent(self):
        return self.__connectionEvent
    
    @numberOfConnections.setter
    def numberOfConnections(self,value):
        self.__numberOfConnections = value

    ''' '''
    @property
    def allocatedConnections(self):
        return self.__allocatedConnections
    
    @allocatedConnections.setter
    def allocatedConnections(self,value):
        self.__allocatedConnections = value

    ''' '''
    @property 
    def bitRatesDefault(self):
        return self.__bitRatesDefault

    @bitRates.setter
    def bitRates(self,bitrateFilename):
        self.__bitRatesDefault = BitRate().readBitRateFile(bitrateFilename)

    ''' '''
    @property
    def blockingProbability(self):
        return self.__blockingProbability
    
    @blockingProbability.setter
    def blockingProbability(self,probability):
        self.__blockingProbability = probability

    ''' '''
    @property
    def columnWidth(self):
        return self.__columnWidth

    @columnWidth.setter
    def columnWidth(self,width):
        self.__columnWidth = width

'''
    __startingTime = None
    __checkTime = None
    __timeDuration = None
'''