from setuptools import setup, find_packages
setup(name='pydsl',
      version='0.0.1',
      description='Python Domain Specific Language Tools',
      author='Nestor Arocha',
      author_email='nesaro@gmail.com',
      url='https://github.com/nesaro/pydsl',
      packages = find_packages(exclude=['tests','tests.*']),
      scripts=['bin/extract.py', 'bin/translate.py','bin/check.py', 'bin/manager.py', 'bin/guess.py', 'bin/validate.py', 'bin/parts.py'],
      install_requires=['ply'],
      package_dir={'pydsl.contrib': 'pydsl/contrib'},
      package_data={'pydsl.contrib': ['board/*.board','grammar/*.re','grammar/*.bnf','dict/*.dict']},
     )

