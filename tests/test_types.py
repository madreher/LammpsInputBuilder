import pytest
import lammpsinputbuilder.types

def test_file_format():

    assert lammpsinputbuilder.types.get_molecule_file_format_from_extension(".xyz") == lammpsinputbuilder.types.MoleculeFileFormat.XYZ
    assert lammpsinputbuilder.types.get_molecule_file_format_from_extension(".XYZ") == lammpsinputbuilder.types.MoleculeFileFormat.XYZ
    assert lammpsinputbuilder.types.get_molecule_file_format_from_extension(".mol2") == lammpsinputbuilder.types.MoleculeFileFormat.MOL2
    assert lammpsinputbuilder.types.get_molecule_file_format_from_extension(".MOL2") == lammpsinputbuilder.types.MoleculeFileFormat.MOL2
    assert lammpsinputbuilder.types.get_molecule_file_format_from_extension(".lammpstrj") == lammpsinputbuilder.types.MoleculeFileFormat.LAMMPS_DUMP_TEXT

    with pytest.raises(NotImplementedError):
        lammpsinputbuilder.types.get_molecule_file_format_from_extension(".txt")

def test_get_extension_from_molecule_file_format():

    assert lammpsinputbuilder.types.get_extension_from_molecule_file_format(lammpsinputbuilder.types.MoleculeFileFormat.XYZ) == ".xyz"
    assert lammpsinputbuilder.types.get_extension_from_molecule_file_format(lammpsinputbuilder.types.MoleculeFileFormat.MOL2) == ".mol2"
    assert lammpsinputbuilder.types.get_extension_from_molecule_file_format(lammpsinputbuilder.types.MoleculeFileFormat.LAMMPS_DUMP_TEXT) == ".lammpstrj"

    with pytest.raises(NotImplementedError):
        lammpsinputbuilder.types.get_extension_from_molecule_file_format(None)

def test_get_forcefield_from_extension():

    assert lammpsinputbuilder.types.get_forcefield_from_extension(".reax") == lammpsinputbuilder.types.Forcefield.REAX
    assert lammpsinputbuilder.types.get_forcefield_from_extension(".REAX") == lammpsinputbuilder.types.Forcefield.REAX
    assert lammpsinputbuilder.types.get_forcefield_from_extension(".airebo") == lammpsinputbuilder.types.Forcefield.AIREBO
    assert lammpsinputbuilder.types.get_forcefield_from_extension(".airebo-m") == lammpsinputbuilder.types.Forcefield.AIREBOM
    assert lammpsinputbuilder.types.get_forcefield_from_extension(".rebo") == lammpsinputbuilder.types.Forcefield.REBO

    with pytest.raises(NotImplementedError):
        lammpsinputbuilder.types.get_forcefield_from_extension(".txt")

def test_get_extension_from_forcefield():

    assert lammpsinputbuilder.types.get_extension_from_forcefield(lammpsinputbuilder.types.Forcefield.REAX) == ".reax"
    assert lammpsinputbuilder.types.get_extension_from_forcefield(lammpsinputbuilder.types.Forcefield.AIREBO) == ".airebo"
    assert lammpsinputbuilder.types.get_extension_from_forcefield(lammpsinputbuilder.types.Forcefield.REBO) == ".rebo"
    assert lammpsinputbuilder.types.get_extension_from_forcefield(lammpsinputbuilder.types.Forcefield.AIREBOM) == ".airebo-m"

    with pytest.raises(NotImplementedError):
        lammpsinputbuilder.types.get_extension_from_forcefield(None)