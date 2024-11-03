# LammpsInputBuilder

[![LIB CI/CD](https://github.com/madreher/lammpsinputbuilder/actions/workflows/ci.yml/badge.svg)](https://github.com/madreher/lammpsinputbuilder/actions/workflows/ci.yml)
[![Coverage badge](https://raw.githubusercontent.com/madreher/lammpsinputbuilder/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/madreher/lammpsinputbuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)
![PyLint](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/madreher/bc29e267d35fad12ca2de2bd7138ecfc/raw/test.json)
[![pypi version](https://img.shields.io/pypi/v/lammpsinputbuilder)](https://pypi.org/project/lammpsinputbuilder/)

## TLDR

LammpsInputBuilder (or LIB) is a Python library designed to generate Lammps inputs from a molecular model, a forcefield, and a high level definition of a simulation workflow.

The goal is to provide an API able to create a Lammps input and data scripts to load a molecular model, assign a forcefield to it, and execute a sequence of operations. The current implementation supports ReaxFF and Rebo potentials for the model defintion, with the possibility to extend to other types of forcefields later on. 

Operations are organized in Sections, where each section is organized around typically but not necessary a time integration operations (minimize, nve, run 0, etc). Each Section can be extended to added addition computations (fix, compute, etc) running at the same time of the main time integration operation. 

With this organization, the main objectives of LammpsInputBuilder are:
- Provide an easy way to generate base Lammps input scripts via a simple Python API
- Create a reusable library of common Sections types to easily chain common operations without having to copy Lammps code
- Make is possible for external tools to generate Lammps inputs via a JSON representation of a workflow (under construction)

Here is a simple example (`examples/tldr.py`) on how to load a molecular model, assign a reax potential to it, and minimize the model: 
```
    from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
    from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
    from lammpsinputbuilder.workflow_builder import WorkflowBuilder
    from lammpsinputbuilder.section import IntegratorSection
    from lammpsinputbuilder.integrator import MinimizeIntegrator, MinimizeStyle

    modelData = Path('benzene.xyz')
    forcefield = Path('ffield.reax.Fe_O_C_H.reax') 

    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(modelData, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder()
    workflow.set_typed_molecular_system(typedMolecule)

    # Create a minimization Section 
    sectionMin = IntegratorSection(
        integrator=MinimizeIntegrator(
            integrator_name="Minimize",
            style=MinimizeStyle.CG, 
            etol=0.01,
            ftol=0.01, 
            maxiter=100, 
            maxeval=10000))
    workflow.add_section(sectionMin)

    # Generate the inputs
    job_folder = workflow.generate_inputs()
```

## Installation

The easiest way to get the latest release is via Pypi. You can install LammpsInputBuilder as follows:

```
# Create a virtual environment
python3 -m venv lammpsinputbuilder
source lammpsinputbuilder/bin/activate

# Install LammpsInputBuilder
pip3 install lammpsinputbuilder
```

Alternatively, if you would like the latest dev build (unstable), you may install LammpsInputBuilder from source as well:
```
# Create a virtual environment
python3 -m venv lammpsinputbuilder
source lammpsinputbuilder/bin/activate

git clone git@github.com:madreher/LammpsInputBuilder.git 
cd LammpsInputBuilder
pip3 install -e .
```

## Documentation 

The user documentation can be found [here](docs/user_doc.md). This page will provide detailed explanations on the different concepts introduced by LammpsInputBuilder and how to build reusable simulation workflows.

A few notes for maintainers are also available [here](docs/dev_doc.md).
