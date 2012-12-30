from setuptools import setup, find_packages
setup(name='pydsl',
      version='0.0.1',
      description='Python Domain Specific Language Tools',
      author='Nestor Arocha',
      author_email='nesaro@gmail.com',
      url='https://github.com/nesaro/pydsl',
      packages = find_packages(),
      scripts=['bin/extract.py', 'bin/translate.py','bin/check.py', 'bin/manager.py', 'bin/guess.py', 'bin/validate.py', 'bin/parts.py'],
      install_requires=['ply'],
      package_data={'pydsl.contrib.grammar':['*.re', '*.bnf'] ,
          'pydsl.contrib.board':['*.board'],
          'pydsl.contrib.dict':['*.dict'],
          'pydsl.contrib.list':['*.py']}
     )

