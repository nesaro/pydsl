#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger("Message")

class EventQueue: #FIXME: May we use the memory abstraction for this class??
    """A queue for messages for clients"""
    def __init__(self):
        self.msgdictid = {}

    from pydsl.Abstract import Event
    def append(self, event:Event):
        """Adds a message to queue"""
        msgid = event.msgid
        if not msgid in self.msgdictid:
            self.msgdictid[msgid] = {}
        if not event.source in self.msgdictid[msgid]:
            self.msgdictid[msgid][event.source] = []
        self.msgdictid[msgid][event.source].append(event.msg)

    def __getitem__(self, msgid:int):
        return self.msgdictid[msgid]

    def getBySource(self, source):
        result = []
        for msgdic in self.msgdictid.values():
            if source in msgdic:
                result.append(msgdic[source])
        return result

    from pydsl.Identifier import FunctionNetworkClientId
    def getBySourceAndId(self, source:FunctionNetworkClientId, msgid):
        return self.__getitem__(msgid)[source]

    def getResultsByMask(self, sourcelist, msgid:int):
        """get all results msg given a mask. Only returns dict if all results is available"""
        try:
            msgdic = self.__getitem__(msgid)
        except KeyError:
            return {}
        result = {}
        for element in sourcelist:
            if element not in msgdic or not msgdic[element][0]: #assume only 1 element
                return {}
            result[element] = msgdic[element][0]
        return result

    def getErrorById(self, msgid:int):
        """get all results msg given a mask. Only returns dict if all results is available"""
        try:
            msgdic = self.__getitem__(msgid)
        except KeyError:
            return None
        for element in msgdic.values():
            from pydsl.Function.Function import Error
            if isinstance(element[0], Error):  #FIXME We assume there is only one error
                return element[0]
        return None

    def __delitem__(self, msgid):
        del self.msgdictid[msgid]



