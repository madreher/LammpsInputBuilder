from lammpsinputbuilder.integrator import *
from lammpsinputbuilder.types import GlobalInformation
import pytest

def test_NVEIntegrator():
    integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nbSteps=1000)
    assert integrator.getIntegratorName() == "myIntegrator"
    assert integrator.get_group_name() == "all"
    assert integrator.getNbSteps() == 1000

    obj_dict = integrator.to_dict()
    assert obj_dict["class"] == "NVEIntegrator"
    assert obj_dict["integrator_name"] == "myIntegrator"
    assert obj_dict["group_name"] == "all"
    assert obj_dict["nbSteps"] == 1000

    integrator2 = NVEIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"
    assert integrator2.get_group_name() == "all"
    assert integrator2.getNbSteps() == 1000

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == "fix myIntegrator all nve\n"
    assert integrator.addRunCommands() == "run 1000\n"
    assert integrator.add_undo_commands() == "unfix myIntegrator\n"

def test_RunZeroIntegrator():
    integrator = RunZeroIntegrator(integrator_name="myIntegrator")
    assert integrator.getIntegratorName() == "myIntegrator"

    obj_dict = integrator.to_dict()
    assert obj_dict["class"] == "RunZeroIntegrator"
    assert obj_dict["integrator_name"] == "myIntegrator"

    integrator2 = RunZeroIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == ""
    assert integrator.addRunCommands() == "run 0\n"
    assert integrator.add_undo_commands() == ""

def test_MinimizeIntegrator():
    integrator = MinimizeIntegrator(integrator_name="myIntegrator", style=MinimizeStyle.CG, etol=0.02, ftol=0.03, maxiter=400, maxeval=50000)
    assert integrator.getIntegratorName() == "myIntegrator"
    assert integrator.getMinimizeStyle() == MinimizeStyle.CG
    assert integrator.getEtol() == 0.02
    assert integrator.getFtol() == 0.03
    assert integrator.getMaxiter() == 400
    assert integrator.getMaxeval() == 50000

    obj_dict = integrator.to_dict()
    assert obj_dict["class"] == "MinimizeIntegrator"
    assert obj_dict["integrator_name"] == "myIntegrator"
    assert obj_dict["style"] == MinimizeStyle.CG.value
    assert obj_dict["etol"] == 0.02
    assert obj_dict["ftol"] == 0.03
    assert obj_dict["maxiter"] == 400
    assert obj_dict["maxeval"] == 50000

    integrator2 = MinimizeIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"
    assert integrator2.getMinimizeStyle() == MinimizeStyle.CG
    assert integrator2.getEtol() == 0.02
    assert integrator2.getFtol() == 0.03
    assert integrator2.getMaxiter() == 400
    assert integrator2.getMaxeval() == 50000

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == ""
    runCmds = integrator.addRunCommands().splitlines()
    assert runCmds[0] == "min_style cg"
    assert runCmds[1] == "minimize 0.02 0.03 400 50000"
    assert integrator.add_undo_commands() == ""

def test_MultipassIntegrator():
    integrator = MultipassMinimizeIntegrator(integrator_name="myIntegrator")
    assert integrator.getIntegratorName() == "myIntegrator"

    obj_dict = integrator.to_dict()
    assert obj_dict["class"] == "MultipassMinimizeIntegrator"
    assert obj_dict["integrator_name"] == "myIntegrator"

    integrator2 = MultipassMinimizeIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == ""
    assert integrator.addRunCommands() == """min_style      cg
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
    integrator = ManualIntegrator(integrator_name="myIntegrator", cmdDo="do", cmdUndo="undo", cmdRun="run")
    assert integrator.getIntegratorName() == "myIntegrator"

    assert integrator.getDoCommands() == "do"
    assert integrator.getUndoCommands() == "undo"
    assert integrator.getRunCommands() == "run"

    obj_dict = integrator.to_dict()
    assert obj_dict["class"] == "ManualIntegrator"
    assert obj_dict["integrator_name"] == "myIntegrator"
    assert obj_dict["cmdDo"] == "do"
    assert obj_dict["cmdUndo"] == "undo"
    assert obj_dict["cmdRun"] == "run"

    integrator2 = ManualIntegrator()
    integrator2.from_dict(obj_dict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.add_do_commands(info) == "do\n"
    assert integrator.addRunCommands() == "run\n"
    assert integrator.add_undo_commands() == "undo\n"

