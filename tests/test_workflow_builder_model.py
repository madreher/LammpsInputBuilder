import json 
from pathlib import Path

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection 
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.group import AllGroup

from lammpsinputbuilder.model.workflow_builder_model import WorkflowBuilderModel

def test_workflow_builder_model():
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

    obj_dict = workflow.to_dict()
    obj_dict_str = json.dumps(obj_dict, indent=4)

    obj_model1 = WorkflowBuilderModel.model_validate_json(obj_dict_str)
    assert obj_model1.header.major_version == 1
    assert obj_model1.header.minor_version == 0
    assert obj_model1.header.format == "WorkflowBuilder"

    assert obj_model1.sections[0].class_name == "IntegratorSection"
    assert obj_model1.sections[0].integrator.class_name == "NVEIntegrator"
    assert obj_model1.sections[0].fileios[0].class_name == "DumpTrajectoryFileIO"
    assert obj_model1.sections[0].fileios[1].class_name == "ReaxBondFileIO"
    assert obj_model1.sections[0].fileios[2].class_name == "ThermoFileIO"

    # Populate the model from the dictionnary
    obj_model2 = WorkflowBuilderModel(**obj_dict)
    assert obj_model2.header.major_version == 1
    assert obj_model2.header.minor_version == 0
    assert obj_model2.header.format == "WorkflowBuilder"

    assert obj_model2.sections[0].class_name == "IntegratorSection"
    assert obj_model2.sections[0].integrator.class_name == "NVEIntegrator"
    assert obj_model2.sections[0].fileios[0].class_name == "DumpTrajectoryFileIO"
    assert obj_model2.sections[0].fileios[1].class_name == "ReaxBondFileIO"
    assert obj_model2.sections[0].fileios[2].class_name == "ThermoFileIO"
