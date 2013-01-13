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

"""
Stores logs into a mongo database
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging


def input_file_generator(filename):
    with open(filename,'r') as f:
        while True:
            content = f.readline()
            if content:
                yield content
            else:
                import time
                time.sleep(1)


process_list = [
    {'input':{'type':'file','location':'/var/log/syslog'},
     'filter':'echo',
     'output':{'type':'stdout'}},
    {'input':{'type':'file','location':'/home/nesaro/repo/pydsl/LICENSE'},
     'filter':'echo',
     'output':{'type':'stdout'}},
]

def inputgenerator_factory(type, **kwargs):
    if type == "file":
        return input_file_generator(kwargs['location'])
    else:
        raise TypeError


def outputgenerator_factory(type, **kwargs):
    if type == "stdout":
        return lambda x:print(x)
    else:
        raise TypeError


def executeprocess(proc):
    from pydsl.Memory.Loader import load
    input_generator = inputgenerator_factory(**proc['input'])
    converter = load(proc['filter'])
    output = outputgenerator_factory(**proc['output'])
    for unit in input_generator:
        output(converter(unit)['output'])

if __name__ == "__main__":
    import argparse
    TUSAGE = "usage: %(prog)s [options]"
    PARSER = argparse.ArgumentParser(usage = TUSAGE)
    PARSER.add_argument("-d", "--debuglevel", action="store", type=int, dest="debuglevel", help="Sets debug level")
    ARGS = PARSER.parse_args()
    DEBUGLEVEL = ARGS.debuglevel or logging.WARNING
    logging.basicConfig(level = DEBUGLEVEL)
    from multiprocessing import Pool
    p = Pool(processes=max(len(process_list),2))
    #result = [p.apply_async(executeprocess,process) for process in process_list]
    p.map(executeprocess, process_list)

