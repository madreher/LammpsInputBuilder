from pathlib import Path

import pytest

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection 
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.group import AllGroup

def test_workflow_builder():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typed_molecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder()
    workflow.set_typed_molecular_system(typed_molecule)

    # Create a NVE Section
    section = IntegratorSection(integrator=NVEIntegrator())
    pos = DumpTrajectoryFileIO(fileio_name="fulltrajectory",
                               add_default_fields=True, interval=10, group=AllGroup())
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
    assert (job_folder / typed_molecule.get_lammps_data_filename()).is_file()
    assert (job_folder / "model.data").is_file()
    assert (job_folder / "model.data.temp").is_file()

    print("Job folder: ", job_folder)

    #shutil.rmtree(job_folder, ignore_errors=True)

def test_workflow_builder_dict():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typed_molecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder()
    workflow.set_typed_molecular_system(typed_molecule)

    # Create a NVE Section
    section = IntegratorSection(integrator=NVEIntegrator())
    pos = DumpTrajectoryFileIO(fileio_name="fulltrajectory",
                               add_default_fields=True, interval=10, group=AllGroup())
    section.add_fileio(pos)
    bonds = ReaxBondFileIO(fileio_name="bonds", interval=10, group=AllGroup())
    section.add_fileio(bonds)
    thermo = ThermoFileIO(fileio_name="thermo", add_default_fields=True, interval=10)
    section.add_fileio(thermo)

    workflow.add_section(section)

    dict_obj = workflow.to_dict()
    assert dict_obj["molecular_system"]["class_name"] == "ReaxTypedMolecularSystem"
    assert dict_obj["sections"][0]["class_name"] == "IntegratorSection"
    assert dict_obj["sections"][0]["integrator"]["class_name"] == "NVEIntegrator"

    workflow2 = WorkflowBuilder()
    workflow2.from_dict(dict_obj, version=0)
    assert workflow2.get_sections()[0].get_integrator().get_integrator_name() == "NVEID"

if __name__ == "__main__":
    test_workflow_builder()
