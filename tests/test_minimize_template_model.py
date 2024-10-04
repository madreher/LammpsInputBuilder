import json

from lammpsinputbuilder.templates.minimize_template import MinimizeTemplate, MinimizeStyle
from lammpsinputbuilder.group import EmptyGroup

from lammpsinputbuilder.model.template_model import MinimizeTemplateModel

def test_minimize_template_model():
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

    obj_dict = template.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = MinimizeTemplateModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "MinimizeTemplate"
    assert obj_model1.id_name == "test"
    assert obj_model1.style == MinimizeStyle.CG
    assert obj_model1.etol == 0.02
    assert obj_model1.ftol == 0.03
    assert obj_model1.maxiter == 400
    assert obj_model1.maxeval == 50000
    assert obj_model1.use_anchors is True
    assert obj_model1.anchor_group.class_name == "EmptyGroup"
    assert obj_model1.anchor_group.id_name == "empty"

    # Populate the model from the dictionnary
    obj_model2 = MinimizeTemplateModel(**obj_dict)
    assert obj_model2.class_name == "MinimizeTemplate"
    assert obj_model2.id_name == "test"
    assert obj_model2.style == MinimizeStyle.CG
    assert obj_model2.etol == 0.02
    assert obj_model2.ftol == 0.03
    assert obj_model2.maxiter == 400
    assert obj_model2.maxeval == 50000
    assert obj_model2.use_anchors is True
    assert obj_model2.anchor_group.class_name == "EmptyGroup"
    assert obj_model2.anchor_group.id_name == "empty"
