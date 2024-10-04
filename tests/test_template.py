import pytest

from lammpsinputbuilder.templates.minimize_template import MinimizeTemplate, MinimizeStyle
from lammpsinputbuilder.templates.template_section import TemplateSection
from lammpsinputbuilder.group import EmptyGroup, AllGroup
from lammpsinputbuilder.instructions import ResetTimestepInstruction
from lammpsinputbuilder.types import GlobalInformation, LammpsUnitSystem
from lammpsinputbuilder.extensions import SetForceExtension
from lammpsinputbuilder.quantities import ForceQuantity
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, DumpStyle

def test_template_accessors():
    template = TemplateSection(section_name="test")

    assert template.get_section_name() == "test"

    grp = EmptyGroup()
    template.add_group(grp)
    assert len(template.get_groups()) == 1
    assert template.get_groups()[0].get_group_name() == grp.get_group_name()
    assert isinstance(template.get_groups()[0], EmptyGroup)

    instr = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    template.add_instruction(instr)
    assert len(template.get_instructions()) == 1
    assert template.get_instructions()[0].get_instruction_name() == instr.get_instruction_name()
    assert isinstance(template.get_instructions()[0], ResetTimestepInstruction)

    ext = SetForceExtension(extension_name="myExtension", group=AllGroup(), fx=ForceQuantity(0.0, "(kcal/mol)/angstrom"))
    template.add_extension(ext)
    assert len(template.get_extensions()) == 1
    assert template.get_extensions()[0].get_extension_name() == ext.get_extension_name()
    assert isinstance(template.get_extensions()[0], SetForceExtension)

    io = DumpTrajectoryFileIO(
        fileio_name="testFile", user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup(), style=DumpStyle.CUSTOM)
    template.add_fileio(io)
    assert len(template.get_fileios()) == 1
    assert template.get_fileios()[0].get_fileio_name() == io.get_fileio_name()
    assert isinstance(template.get_fileios()[0], DumpTrajectoryFileIO)

    with pytest.raises(NotImplementedError):
        template.generate_sections()

def test_template_dict():
    template = TemplateSection(section_name="test")

    grp = EmptyGroup()
    template.add_group(grp)

    instr = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    template.add_instruction(instr)

    ext = SetForceExtension(extension_name="myExtension", group=AllGroup(), fx=ForceQuantity(0.0, "(kcal/mol)/angstrom"))
    template.add_extension(ext)


    io = DumpTrajectoryFileIO(
        fileio_name="testFile", user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup(), style=DumpStyle.CUSTOM)
    template.add_fileio(io)

    assert template.to_dict() == {
        "class_name": "TemplateSection",
        "id_name": "test",
        "fileios": [io.to_dict()],
        "extensions": [ext.to_dict()],
        "groups": [grp.to_dict()],
        "instructions": [instr.to_dict()]
    }

    template2 = TemplateSection()
    template2.from_dict(template.to_dict(), version=0)
    assert template2.to_dict() == template.to_dict()

def test_template_commands():
    template = MinimizeTemplate(
        section_name="test",
        style=MinimizeStyle.CG,
        etol=0.02,
        ftol=0.03,
        maxiter=400,
        maxeval=50000,
        use_anchors=True,
        anchor_group=EmptyGroup()
    )

    grp = EmptyGroup()
    template.add_group(grp)

    instr = ResetTimestepInstruction(
        instruction_name="myInstruction",
        new_timestep=10
    )
    template.add_instruction(instr)

    ext = SetForceExtension(
        extension_name="myExtension",
        group=AllGroup(),
        fx=ForceQuantity(0.0, "(kcal/mol)/angstrom"))
    template.add_extension(ext)


    io = DumpTrajectoryFileIO(
        fileio_name="testFile", user_fields=["a", "b", "c", "element"],
        add_default_fields=True,
        interval=10,
        group=AllGroup(), style=DumpStyle.CUSTOM)
    template.add_fileio(io)


    global_info = GlobalInformation()
    global_info.set_element_table({"H": 1})
    global_info.set_unit_style(LammpsUnitSystem.REAL)

    result = template.add_all_commands(global_information=global_info)

    # Disable line length check
    #pylint: disable=line-too-long
    assert result == """#### START Section test ########################################################
#### START Groups DECLARATION ##################################################
#### END Groups DECLARATION ####################################################
#### START Extensions DECLARATION ##############################################
fix myExtension all setforce 0.0 0.0 0.0
#### END Extensions DECLARATION ################################################
#### START IOs DECLARATION #####################################################
dump testFile all custom 10 dump.testFile.lammpstrj id type x y z a b c element
dump_modify testFile sort id
dump_modify testFile element 1
#### END IOs DECLARATION #######################################################
#### START SECTION minimizationTemplate ########################################
#### START Groups DECLARATION ##################################################
#### END Groups DECLARATION ####################################################
#### START Extensions DECLARATION ##############################################
fix zeroForceAnchor empty setforce 0.0 0.0 0.0
#### END Extensions DECLARATION ################################################
#### START INTEGRATOR DECLARATION ##############################################
#### END INTEGRATOR DECLARATION ################################################
#### START Post Extensions DECLARATION #########################################
#### END Post Extensions DECLARATION ###########################################
#### START IOs DECLARATION #####################################################
#### END IOs DECLARATION #######################################################
#### START RUN INTEGRATOR FOR SECTION minimizationTemplate #####################
min_style cg
minimize 0.02 0.03 400 50000
#### END RUN INTEGRATOR FOR SECTION minimizationTemplate #######################
#### START IO REMOVAL ##########################################################
#### END IOs DECLARATION #######################################################
#### START Post Extensions REMOVAL #############################################
#### END Post Extensions REMOVAL ###############################################
#### START INTEGRATOR REMOVAL ##################################################
#### END INTEGRATOR REMOVAL ####################################################
#### START Extensions REMOVAL ##################################################
unfix zeroForceAnchor
#### END Extensions DECLARATION ################################################
#### START Groups REMOVAL ######################################################
#### END Groups DECLARATION ####################################################
#### END SECTION minimizationTemplate ##########################################
#### START IO REMOVAL ##########################################################
undump testFile
#### END IOs DECLARATION #######################################################
#### START Extensions REMOVAL ##################################################
unfix myExtension
#### END Extensions DECLARATION ################################################
#### START Groups REMOVAL ######################################################
#### END Groups DECLARATION ####################################################
#### END Section test ##########################################################
"""