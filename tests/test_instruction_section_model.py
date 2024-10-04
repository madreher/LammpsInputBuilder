import json

from lammpsinputbuilder.section import InstructionsSection
from lammpsinputbuilder.instructions import ResetTimestepInstruction

from lammpsinputbuilder.model.section_model import InstructionsSectionModel

def test_instruction_section_model():
    section = InstructionsSection(section_name="test")

    instr = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    section.add_instruction(instr)

    obj_dict = section.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = InstructionsSectionModel.model_validate_json(obj_dict_str)

    assert obj_model1.class_name == "InstructionsSection"
    assert obj_model1.id_name == "test"
    assert obj_model1.instructions[0].class_name == "ResetTimestepInstruction"
    assert obj_model1.instructions[0].new_timestep == 10

    # Populate the model from the dictionnary
    obj_model2 = InstructionsSectionModel(**obj_dict)
    assert obj_model2.class_name == "InstructionsSection"
    assert obj_model2.id_name == "test"
    assert obj_model2.instructions[0].class_name == "ResetTimestepInstruction"
    assert obj_model2.instructions[0].new_timestep == 10