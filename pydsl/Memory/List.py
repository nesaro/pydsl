#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""ListLibrary"""
from pypository.utils import ImmutableDict
import logging
LOG = logging.getLogger(__name__)
from pypository.List import ListStorage
from pydsl.Alphabet.Definition import Encoding


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class EncodingStorage(ListStorage):

    @staticmethod
    def _generatekey(element):
        return element

    @staticmethod
    def load(index):
        return Encoding(index)

    def generate_all_summaries(self):
        return tuple([ImmutableDict({"identifier": x, "value": x, "iclass": "Encoding"}) for x in self._content])
