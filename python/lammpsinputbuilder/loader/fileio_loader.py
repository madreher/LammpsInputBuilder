"""Module faciliating the instanciation of FileIO classes."""

import copy

from lammpsinputbuilder.fileio import ReaxBondFileIO, \
    DumpTrajectoryFileIO, ThermoFileIO, ManualFileIO


class FileIOLoader():
    def __init__(self) -> None:
        pass

    def dict_to_fileio(self, d: dict, version: int = 0):
        file_io_table = {}
        file_io_table[ReaxBondFileIO.__name__] = ReaxBondFileIO()
        file_io_table[DumpTrajectoryFileIO.__name__] = DumpTrajectoryFileIO()
        file_io_table[ThermoFileIO.__name__] = ThermoFileIO()
        file_io_table[ManualFileIO.__name__] = ManualFileIO()

        if "class_name" not in d:
            raise RuntimeError(f"Missing 'class_name' key in {d}.")
        class_name = d["class_name"]
        if class_name not in file_io_table:
            raise RuntimeError(f"Unknown FileIO class {class_name}.")
        # Create a copy of the base object, and we will update the settings of
        # the object from the dictionary
        obj = copy.deepcopy(file_io_table[class_name])
        obj.from_dict(d, version)

        return obj
