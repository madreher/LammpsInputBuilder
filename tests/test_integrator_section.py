import pytest

from lammpsinputbuilder.section import IntegratorSection
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.group import AllGroup, IndicesGroup
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, DumpStyle
from lammpsinputbuilder.instructions import SetTimestepInstruction
from lammpsinputbuilder.extensions import MoveExtension
from lammpsinputbuilder.quantities import TimeQuantity, VelocityQuantity
from lammpsinputbuilder.types import GlobalInformation, LammpsUnitSystem

def test_integrator_section_accessors():
    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    section = IntegratorSection(integrator=integrator, section_name="mySection")
    assert section.get_integrator().to_dict() == integrator.to_dict()

    io = DumpTrajectoryFileIO(
        fileio_name="testFile", user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup(), style=DumpStyle.CUSTOM)
    section.add_fileio(io)

    grp = IndicesGroup(group_name="myIndicesGroup", indices=[1, 2, 3])
    section.add_group(grp)
    assert len(section.get_groups()) == 1

    instr = SetTimestepInstruction(
        instruction_name="myInstruction",
        timestep=TimeQuantity(20, "fs"))
    section.add_instruction(instr)
    assert len(section.get_instructions()) == 1

    ext = MoveExtension(
        extension_name="myExtension",
        group=AllGroup(),
        vx=VelocityQuantity(0.0, "angstrom/ps"),
        vy=VelocityQuantity(0.0, "angstrom/ps"),
        vz=VelocityQuantity(0.0, "angstrom/ps"))
    section.add_extension(ext)
    assert len(section.get_extensions()) == 1

def test_integrator_section_dict():
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

    assert section.to_dict() == {
        "class": "IntegratorSection",
        "integrator": {
            "class": "NVEIntegrator",
            "integrator_name": "myIntegrator",
            "group_name": "all",
            "nb_steps": 1000
        },
        "section_name": "mySection",
        "fileios": [{
            "class": "DumpTrajectoryFileIO",
            "fileio_name": "testFile",
            "user_fields": ["a", "b", "c", "element"],
            "add_default_fields": True,
            "interval": 10,
            "group_name": "all",
            "style": DumpStyle.CUSTOM.value
        }],
        "groups": [{
            "class": "IndicesGroup",
            "group_name": "myIndicesGroup",
            "indices": [1, 2, 3]
        }],
        "instructions": [{
            "class": "SetTimestepInstruction",
            "instruction_name": "myInstruction",
            "timestep": {
                "class": "TimeQuantity",
                "magnitude": 20,
                "units": "fs"
            }
        }],
        "extensions": [{
            "class": "MoveExtension",
            "extension_name": "myExtension",
            "group_name": "all",
            "vx": {
                "class": "VelocityQuantity",
                "magnitude": 0,
                "units": "angstrom/ps"
            },
            "vy": {
                "class": "VelocityQuantity",
                "magnitude": 0,
                "units": "angstrom/ps"
            },
            "vz": {
                "class": "VelocityQuantity",
                "magnitude": 0,
                "units": "angstrom/ps"
            }
        }]
    }

    section2 = IntegratorSection()
    section2.from_dict(section.to_dict(), version=0)
    assert section2.get_integrator().to_dict() == integrator.to_dict()

def test_integrator_section_commands():
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

    global_info = GlobalInformation()
    global_info.set_unit_style(LammpsUnitSystem.REAL)
    global_info.set_element_table({1: "C"})

    result = section.add_all_commands(global_information=global_info)

    assert result == """################# START SECTION mySection #################

################# START Groups DECLARATION #################
group myIndicesGroup id 1 2 3
################# END Groups DECLARATION #################
################# START Extensions DECLARATION #################
fix myExtension all move linear 0.0 0.0 0.0
################# END Extensions DECLARATION #################
################# START IOs DECLARATION #################
dump testFile all custom 10 dump.testFile.lammpstrj id type x y z a b c element
dump_modify testFile sort id
dump_modify testFile element C
################# END IOs DECLARATION #################
################# START INTEGRATOR DECLARATION #################
fix myIntegrator all nve
################# END INTEGRATOR DECLARATION #################
################# START RUN INTEGRATOR FOR SECTION mySection #################
run 1000
################# END RUN INTEGRATOR FOR SECTION mySection #################
################# START INTEGRATOR REMOVAL #################
unfix myIntegrator
################# END INTEGRATOR REMOVAL #################
################# START IO REMOVAL #################
undump testFile
################# END IOs DECLARATION #################
################# START Extensions REMOVAL #################
unfix myExtension
################# END Extensions DECLARATION #################
################# START Groups REMOVAL #################
group myIndicesGroup delete
################# END Groups DECLARATION #################
################# END SECTION mySection #################

"""
