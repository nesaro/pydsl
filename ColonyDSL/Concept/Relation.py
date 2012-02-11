#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from ColonyDSL.Abstract import Indexable

class Relation:
    """A concept"""
    def __init__(self, relation:"Concept", roledict:dict):
        self.roledict = roledict #which concepts compounds the relations (and their roles) {"noun":Person,"object":blabla}
        self.relation = relation 
        self.identifier = self.__identifier()
        
    def __str__(self):
        return "(" + str(self.identifier) + "," + str(self.rules) + ")"

    @staticmethod
    def generate_identifier(relation, roledict): 
        """static method to avoid unnecessary instantiation"""
        newroledic = {}
        for key in roledict:
            newroledic[key] = str(roledict[key])
        return str(newroledic) + str(relation)

    def __identifier(self) -> str:
        """Returns a unique identifier"""
        return self.generate_identifier(self.relation, self.roledict)

    @property
    def summary(self):
        from ColonyDSL.Abstract import InmutableDict
        newdic = {}
        for key in self.roledict:
            newdic[key] = str(self.roledict[key])
        result =  {"iclass":"Relation", "identifier":str(self.identifier) ,"relation":str(self.relation), "concepts":tuple(self.roledict.values()), "roledict":InmutableDict(newdic)}
        return result
