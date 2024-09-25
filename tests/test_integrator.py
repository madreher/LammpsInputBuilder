from lammpsinputbuilder.integrator import *
from lammpsinputbuilder.types import GlobalInformation
import pytest

def test_NVEIntegrator():
    integrator = NVEIntegrator(integratorName="myIntegrator", group=AllGroup(), nbSteps=1000)
    assert integrator.getIntegratorName() == "myIntegrator"
    assert integrator.getGroupName() == "all"
    assert integrator.getNbSteps() == 1000

    objDict = integrator.toDict()
    assert objDict["class"] == "NVEIntegrator"
    assert objDict["integratorName"] == "myIntegrator"
    assert objDict["groupName"] == "all"
    assert objDict["nbSteps"] == 1000

    integrator2 = NVEIntegrator()
    integrator2.fromDict(objDict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"
    assert integrator2.getGroupName() == "all"
    assert integrator2.getNbSteps() == 1000

    info = GlobalInformation()
    assert integrator.addDoCommands(info) == "fix myIntegrator all nve\n"
    assert integrator.addRunCommands() == "run 1000\n"
    assert integrator.addUndoCommands() == "unfix myIntegrator\n"

def test_RunZeroIntegrator():
    integrator = RunZeroIntegrator(integratorName="myIntegrator")
    assert integrator.getIntegratorName() == "myIntegrator"

    objDict = integrator.toDict()
    assert objDict["class"] == "RunZeroIntegrator"
    assert objDict["integratorName"] == "myIntegrator"

    integrator2 = RunZeroIntegrator()
    integrator2.fromDict(objDict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.addDoCommands(info) == ""
    assert integrator.addRunCommands() == "run 0\n"
    assert integrator.addUndoCommands() == ""

def test_MinimizeIntegrator():
    integrator = MinimizeIntegrator(integratorName="myIntegrator", style=MinimizeStyle.CG, etol=0.02, ftol=0.03, maxiter=400, maxeval=50000)
    assert integrator.getIntegratorName() == "myIntegrator"
    assert integrator.getMinimizeStyle() == MinimizeStyle.CG
    assert integrator.getEtol() == 0.02
    assert integrator.getFtol() == 0.03
    assert integrator.getMaxiter() == 400
    assert integrator.getMaxeval() == 50000

    objDict = integrator.toDict()
    assert objDict["class"] == "MinimizeIntegrator"
    assert objDict["integratorName"] == "myIntegrator"
    assert objDict["style"] == MinimizeStyle.CG.value
    assert objDict["etol"] == 0.02
    assert objDict["ftol"] == 0.03
    assert objDict["maxiter"] == 400
    assert objDict["maxeval"] == 50000

    integrator2 = MinimizeIntegrator()
    integrator2.fromDict(objDict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"
    assert integrator2.getMinimizeStyle() == MinimizeStyle.CG
    assert integrator2.getEtol() == 0.02
    assert integrator2.getFtol() == 0.03
    assert integrator2.getMaxiter() == 400
    assert integrator2.getMaxeval() == 50000

    info = GlobalInformation()
    assert integrator.addDoCommands(info) == ""
    runCmds = integrator.addRunCommands().splitlines()
    assert runCmds[0] == "min_style cg"
    assert runCmds[1] == "minimize 0.02 0.03 400 50000"
    assert integrator.addUndoCommands() == ""

def test_MultipassIntegrator():
    integrator = MultipassMinimizeIntegrator(integratorName="myIntegrator")
    assert integrator.getIntegratorName() == "myIntegrator"

    objDict = integrator.toDict()
    assert objDict["class"] == "MultipassMinimizeIntegrator"
    assert objDict["integratorName"] == "myIntegrator"

    integrator2 = MultipassMinimizeIntegrator()
    integrator2.fromDict(objDict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.addDoCommands(info) == ""
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
    assert integrator.addUndoCommands() == ""

def test_ManualIntegrator():
    integrator = ManualIntegrator(integratorName="myIntegrator", cmdDo="do", cmdUndo="undo", cmdRun="run")
    assert integrator.getIntegratorName() == "myIntegrator"

    assert integrator.getDoCommands() == "do"
    assert integrator.getUndoCommands() == "undo"
    assert integrator.getRunCommands() == "run"

    objDict = integrator.toDict()
    assert objDict["class"] == "ManualIntegrator"
    assert objDict["integratorName"] == "myIntegrator"
    assert objDict["cmdDo"] == "do"
    assert objDict["cmdUndo"] == "undo"
    assert objDict["cmdRun"] == "run"

    integrator2 = ManualIntegrator()
    integrator2.fromDict(objDict, version=0)
    assert integrator2.getIntegratorName() == "myIntegrator"

    info = GlobalInformation()
    assert integrator.addDoCommands(info) == "do\n"
    assert integrator.addRunCommands() == "run\n"
    assert integrator.addUndoCommands() == "undo\n"

