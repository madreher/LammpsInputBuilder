from lammpsinputbuilder.templates.minimize_template import MinimizeTemplate, MinimizeStyle
from lammpsinputbuilder.group import EmptyGroup
from lammpsinputbuilder.section import IntegratorSection
from lammpsinputbuilder.types import GlobalInformation, LammpsUnitSystem

def test_minimize_template_accessors():
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
    assert template.get_minimize_style() == MinimizeStyle.CG
    assert template.get_etol() == 0.02
    assert template.get_ftol() == 0.03
    assert template.get_maxiter() == 400
    assert template.get_maxeval() == 50000
    assert template.get_use_anchors() is True
    assert template.anchor_group.get_group_name() == EmptyGroup().get_group_name()
    assert template.get_section_name() == "test"

def test_minimize_template_dict():
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

    assert template.to_dict() == {
    "class_name": "MinimizeTemplate",
    "id_name": "test",
    "fileios": [],
    "extensions": [],
    "groups": [],
    "instructions": [],
    "style": 0,
    "etol": 0.02,
    "ftol": 0.03,
    "maxiter": 400,
    "maxeval": 50000,
    "use_anchors": True,
    "anchor_group": {
        "class_name": "EmptyGroup",
        "id_name": "empty"
    }
}

    template2 = MinimizeTemplate()
    template2.from_dict(template.to_dict(), version=0)
    assert template2.to_dict() == template.to_dict()

def test_minimize_template_commands():
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

    section_list = template.generate_sections()

    assert len(section_list) == 1
    assert isinstance(section_list[0], IntegratorSection)
    assert section_list[0].get_section_name() == "minimizationTemplate"
    assert section_list[0].get_integrator().get_integrator_name() == "minimizer"
    assert section_list[0].get_integrator().get_minimize_style() == MinimizeStyle.CG
    assert section_list[0].get_integrator().get_etol() == 0.02
    assert section_list[0].get_integrator().get_ftol() == 0.03
    assert section_list[0].get_integrator().get_maxiter() == 400
    assert section_list[0].get_integrator().get_maxeval() == 50000

    assert len(section_list[0].get_fileios()) == 0
    assert len(section_list[0].get_groups()) == 1
    assert len(section_list[0].get_instructions()) == 0
    assert len(section_list[0].get_extensions()) == 1

    global_info = GlobalInformation()
    global_info.set_unit_style(LammpsUnitSystem.REAL)

    result = template.add_all_commands(global_information=global_info)

    #pylint: disable=line-too-long
    assert result == """#### START Section test ########################################################
#### START Groups DECLARATION ##################################################
#### END Groups DECLARATION ####################################################
#### START Extensions DECLARATION ##############################################
#### END Extensions DECLARATION ################################################
#### START IOs DECLARATION #####################################################
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
#### END IOs DECLARATION #######################################################
#### START Extensions REMOVAL ##################################################
#### END Extensions DECLARATION ################################################
#### START Groups REMOVAL ######################################################
#### END Groups DECLARATION ####################################################
#### END Section test ##########################################################
"""
    