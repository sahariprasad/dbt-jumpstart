# from distutils.core import setup
from setuptools import setup

setup(
  name = 'dbtjumpstart',         # How you named your package folder (MyLib)
  packages = ['dbtjumpstart'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package to jumpstart a dbt project',   # Give a short description about your library
  author = 'Hari Prasad SA',                   # Type in your name
  author_email = 'sahariprasad@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/sahariprasad/dbt-starter',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/sahariprasad/dbt-starter/archive/refs/tags/v0.1-alpha.tar.gz',    # I explain this later on
  keywords = ['dbt', 'start'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'openpyxl',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)