# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:25:01 2022

@author: redno
"""

class Connection:
    __id : int
    __links : None
    __slots : None
    __bandSelected : str
    
    def __init__(self, id : int):
        self.__id = id
        self.__links = []
        self.__slots = []
        self.__bandSelected : str = "NoBand"
    
    def addLink(self, idLink : int, slots: int):
        self.__links.append(idLink)
        self.__slots.append(slots)
        
    def addLink(self, idLink, fromSlot: int, toSlot : int):
        self.__links.append(idLink)
        lSlots = []
        for i in range(fromSlot, toSlot):
            lSlots.append(i)
        self.__slots.append(lSlots)
        
    @property
    def bandSelected(self):
        return self.__bandSelected
    
    @bandSelected.setter
    def bandSelected(self, bandSelected : str):
        self.__bandSelected = bandSelected

    ''' Id getter & setter '''
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,id):
        self.__id = id

    ''' Links getter & setter '''
    @property
    def links(self):
        return self.__links

    @links.setter
    def links(self,idLinks):
        #self.__links = []
        self.__links = idLinks       # Asigna todos los links en la conexión en vez de ir uno por uno 

    ''' Slots getter & setter '''
    @property
    def slots(self):
        return self.__slots

    @slots.setter
    def slots(self,slots):
        #self.__slots = []
        self.__slots = slots       # Asigna todos los slots de cada enlace en la conexión  