import pytest

from lammpsinputbuilder.section import InstructionsSection
from lammpsinputbuilder.types import GlobalInformation, LammpsUnitSystem
from lammpsinputbuilder.instructions import ResetTimestepInstruction

import json
def test_instructions_section_accessors():

    section = InstructionsSection(section_name="test")

    instr = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    section.add_instruction(instr)

    assert section.get_section_name() == "test"
    assert len(section.get_instructions()) == 1

def test_instructions_section_dict():

    section = InstructionsSection(section_name="test")

    instr = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    section.add_instruction(instr)

    d = section.to_dict()

    print(json.dumps(d, indent=4))

    assert d == {
    "class_name": "InstructionsSection",
    "id_name": "test",
    "instructions": [
        {
            "class_name": "ResetTimestepInstruction",
            "id_name": "myInstruction",
            "new_timestep": 10
        }
    ]
}
    
    section2 = InstructionsSection()
    section2.from_dict(d, version=0)

    assert section2.get_section_name() == "test"
    assert len(section2.get_instructions()) == 1

    assert section2.to_dict() == d

def test_instructions_section_commands():

    section = InstructionsSection(section_name="test")

    instr = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    section.add_instruction(instr)

    global_info = GlobalInformation()
    global_info.set_unit_style(LammpsUnitSystem.REAL)

    result = section.add_all_commands(global_information=global_info)

    #pylint: disable=line-too-long
    assert result == """#### START SECTION test ########################################################
reset_timestep 10
#### END SECTION test ##########################################################
"""
