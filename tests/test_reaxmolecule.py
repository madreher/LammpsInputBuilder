import pytest

from pathlib import Path
import tempfile
from uuid import uuid4
import os
import shutil

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod, Forcefield, MoleculeFileFormat
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecule


def test_emptyReaxMolecule():
    # Create an empty molecule 
    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    assert typedMolecule.getForcefieldType() == Forcefield.REAX
    assert typedMolecule.getBoundingBoxStyle() == BoundingBoxStyle.PERIODIC
    assert typedMolecule.getElectrostaticMethod() == ElectrostaticMethod.QEQ
    
    assert not typedMolecule.isModelLoaded()

    assert typedMolecule.getMoleculeContent() == ""
    assert typedMolecule.getMoleculeFormat() is None 
    assert typedMolecule.getMoleculePath() is None

    assert typedMolecule.getForcefieldContent() == ""
    assert typedMolecule.getForcefieldPath() is None



def test_reaxMoleculeFromFile():
    # Create a molecule
    moleculePath = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(moleculePath, forcefieldPath)

    assert typedMolecule.getForcefieldType() == Forcefield.REAX
    assert typedMolecule.getBoundingBoxStyle() == BoundingBoxStyle.PERIODIC
    assert typedMolecule.getElectrostaticMethod() == ElectrostaticMethod.QEQ
    
    assert typedMolecule.isModelLoaded()

    assert typedMolecule.getMoleculeContent() != ""
    assert typedMolecule.getMoleculeFormat() == MoleculeFileFormat.XYZ
    assert typedMolecule.getMoleculePath()  == moleculePath

    assert typedMolecule.getForcefieldContent() != ""
    assert typedMolecule.getForcefieldPath() == forcefieldPath


def test_reaxMoleculeFromStrings():
    # Create a molecule
    moleculePath = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    moleculeContent = ""
    potentialContent = ""
    with open(moleculePath, 'r') as f:
        moleculeContent = f.read()
    with open(forcefieldPath, 'r') as f:
        potentialContent = f.read()

    typedMolecule.loadFromStrings(moleculeContent, MoleculeFileFormat.XYZ, potentialContent, forcefieldPath, moleculePath)

    assert typedMolecule.getForcefieldType() == Forcefield.REAX
    assert typedMolecule.getBoundingBoxStyle() == BoundingBoxStyle.PERIODIC
    assert typedMolecule.getElectrostaticMethod() == ElectrostaticMethod.QEQ
    
    assert typedMolecule.isModelLoaded()

    assert typedMolecule.getMoleculeContent() == moleculeContent
    assert typedMolecule.getMoleculeFormat() == MoleculeFileFormat.XYZ
    assert typedMolecule.getMoleculePath()  == moleculePath

    assert typedMolecule.getForcefieldContent() == potentialContent
    assert typedMolecule.getForcefieldPath() == forcefieldPath


def test_moleculeToDict():
    # Create a molecule
    moleculePath = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(moleculePath, forcefieldPath)

    result = typedMolecule.toDict()

    assert result["class"] == "ReaxTypedMolecule"
    assert result["electrostaticMethod"] == ElectrostaticMethod.QEQ.value
    assert result["forcefieldPath"] == Path(str(forcefieldPath))
    assert result["moleculePath"] == Path(str(moleculePath))
    assert result["moleculeFormat"] == MoleculeFileFormat.XYZ.value
    assert result["forcefieldContent"] == typedMolecule.getForcefieldContent()
    assert result["moleculeContent"] == typedMolecule.getMoleculeContent()

def test_moleculeToDictToMolecule():
    # Create a molecule
    moleculePath = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(moleculePath, forcefieldPath)

    dict1 = typedMolecule.toDict()

    typedMolecule2 = ReaxTypedMolecule()
    typedMolecule2.fromDict(dict1)

    assert typedMolecule.toDict() == typedMolecule2.toDict()

def test_moleculeToJobFolder():
    # Create a molecule
    moleculePath = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefieldPath=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )

    typedMolecule.loadFromFile(moleculePath, forcefieldPath)

    jobFolder = Path(tempfile.gettempdir()) / str(uuid4())
    os.makedirs(jobFolder)

    moleculeHolder = typedMolecule.generateLammpsDataFile(jobFolder)
    inputPath = typedMolecule.generateLammpsInputFile(jobFolder, moleculeHolder)

    assert moleculeHolder is not None
    assert inputPath == jobFolder / "lammps.input"
    assert (jobFolder / "molecule.XYZ").is_file()
    assert (jobFolder / typedMolecule.getLammpsDataFileName()).is_file()
    assert (jobFolder / "model.data").is_file()
    assert (jobFolder / "model.data.temp").is_file()

    shutil.rmtree(jobFolder, ignore_errors=True)
