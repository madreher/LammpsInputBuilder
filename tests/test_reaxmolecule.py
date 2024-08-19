import pytest

from pathlib import Path

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecule
from lammpsinputbuilder.workflowBuilder import WorkflowBuilder

def test_dataToJobFolder():
    

    # Create a molecule
    modelData = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax',
        moleculePath=modelData,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder ()
    workflow.setTypedMolecule(typedMolecule)

    # Generate the inputs
    jobFolder = workflow.generateInputs()

    assert jobFolder.is_dir()
    assert (jobFolder / "model.data").is_file()
    assert (jobFolder / "model.data.temp").is_file()
    assert (jobFolder / "lammps.input").is_file()
    assert (jobFolder / "molecule.XYZ").is_file()