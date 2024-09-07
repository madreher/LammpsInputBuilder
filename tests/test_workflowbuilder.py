import pytest

from pathlib import Path
import shutil

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, Forcefield, MoleculeFileFormat
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecule
from lammpsinputbuilder.workflowBuilder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection 
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.fileIO import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.group import AllGroup

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

    # Create a NVE Section
    section = IntegratorSection(integrator=NVEIntegrator())
    pos = DumpTrajectoryFileIO(fileIOName="fulltrajectory", addDefaultFields=True, interval=10, group=AllGroup())
    section.addFileIO(pos)
    bonds = ReaxBondFileIO(fileIOName="bonds", interval=10, group=AllGroup())
    section.addFileIO(bonds)
    thermo = ThermoFileIO(fileIOName="thermo", addDefaultFields=True, interval=10)
    section.addFileIO(thermo)

    workflow.addSection(section)

    # Generate the inputs
    jobFolder = workflow.generateInputs()

    assert jobFolder is not None
    assert (jobFolder / "molecule.XYZ").is_file()
    assert (jobFolder / typedMolecule.getLammpsDataFileName()).is_file()
    assert (jobFolder / "model.data").is_file()
    assert (jobFolder / "model.data.temp").is_file()

    print("Job folder: ", jobFolder)

    #shutil.rmtree(jobFolder, ignore_errors=True)

if __name__ == "__main__":
    test_workflowBuilder()