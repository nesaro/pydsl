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

"""Python Transformers"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .Channel import HostChannel
import logging
LOG = logging.getLogger("PythonTransformer")

class PythonTransformer(HostChannel):
    """ Python function based transformer """
    def __init__(self, inputdic, outputdic, function):
        HostChannel.__init__(self, inputdic, outputdic)
        self._function = function

    def __call__(self, ibdic):
        for inputkey in self.inputchanneldic.keys():
            if inputkey not in ibdic:
                raise KeyError("Key %s not found in inputdic" % inputkey)
        for dickey in ibdic.keys():
            if not self.inputchanneldic[dickey].check(ibdic[dickey]):
                raise ValueError("Invalid value %s for input %s (%s)" % (ibdic[dickey], dickey, self))
        from pydsl.Exceptions import ProcessingError
        result = self._functionwrapper(ibdic)
        return result

    def _functionwrapper(self, wdict):
        """Wraps function call, to add parammeters if required"""
        LOG.debug("PythonTransformer._functionwrapper: begin")
        result = self._function(wdict, self.inputchanneldic, self.outputchanneldic)
        from pydsl.Exceptions import ProcessingError
        if not result:
            raise ProcessingError("Transformer", self)
        for outputgrammarname in self.outputchanneldic.keys():
            LOG.debug("Verifying Grammar name: " + outputgrammarname)
            if not outputgrammarname in result:
                LOG.error("Error while verifying Grammar name:" + outputgrammarname)
                raise ProcessingError("Transformer")

        #Converting to words
        #TODO Process errors like HostPythonTransformer
        return result

    @property
    def summary(self):
        from pydsl.Abstract import InmutableDict
        inputdic = tuple(self.inputdefinition.values())
        outputdic = tuple(self.outputdefinition.values())
        result = {"iclass":"PythonTransformer", "input":inputdic,"output":outputdic}
        return InmutableDict(result)

class HostPythonTransformer(PythonTransformer):
    """Python Function Transformer which can call to other functions"""
    def __init__(self, inputdic, outputdic, auxdic:dict, function):
        PythonTransformer.__init__(self, inputdic, outputdic, function)
        self._hostT = {}
        self._initHostT(auxdic)

    def _initHostT(self, namedic):
        """Inits aux GTs. if a requested aux GT isn't connected, This function will create them"""
        from pydsl.Memory.Storage.Loader import load_transformer
        for title, gttype in namedic.items():
            self._hostT[title] = load_transformer(gttype) 
            LOG.debug("loaded " + str(title) + "auxT")


    def _functionwrapper(self, worddic):
        """Wraps function call, to add parammeters if required"""
        LOG.info("HostPythonTransformer._functionwrapper: begin")
        from pydsl.Exceptions import ProcessingError
        result = self._function(worddic, self._hostT, self.inputchanneldic, self.outputchanneldic)
        if not result:
            raise ProcessingError("Transformer", self)
        for channel in result.keys():
            if not result[channel]: #FIXME: > 1 channel receives an error
                newerror = result[channel]
                return newerror
        return result
