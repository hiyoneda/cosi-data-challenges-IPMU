# Imports:
from setuptools import setup, find_packages

# Setup:
setup(
    name='cosi_dc',
    version="dev",
    url='https://github.com/cositools/cosi-data-challenges.git',
    author='COSI Team',
    author_email='christopher.m.karwin@nasa.gov',
    packages=find_packages(),
    description = "Pipeline for data challenge simulations.",
    entry_points = {"console_scripts":["new_sim = cosi_dc.make_new_sim:main"]}
)
