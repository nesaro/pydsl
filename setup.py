from setuptools import setup, find_packages
setup(name='pydsl',
      version='0.5.3',
      description='Python Domain Specific Language Tools',
      author='Nestor Arocha',
      author_email='nesaro@gmail.com',
      url='https://github.com/nesaro/pydsl',
      packages = find_packages(exclude=['tests.*']),
      install_requires=['ply'],
      package_dir={'pydsl.contrib': 'pydsl/contrib'},
      package_data={'pydsl.contrib': ['grammar/*.re','grammar/*.bnf','grammar/*.parsley','dict/*.dict']},
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3',
          ],
     )

