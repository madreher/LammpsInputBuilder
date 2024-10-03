from lammpsinputbuilder.integrator import *
from lammpsinputbuilder.types import GlobalInformation
import pytest

def test_NVEIntegrator():
    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)
    assert integrator.get_integrator_name() == "myIntegrator"
    assert integrator.get_group_name() == "all"
    assert integrator.get_nb_steps() == 1000

    obj_dict = integrator.to_dict()
    assert obj_dict["class_name"] == "NVEIntegrator"
    assert obj_dict["id_name"] == "myIntegrator"
    assert obj_dict["group_name"] == "all"
    assert obj_dict["nb_steps"] == 1000

    integrator2 = NVEIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.get_integrator_name() == "myIntegrator"
    assert integrator2.get_group_name() == "all"
    assert integrator2.get_nb_steps() == 1000

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == "fix myIntegrator all nve\n"
    assert integrator.add_run_commands() == "run 1000\n"
    assert integrator.add_undo_commands() == "unfix myIntegrator\n"

def test_RunZeroIntegrator():
    integrator = RunZeroIntegrator(integrator_name="myIntegrator")
    assert integrator.get_integrator_name() == "myIntegrator"

    obj_dict = integrator.to_dict()
    assert obj_dict["class_name"] == "RunZeroIntegrator"
    assert obj_dict["id_name"] == "myIntegrator"

    integrator2 = RunZeroIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.get_integrator_name() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == ""
    assert integrator.add_run_commands() == "run 0\n"
    assert integrator.add_undo_commands() == ""

def test_MinimizeIntegrator():
    integrator = MinimizeIntegrator(integrator_name="myIntegrator", style=MinimizeStyle.CG, etol=0.02, ftol=0.03, maxiter=400, maxeval=50000)
    assert integrator.get_integrator_name() == "myIntegrator"
    assert integrator.get_minimize_style() == MinimizeStyle.CG
    assert integrator.get_etol() == 0.02
    assert integrator.get_ftol() == 0.03
    assert integrator.get_maxiter() == 400
    assert integrator.get_maxeval() == 50000

    obj_dict = integrator.to_dict()
    assert obj_dict["class_name"] == "MinimizeIntegrator"
    assert obj_dict["id_name"] == "myIntegrator"
    assert obj_dict["style"] == MinimizeStyle.CG.value
    assert obj_dict["etol"] == 0.02
    assert obj_dict["ftol"] == 0.03
    assert obj_dict["maxiter"] == 400
    assert obj_dict["maxeval"] == 50000

    integrator2 = MinimizeIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.get_integrator_name() == "myIntegrator"
    assert integrator2.get_minimize_style() == MinimizeStyle.CG
    assert integrator2.get_etol() == 0.02
    assert integrator2.get_ftol() == 0.03
    assert integrator2.get_maxiter() == 400
    assert integrator2.get_maxeval() == 50000

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == ""
    runCmds = integrator.add_run_commands().splitlines()
    assert runCmds[0] == "min_style cg"
    assert runCmds[1] == "minimize 0.02 0.03 400 50000"
    assert integrator.add_undo_commands() == ""

def test_MultipassIntegrator():
    integrator = MultipassMinimizeIntegrator(integrator_name="myIntegrator")
    assert integrator.get_integrator_name() == "myIntegrator"

    obj_dict = integrator.to_dict()
    assert obj_dict["class_name"] == "MultipassMinimizeIntegrator"
    assert obj_dict["id_name"] == "myIntegrator"

    integrator2 = MultipassMinimizeIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.get_integrator_name() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == ""
    assert integrator.add_run_commands() == """min_style      cg
minimize       1.0e-10 1.0e-10 10000 100000
min_style      hftn
minimize       1.0e-10 1.0e-10 10000 100000
min_style      sd
minimize       1.0e-10 1.0e-10 10000 100000
variable       i loop 100
label          loop1
variable       ene_min equal pe
variable       ene_min_i equal ${ene_min}
min_style      cg
minimize       1.0e-10 1.0e-10 10000 100000
min_style      hftn
minimize       1.0e-10 1.0e-10 10000 100000
min_style      sd
minimize       1.0e-10 1.0e-10 10000 100000
variable       ene_min_f equal pe
variable       ene_diff equal ${ene_min_i}-${ene_min_f}
print          "Delta_E = ${ene_diff}"
if             "${ene_diff}<1e-6" then "jump SELF break1"
print          "Loop_id = $i"
next           i
jump           SELF loop1
label          break1
variable       i delete\n"""
    assert integrator.add_undo_commands() == ""

def test_ManualIntegrator():
    integrator = ManualIntegrator(integrator_name="myIntegrator", cmd_do="do", cmd_undo="undo", cmd_run="run")
    assert integrator.get_integrator_name() == "myIntegrator"

    assert integrator.get_do_commands() == "do"
    assert integrator.get_undo_commands() == "undo"
    assert integrator.get_run_commands() == "run"

    obj_dict = integrator.to_dict()
    assert obj_dict["class_name"] == "ManualIntegrator"
    assert obj_dict["id_name"] == "myIntegrator"
    assert obj_dict["cmd_do"] == "do"
    assert obj_dict["cmd_undo"] == "undo"
    assert obj_dict["cmd_run"] == "run"

    integrator2 = ManualIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.get_integrator_name() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == "do\n"
    assert integrator.add_run_commands() == "run\n"
    assert integrator.add_undo_commands() == "undo\n"

def test_wrong_name():
    with pytest.raises(ValueError):
        obj = ManualIntegrator(integrator_name="&&&", cmd_do="do", cmd_undo="undo", cmd_run="run")
        del obj