from setuptools import find_packages, setup

setup(
    name="lammpsinputbuilder",
    version='0.0.1',
    packages=find_packages(where='python'),
    package_dir={'' : 'python'},
    package_data={"lammpsinputbuilder" : ["lib_units.txt"]},
    install_requires=['ase >= 3.20', 'pint >= 0.17 '],
    license = 'MIT License',
    python_requires='>=3.6',
    author='Matthieu Dreher',
    author_email='dreher.matthieu@gmail.com',
    maintainer='Matthieu Dreher',
    maintainer_email='dreher.matthieu@gmail.com',
    description='Lammps Input Builder, a python library and API designed to generate Lammps inputs from a molecule and workflow high level definition.'
)