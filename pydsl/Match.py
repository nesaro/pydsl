
#!/usr/bin/env python
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


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)


from pydsl.Grammar.Definition import String

class Matcher(object):
    """ Consumes a part of the input, returns the tail as well..."""
    def __init__(self):
        pass

    def __call__(self, value):
        return self.match(value)

    def match(self, value):
        raise NotImplementedError

class StringMatcher(Matcher):
    def __init__(self, definition):
        if isinstance(definition, str):
            definition = String(definition)
        self.definition = definition

    def match(self, value):
        if value.startswith(self.definition.string):
            return value[:len(self.definition.string)], value[len(self.definition.string):]
        raise Exception("No match")


def match_factory(definition):
    if isinstance(definition, String):
        return StringMatcher(definition)

def match(definition, data):
    return match_factory(definition)(data)
