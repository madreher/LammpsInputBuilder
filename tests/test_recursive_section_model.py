import json

from lammpsinputbuilder.section import IntegratorSection, RecursiveSection
from lammpsinputbuilder.quantities import TimeQuantity, VelocityQuantity
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.group import AllGroup, IndicesGroup
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, DumpStyle
from lammpsinputbuilder.instructions import SetTimestepInstruction
from lammpsinputbuilder.extensions import MoveExtension

from lammpsinputbuilder.model.template_model import RecursiveSectionModel

def test_recursive_section_model():

    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    section = IntegratorSection(integrator=integrator, section_name="mySection")
    assert section.get_integrator().to_dict() == integrator.to_dict()

    recursive_section = RecursiveSection(section_name="recursive")
    recursive_section.add_section(section)

    io = DumpTrajectoryFileIO(
        fileio_name="testFile", user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup(), style=DumpStyle.CUSTOM)
    recursive_section.add_fileio(io)

    grp = IndicesGroup(group_name="myIndicesGroup", indices=[1, 2, 3])
    recursive_section.add_group(grp)


    instr = SetTimestepInstruction(
        instruction_name="myInstruction",
        timestep=TimeQuantity(20, "fs"))
    recursive_section.add_instruction(instr)


    ext = MoveExtension(
        extension_name="myExtension",
        group=AllGroup(),
        vx=VelocityQuantity(0.0, "angstrom/ps"),
        vy=VelocityQuantity(0.0, "angstrom/ps"),
        vz=VelocityQuantity(0.0, "angstrom/ps"))
    recursive_section.add_extension(ext)

    obj_dict = recursive_section.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model = RecursiveSectionModel.model_validate_json(obj_dict_str)

    assert obj_model.id_name == "recursive"
    assert len(obj_model.fileios) == 1
    assert obj_model.fileios[0].id_name == "testFile"
    assert obj_model.fileios[0].user_fields == ["a", "b", "c", "element"]
    assert obj_model.fileios[0].add_default_fields
    assert obj_model.fileios[0].interval == 10
    assert obj_model.fileios[0].group_name == "all"
    assert obj_model.fileios[0].style == DumpStyle.CUSTOM.value

    assert len(obj_model.groups) == 1
    assert obj_model.groups[0].id_name == "myIndicesGroup"
    assert obj_model.groups[0].indices == [1, 2, 3]

    assert len(obj_model.instructions) == 1
    assert obj_model.instructions[0].id_name == "myInstruction"
    assert obj_model.instructions[0].timestep.magnitude == 20
    assert obj_model.instructions[0].timestep.units == "fs"

    assert len(obj_model.extensions) == 1
    assert obj_model.extensions[0].id_name == "myExtension"
    assert obj_model.extensions[0].group_name == "all"
    assert obj_model.extensions[0].vx.magnitude == 0.0
    assert obj_model.extensions[0].vx.units == "angstrom/ps"
    assert obj_model.extensions[0].vy.magnitude == 0.0
    assert obj_model.extensions[0].vy.units == "angstrom/ps"
    assert obj_model.extensions[0].vz.magnitude == 0.0
    assert obj_model.extensions[0].vz.units == "angstrom/ps"

    # Populate the model from the dictionnary
    obj_model2 = RecursiveSectionModel(**obj_dict)
    assert obj_model2.id_name == "recursive"
    assert len(obj_model2.fileios) == 1
    assert obj_model2.fileios[0].id_name == "testFile"
    assert obj_model2.fileios[0].user_fields == ["a", "b", "c", "element"]
    assert obj_model2.fileios[0].add_default_fields
    assert obj_model2.fileios[0].interval == 10
    assert obj_model2.fileios[0].group_name == "all"
    assert obj_model2.fileios[0].style == DumpStyle.CUSTOM.value

    assert len(obj_model2.groups) == 1
    assert obj_model2.groups[0].id_name == "myIndicesGroup"
    assert obj_model2.groups[0].indices == [1, 2, 3]

    assert len(obj_model2.instructions) == 1
    assert obj_model2.instructions[0].id_name == "myInstruction"
    assert obj_model2.instructions[0].timestep.magnitude == 20
    assert obj_model2.instructions[0].timestep.units == "fs"

    assert len(obj_model2.extensions) == 1
    assert obj_model2.extensions[0].id_name == "myExtension"
    assert obj_model2.extensions[0].group_name == "all"
    assert obj_model2.extensions[0].vx.magnitude == 0.0
    assert obj_model2.extensions[0].vx.units == "angstrom/ps"
    assert obj_model2.extensions[0].vy.magnitude == 0.0
    assert obj_model2.extensions[0].vy.units == "angstrom/ps"
    assert obj_model2.extensions[0].vz.magnitude == 0.0
    assert obj_model2.extensions[0].vz.units == "angstrom/ps"