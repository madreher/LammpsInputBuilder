import pytest

from lammpsinputbuilder.integrator import RunZeroIntegrator, NVEIntegrator, \
    MinimizeIntegrator, MinimizeStyle, MultipassMinimizeIntegrator
from lammpsinputbuilder.loader.integrator_loader import IntegratorLoader
from lammpsinputbuilder.group import AllGroup

def test_load_runzero_integrator():
    obj = RunZeroIntegrator(integrator_name="testIntegrator")

    obj_dict = obj.to_dict()

    loader = IntegratorLoader()
    obj2 = loader.dict_to_integrator(obj_dict, version=0)
    assert isinstance(obj2, RunZeroIntegrator)
    assert obj2.get_integrator_name() == "testIntegrator"


def test_load_nve_integrator():
    obj = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)

    obj_dict = obj.to_dict()

    loader = IntegratorLoader()
    obj2 = loader.dict_to_integrator(obj_dict, version=0)
    assert isinstance(obj2, NVEIntegrator)
    assert obj2.get_integrator_name() == "myIntegrator"
    assert obj2.get_group_name() == "all"
    assert obj2.get_nb_steps() == 1000


def test_load_minimize_integrator():
    integrator = MinimizeIntegrator(
        integrator_name="myIntegrator",
        style=MinimizeStyle.CG,
        etol=0.02,
        ftol=0.03,
        maxiter=400,
        maxeval=50000)

    obj_dict = integrator.to_dict()

    loader = IntegratorLoader()
    obj2 = loader.dict_to_integrator(obj_dict, version=0)
    assert isinstance(obj2, MinimizeIntegrator)
    assert obj2.get_integrator_name() == "myIntegrator"
    assert obj2.get_minimize_style() == MinimizeStyle.CG
    assert obj2.get_etol() == 0.02
    assert obj2.get_ftol() == 0.03
    assert obj2.get_maxiter() == 400
    assert obj2.get_maxeval() == 50000

def test_load_multipass_minimize_integrator():
    integrator = MultipassMinimizeIntegrator(integrator_name="myIntegrator")

    obj_dict = integrator.to_dict()

    loader = IntegratorLoader()
    obj2 = loader.dict_to_integrator(obj_dict, version=0)
    assert isinstance(obj2, MultipassMinimizeIntegrator)
    assert obj2.get_integrator_name() == "myIntegrator"

def test_load_no_class_integrator():
    obj = MinimizeIntegrator(
        integrator_name="myIntegrator",
        style=MinimizeStyle.CG,
        etol=0.02,
        ftol=0.03,
        maxiter=400,
        maxeval=50000)

    obj_dict = obj.to_dict()
    del obj_dict["class_name"]

    with pytest.raises(RuntimeError):
        loader = IntegratorLoader()
        obj2 = loader.dict_to_integrator(obj_dict, version=0)
        del obj2

def test_load_unknown_class_integrator():
    obj = MinimizeIntegrator(
        integrator_name="myIntegrator",
        style=MinimizeStyle.CG,
        etol=0.02,
        ftol=0.03,
        maxiter=400,
        maxeval=50000)

    obj_dict = obj.to_dict()
    obj_dict["class_name"] = "unknown"

    with pytest.raises(RuntimeError):
        loader = IntegratorLoader()
        obj2 = loader.dict_to_integrator(obj_dict, version=0)
        del obj2