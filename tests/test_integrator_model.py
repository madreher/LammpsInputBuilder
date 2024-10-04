import json 

from lammpsinputbuilder.integrator import RunZeroIntegrator, NVEIntegrator, \
    MinimizeIntegrator, MultipassMinimizeIntegrator, ManualIntegrator, MinimizeStyle
from lammpsinputbuilder.model.integrator_model import RunZeroIntegratorModel, \
    NVEIntegratorModel, MinimizeIntegratorModel, MultiPassMinimizeIntegratorModel, \
    ManualIntegratorModel
from lammpsinputbuilder.group import AllGroup

def test_run_zero_integrator_model():
    obj = RunZeroIntegrator(integrator_name="myIntegrator")

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = RunZeroIntegratorModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "RunZeroIntegrator"
    assert obj_model1.id_name == "myIntegrator"

    # Populate the model from the dictionnary
    obj_model2 = RunZeroIntegratorModel(**obj_dict)
    assert obj_model2.class_name == "RunZeroIntegrator"
    assert obj_model2.id_name == "myIntegrator"

def test_nve_integrator_model():
    obj = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = NVEIntegratorModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "NVEIntegrator"
    assert obj_model1.id_name == "myIntegrator"
    assert obj_model1.group_name == "all"
    assert obj_model1.nb_steps == 1000

    # Populate the model from the dictionnary
    obj_model2 = NVEIntegratorModel(**obj_dict)
    assert obj_model2.class_name == "NVEIntegrator"
    assert obj_model2.id_name == "myIntegrator"
    assert obj_model2.group_name == "all"
    assert obj_model2.nb_steps == 1000

def test_minimize_integrator_model():
    obj = MinimizeIntegrator(integrator_name="myIntegrator", style=MinimizeStyle.CG, etol=0.02, ftol=0.03, maxiter=400, maxeval=50000)

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = MinimizeIntegratorModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "MinimizeIntegrator"
    assert obj_model1.id_name == "myIntegrator"
    assert obj_model1.style == MinimizeStyle.CG
    assert obj_model1.etol == 0.02
    assert obj_model1.ftol == 0.03
    assert obj_model1.maxiter == 400
    assert obj_model1.maxeval == 50000

    # Populate the model from the dictionnary
    obj_model2 = MinimizeIntegratorModel(**obj_dict)
    assert obj_model2.class_name == "MinimizeIntegrator"
    assert obj_model2.id_name == "myIntegrator"
    assert obj_model2.style == MinimizeStyle.CG
    assert obj_model2.etol == 0.02
    assert obj_model2.ftol == 0.03
    assert obj_model2.maxiter == 400

def test_multipass_minimize_integrator_model():
    obj = MultipassMinimizeIntegrator(integrator_name="myIntegrator")

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = MultiPassMinimizeIntegratorModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "MultipassMinimizeIntegrator"
    assert obj_model1.id_name == "myIntegrator"

    # Populate the model from the dictionnary
    obj_model2 = MultiPassMinimizeIntegratorModel(**obj_dict)
    assert obj_model2.class_name == "MultipassMinimizeIntegrator"
    assert obj_model2.id_name == "myIntegrator"

def test_manual_integrator_model():
    obj = ManualIntegrator(integrator_name="myIntegrator", cmd_do="do", cmd_undo="undo", cmd_run="run")

    obj_dict = obj.to_dict()
    obj_dict_str = json.dumps(obj_dict)

    # Check that the json produced by the object matches the model
    obj_model1 = ManualIntegratorModel.model_validate_json(obj_dict_str)
    assert obj_model1.class_name == "ManualIntegrator"
    assert obj_model1.id_name == "myIntegrator"
    assert obj_model1.cmd_do == "do"
    assert obj_model1.cmd_undo == "undo"
    assert obj_model1.cmd_run == "run"

    # Populate the model from the dictionnary
    obj_model2 = ManualIntegratorModel(**obj_dict)
    assert obj_model2.class_name == "ManualIntegrator"
    assert obj_model2.id_name == "myIntegrator"
    assert obj_model2.cmd_do == "do"
    assert obj_model2.cmd_undo == "undo"
    assert obj_model2.cmd_run == "run"
