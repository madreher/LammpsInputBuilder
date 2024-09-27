import pytest

from pathlib import Path
import shutil

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, Forcefield, MoleculeFileFormat
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflowBuilder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection 
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.fileIO import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.group import AllGroup

def test_workflowBuilder():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(molecule_path, forcefieldPath)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder ()
    workflow.set_typed_molecular_system(typedMolecule)

    # Create a NVE Section
    section = IntegratorSection(integrator=NVEIntegrator())
    pos = DumpTrajectoryFileIO(fileio_name="fulltrajectory", add_default_fields=True, interval=10, group=AllGroup())
    section.add_fileio(pos)
    bonds = ReaxBondFileIO(fileio_name="bonds", interval=10, group=AllGroup())
    section.add_fileio(bonds)
    thermo = ThermoFileIO(fileio_name="thermo", add_default_fields=True, interval=10)
    section.add_fileio(thermo)

    workflow.add_section(section)

    # Generate the inputs
    job_folder = workflow.generate_inputs()

    assert job_folder is not None
    assert (job_folder / "molecule.XYZ").is_file()
    assert (job_folder / typedMolecule.getLammpsDataFileName()).is_file()
    assert (job_folder / "model.data").is_file()
    assert (job_folder / "model.data.temp").is_file()

    print("Job folder: ", job_folder)

    #shutil.rmtree(job_folder, ignore_errors=True)

if __name__ == "__main__":
    test_workflowBuilder()