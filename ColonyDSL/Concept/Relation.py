#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from ColonyDSL.Abstract import Indexable

class Rel:
    """Relation class or whatever"""
    def __init__(self, identifier, content):
        self.content = content
        self.identifier = identifier

    def __contains__(self, key):
        return key in self.content

class Relation:
    """Relation instance"""
    def __init__(self, relation:"Rel", roledict:dict):
        if isinstance(relation, str):
            #call load_rel
            raise NotImplementedError
        for key in roledict:
            assert(key in relation)
        self.roledict = roledict #which concepts compounds the relations (and their roles) {"noun":Person,"object":blabla}
        self.relation = relation 
        
    def __str__(self):
        return "(" + str(self.identifier) + "," + str(self.rules) + ")"

    @staticmethod
    def generate_identifier(relation, roledict): 
        """static method to avoid unnecessary instantiation"""
        newroledic = {}
        for key in roledict:
            newroledic[key] = str(roledict[key])
        return str(newroledic) + str(relation) #FIXME: Random order makes identifier unpredictable

    @property
    def summary(self):
        from ColonyDSL.Abstract import InmutableDict
        newdic = {}
        for key in self.roledict:
            newdic[key] = str(self.roledict[key])
        result =  {"iclass":"Relation", "rel":str(self.relation), "concepts":tuple(self.roledict.values()), "roledict":InmutableDict(newdic)}
        return result
