from setuptools import setup, find_packages
import glob

setup(name='pydsl',
      version='0.1',
      description='Python Domain Specific Language Tools',
      author='Nestor Arocha',
      author_email='nesaro@gmail.com',
      url='https://github.com/nesaro/pydsl',
      packages = find_packages(),
      scripts=['bin/extract.py', 'bin/translate.py','bin/check.py','bin/search.py', 'bin/guess.py', 'bin/info.py', 'bin/validate.py', 'bin/parts.py'],
      requires=['ply']
     )

