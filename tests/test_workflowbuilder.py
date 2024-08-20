import pytest

from pathlib import Path
import shutil

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, Forcefield, MoleculeFileFormat
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecule
from lammpsinputbuilder.workflowBuilder import WorkflowBuilder

def test_workflowBuilder():
    # Create a molecule
    moleculePath = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(moleculePath, forcefieldPath)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder ()
    workflow.setTypedMolecule(typedMolecule)

    # Generate the inputs
    jobFolder = workflow.generateInputs()

    assert jobFolder is not None
    assert (jobFolder / "molecule.XYZ").is_file()
    assert (jobFolder / typedMolecule.getLammpsDataFileName()).is_file()
    assert (jobFolder / "model.data").is_file()
    assert (jobFolder / "model.data.temp").is_file()

    shutil.rmtree(jobFolder, ignore_errors=True)