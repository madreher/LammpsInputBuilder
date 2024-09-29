import pytest

from lammpsinputbuilder.section import IntegratorSection, RecusiveSection
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.group import AllGroup, IndicesGroup
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, DumpStyle
from lammpsinputbuilder.instructions import SetTimestepInstruction
from lammpsinputbuilder.extensions import MoveExtension
from lammpsinputbuilder.quantities import TimeQuantity, VelocityQuantity
from lammpsinputbuilder.types import GlobalInformation, LammpsUnitSystem

def test_recursive_section_accessors():
    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    section = IntegratorSection(integrator=integrator, section_name="mySection")
    assert section.get_integrator().to_dict() == integrator.to_dict()

    recursive_section = RecusiveSection(section_name="recursive")
    recursive_section.add_section(section)

    io = DumpTrajectoryFileIO(
        fileio_name="testFile", user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup(), style=DumpStyle.CUSTOM)
    recursive_section.add_fileio(io)
    assert len(recursive_section.get_fileios()) == 1

    grp = IndicesGroup(group_name="myIndicesGroup", indices=[1, 2, 3])
    recursive_section.add_group(grp)
    assert len(recursive_section.get_groups()) == 1

    instr = SetTimestepInstruction(
        instruction_name="myInstruction",
        timestep=TimeQuantity(20, "fs"))
    recursive_section.add_instruction(instr)
    assert len(recursive_section.get_instructions()) == 1

    ext = MoveExtension(
        extension_name="myExtension",
        group=AllGroup(),
        vx=VelocityQuantity(0.0, "angstrom/ps"),
        vy=VelocityQuantity(0.0, "angstrom/ps"),
        vz=VelocityQuantity(0.0, "angstrom/ps"))
    recursive_section.add_extension(ext)
    assert len(recursive_section.get_extensions()) == 1

def test_recursive_section_dict():
    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    section = IntegratorSection(integrator=integrator, section_name="mySection")
    assert section.get_integrator().to_dict() == integrator.to_dict()

    recursive_section = RecusiveSection(section_name="recursive")
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

    assert recursive_section.to_dict() == {
    "class": "RecusiveSection",
    "section_name": "recursive",
    "sections": [
        {
            "class": "IntegratorSection",
            "section_name": "mySection",
            "integrator": {
                "class": "NVEIntegrator",
                "integrator_name": "myIntegrator",
                "group_name": "all",
                "nb_steps": 1000
            },
            "fileios": [],
            "extensions": [],
            "groups": [],
            "instructions": []
        }
    ],
    "fileios": [
        {
            "class": "DumpTrajectoryFileIO",
            "fileio_name": "testFile",
            "user_fields": [
                "a",
                "b",
                "c",
                "element"
            ],
            "add_default_fields": True,
            "interval": 10,
            "group_name": "all",
            "style": 1
        }
    ],
    "extensions": [
        {
            "class": "MoveExtension",
            "extension_name": "myExtension",
            "group_name": "all",
            "vx": {
                "class": "VelocityQuantity",
                "magnitude": 0.0,
                "units": "angstrom/ps"
            },
            "vy": {
                "class": "VelocityQuantity",
                "magnitude": 0.0,
                "units": "angstrom/ps"
            },
            "vz": {
                "class": "VelocityQuantity",
                "magnitude": 0.0,
                "units": "angstrom/ps"
            }
        }
    ],
    "groups": [
        {
            "class": "IndicesGroup",
            "group_name": "myIndicesGroup",
            "indices": [
                1,
                2,
                3
            ]
        }
    ],
    "instructions": [
        {
            "class": "SetTimestepInstruction",
            "instruction_name": "myInstruction",
            "timestep": {
                "class": "TimeQuantity",
                "magnitude": 20,
                "units": "fs"
            }
        }
    ]
}

    section2 = RecusiveSection()
    section2.from_dict(recursive_section.to_dict(), version=0)

    assert section2.to_dict() == recursive_section.to_dict()

def test_integrator_section_commands():
    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    section = IntegratorSection(integrator=integrator, section_name="mySection")
    assert section.get_integrator().to_dict() == integrator.to_dict()

    recursive_section = RecusiveSection(section_name="recursive")
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

    global_info = GlobalInformation()
    global_info.set_unit_style(LammpsUnitSystem.REAL)
    global_info.set_element_table({1: "C"})

    result = recursive_section.add_all_commands(global_information=global_info)

    assert result == """################# START Section recursive #################
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
################# START SECTION mySection #################

################# START Groups DECLARATION #################
################# END Groups DECLARATION #################
################# START Extensions DECLARATION #################
################# END Extensions DECLARATION #################
################# START IOs DECLARATION #################
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
################# END IOs DECLARATION #################
################# START Extensions REMOVAL #################
################# END Extensions DECLARATION #################
################# START Groups REMOVAL #################
################# END Groups DECLARATION #################
################# END SECTION mySection #################

################# START IO REMOVAL #################
undump testFile
################# END IOs DECLARATION #################
################# START Extensions REMOVAL #################
unfix myExtension
################# END Extensions DECLARATION #################
################# START Groups REMOVAL #################
group myIndicesGroup delete
################# END Groups DECLARATION #################
################# END Section recursive #################
"""
