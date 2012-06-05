#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
import threading
LOG = logging.getLogger(__name__)
from abc import ABCMeta, abstractmethod
from ..Function import FunctionInterface

class FunctionNetworkClient(FunctionInterface):
    def __init__(self, idname, eventserver, parentpath = None):
        if eventserver != None and not isinstance(eventserver, FunctionNetworkServer) and not isinstance(eventserver, HostFunctionNetwork):
            raise TypeError("Type Error: eventserver is a " + str(eventserver.__class__))
        self._parent = eventserver
        from .EventQueue import EventQueue
        self._queue = EventQueue()        
        from pydsl.Identifier import FunctionNetworkClientId
        if isinstance(idname, str):
            self._ecuid = FunctionNetworkClientId(idname, parentpath)
            if eventserver != None:
                self._parent.registerInstance(self._ecuid, self)
            return
        elif idname == None:
            if True or eventserver == None: # FIXME
                self._ecuid = FunctionNetworkClientId("Main")
                return
        raise TypeError("idname for FunctionNetworkClient: " + str(idname))

    @property
    def ecuid(self):
        """Eventclient unique id"""
        return self._ecuid

    def __str__(self):
        return "<FunctionNetworkClient ecuid: " + self.ecuid.name + " parent: " + str(self._parent) + ">"
    
    def emitToServer(self, msgid:int, content):
        assert(self._parent)
        from pydsl.Abstract import Event
        self.emit(Event(self.ecuid, self._parent.ecuid, msgid, content))

    def emitToSelf(self, msgid:int, content):
        from pydsl.Abstract import Event
        self.emit(Event(self.ecuid, self.ecuid, msgid, content))

    from pydsl.Abstract import Event
    def emit(self, event:Event):
        """Emit an event"""
        assert(self._parent)
        self._parent.handleEvent(event)

    def receiveEvent(self, event):
        """ Receives a message """
        result = self._onReceiveEvent(event)
        #self.__event.set()
        return result

    @abstractmethod
    def _onReceiveEvent(self, event):
        pass

    def changeParent(self, eventserver):
        """Changes to new parent eventmanager"""
        if self._parent:
            self._parent.unregisterInstance(self.ecuid.name)
        self._parent = eventserver
        self._parent.registerInstance(self.ecuid.name, self)

class FunctionNetworkServer(threading.Thread):
    """Allow Function subscription and to send asynchronous events like 
        - a statement doesn't belong to a grammar
        - Unexpected processing error
        - Successful processing
       """
    def __init__(self, parent = None, uid = None):
        threading.Thread.__init__(self)
        self.__instancedic = {}
        import queue
        self.__pendantevent = queue.Queue()
        self.parent = parent
        self.setDaemon(True)
        assert(not parent or not uid)
        self.__ecuid = uid
        if uid == None and parent == None:
            from pydsl.Identifier import FunctionNetworkClientId
            self.__ecuid = FunctionNetworkClientId("Main")

    @property
    def ecuid(self):
        if self.__ecuid == None:
            return self.parent.ecuid
        return self.__ecuid

    def registerInstance(self, ecuid, instance:FunctionNetworkClient):
        if not ecuid:
            import random
            ecuid = str(random.randint(1, 99999999999))
            LOG.warning("registerInstance: asigned random ecuid")
        LOG.debug("registerInstance: registering " + str(ecuid))
        if ecuid in self.__instancedic:
            LOG.error("RegisterInstance duplicated instance: "+ str(ecuid))
            raise NameError #Already exists
        LOG.debug("registerInstance: registered " + str(ecuid))
        self.__instancedic[ecuid] = instance

    def unregisterInstance(self, ecuid:str):
        del self.__instancedic[ecuid]

    def handleEvent(self, event):
        """Event sent from client"""
        self.__pendantevent.put(event)

    def run(self):
        """ Thread execution block"""
        while True:
            event = self.__pendantevent.get()
            if self.parent and event.destination == self.parent.ecuid:
                self.parent.handleEvent(event)
            else:
                self.__instancedic[event.destination].receiveEvent(event)                    

class HostFunctionNetwork(metaclass = ABCMeta):
    """An interface for T that acts as Function Network host"""
    def __init__(self):
        from pydsl.Function.Function import Function
        if not isinstance(self, Function):
            raise TypeError
        self._server = FunctionNetworkServer(self)
        self._hostT = {}
        #self._varstack = VarStack()

    def _initHostT(self, namedic):
        """Inits aux GTs. if a requested aux GT isn't connected, This function will create it"""
        from pydsl.Memory.Storage.Loader import load_transformer
        for title, gttype in namedic.items():
            print(self._server)
            self._hostT[title] = load_transformer(gttype, eventmanager = self._server, ecuid = title) 
            LOG.debug("loaded " + str(title) + "auxT")

    @abstractmethod
    def handleEvent(self, event):
        """Handle message as server.
        Should check how to handle message before sending to server"""
        pass

    @abstractmethod
    def registerInstance(self, ecuid, clientinstance):
        pass

