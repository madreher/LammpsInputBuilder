import json

from lammpsinputbuilder.section import IntegratorSection
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.instructions import SetTimestepInstruction
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, DumpStyle
from lammpsinputbuilder.group import IndicesGroup, AllGroup
from lammpsinputbuilder.extensions import MoveExtension
from lammpsinputbuilder.quantities import TimeQuantity, VelocityQuantity

from lammpsinputbuilder.model.section_model import IntegratorSectionModel


def test_integrator_section_model():
    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    section = IntegratorSection(integrator=integrator, section_name="mySection")

    io = DumpTrajectoryFileIO(
        fileio_name="testFile", user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup(), style=DumpStyle.CUSTOM)
    section.add_fileio(io)

    grp = IndicesGroup(group_name="myIndicesGroup", indices=[1, 2, 3])
    section.add_group(grp)

    instr = SetTimestepInstruction(
        instruction_name="myInstruction",
        timestep=TimeQuantity(20, "fs"))
    section.add_instruction(instr)

    ext = MoveExtension(
        extension_name="myExtension",
        group=AllGroup(),
        vx=VelocityQuantity(0.0, "angstrom/ps"),
        vy=VelocityQuantity(0.0, "angstrom/ps"),
        vz=VelocityQuantity(0.0, "angstrom/ps"))
    section.add_extension(ext)

    post_ext = MoveExtension(
        extension_name="myPostExtension",
        group=AllGroup(),
        vx=VelocityQuantity(0.0, "angstrom/ps"),
        vy=VelocityQuantity(0.0, "angstrom/ps"),
        vz=VelocityQuantity(0.0, "angstrom/ps"))
    section.add_post_extension(post_ext)

    obj_dict = section.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = IntegratorSectionModel.model_validate_json(obj_dict_str)

    assert obj_model1.integrator.id_name == "myIntegrator"
    assert obj_model1.integrator.group_name == "all"
    assert obj_model1.integrator.nb_steps == 1000
    assert obj_model1.fileios[0].id_name == "testFile"
    assert obj_model1.fileios[0].user_fields == ["a", "b", "c", "element"]
    assert obj_model1.fileios[0].add_default_fields is True
    assert obj_model1.fileios[0].interval == 10
    assert obj_model1.fileios[0].group_name == "all"
    assert obj_model1.fileios[0].style == DumpStyle.CUSTOM.value
    assert obj_model1.groups[0].id_name == "myIndicesGroup"
    assert obj_model1.groups[0].indices == [1, 2, 3]
    assert obj_model1.instructions[0].id_name == "myInstruction"
    assert obj_model1.instructions[0].timestep.magnitude == 20
    assert obj_model1.instructions[0].timestep.units == "fs"
    assert obj_model1.extensions[0].id_name == "myExtension"
    assert obj_model1.extensions[0].group_name == "all"
    assert obj_model1.extensions[0].vx.magnitude == 0.0
    assert obj_model1.extensions[0].vx.units == "angstrom/ps"
    assert obj_model1.extensions[0].vy.magnitude == 0.0
    assert obj_model1.extensions[0].vy.units == "angstrom/ps"
    assert obj_model1.extensions[0].vz.magnitude == 0.0
    assert obj_model1.extensions[0].vz.units == "angstrom/ps"
    assert obj_model1.post_extensions[0].id_name == "myPostExtension"
    assert obj_model1.post_extensions[0].group_name == "all"
    assert obj_model1.post_extensions[0].vx.magnitude == 0.0
    assert obj_model1.post_extensions[0].vx.units == "angstrom/ps"
    assert obj_model1.post_extensions[0].vy.magnitude == 0.0
    assert obj_model1.post_extensions[0].vy.units == "angstrom/ps"
    assert obj_model1.post_extensions[0].vz.magnitude == 0.0
    assert obj_model1.post_extensions[0].vz.units == "angstrom/ps"

    # Populate the model from the dictionnary
    obj_model2 = IntegratorSectionModel(**obj_dict)
    assert obj_model2.integrator.id_name == "myIntegrator"
    assert obj_model2.integrator.group_name == "all"
    assert obj_model2.integrator.nb_steps == 1000
    assert obj_model2.fileios[0].id_name == "testFile"
    assert obj_model2.fileios[0].user_fields == ["a", "b", "c", "element"]
    assert obj_model2.fileios[0].add_default_fields is True
    assert obj_model2.fileios[0].interval == 10
    assert obj_model2.fileios[0].group_name == "all"
    assert obj_model2.fileios[0].style == DumpStyle.CUSTOM.value
    assert obj_model2.groups[0].id_name == "myIndicesGroup"
    assert obj_model2.groups[0].indices == [1, 2, 3]
    assert obj_model2.instructions[0].id_name == "myInstruction"
    assert obj_model2.instructions[0].timestep.magnitude == 20
    assert obj_model2.instructions[0].timestep.units == "fs"
    assert obj_model2.extensions[0].id_name == "myExtension"
    assert obj_model2.extensions[0].group_name == "all"
    assert obj_model2.extensions[0].vx.magnitude == 0.0
    assert obj_model2.extensions[0].vx.units == "angstrom/ps"
    assert obj_model2.extensions[0].vy.magnitude == 0.0
    assert obj_model2.extensions[0].vy.units == "angstrom/ps"
    assert obj_model2.extensions[0].vz.magnitude == 0.0
    assert obj_model2.extensions[0].vz.units == "angstrom/ps"
    assert obj_model2.post_extensions[0].id_name == "myPostExtension"
    assert obj_model2.post_extensions[0].group_name == "all"
    assert obj_model2.post_extensions[0].vx.magnitude == 0.0
    assert obj_model2.post_extensions[0].vx.units == "angstrom/ps"
    assert obj_model2.post_extensions[0].vy.magnitude == 0.0
    assert obj_model2.post_extensions[0].vy.units == "angstrom/ps"
    assert obj_model2.post_extensions[0].vz.magnitude == 0.0
    assert obj_model2.post_extensions[0].vz.units == "angstrom/ps"
