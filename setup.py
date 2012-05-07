from setuptools import setup
import glob

setup(name='ColonyDSL',
      version='0.1',
      description='?',
      author='Nestor Arocha',
      author_email='nesaro@gmail.com',
      url='https://github.com/nesaro/colony',
      packages=['ColonyDSL', 'ColonyDSL/Type',  'ColonyDSL/Type/Grammar/' , 'ColonyDSL/Type/Grammar/Parser/', 'ColonyDSL/Interaction/', 'ColonyDSL/Memory/', 'ColonyDSL/Memory/Storage/', 'ColonyDSL/Memory/Storage/Directory/', 'ColonyDSL/Function/', 'ColonyDSL/Function/Transformer/', 'ColonyDSL/Concept/', 'ColonyDSL/Memory/Search/'],
      scripts=['bin/extract.py', 'bin/translate.py','bin/check.py','bin/search.py', 'bin/guess.py', 'bin/convert.py', 'bin/info.py', 'bin/validate.py', 'bin/parts.py'],
     )

