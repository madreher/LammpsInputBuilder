LAMMPS_INPUT_BUILDER_MAJOR_VERSION = 0
LAMMPS_INPUT_BUILDER_MINOR_VERSION = 1
LAMMPS_INPUT_BUILDER_JSON_MAJOR_VERSION = 1
LAMMPS_INPUT_BUILDER_JSON_MINOR_VERSION = 0

class PackageVersion:
    def __init__(self) -> None:
        pass

    def get_major_lib_version(self) -> int:
        return LAMMPS_INPUT_BUILDER_MAJOR_VERSION

    def get_minor_lib_version(self) -> int:
        return LAMMPS_INPUT_BUILDER_MINOR_VERSION
    
    def get_major_lib_json_version(self) -> int:
        return LAMMPS_INPUT_BUILDER_JSON_MAJOR_VERSION

    def get_minor_lib_json_version(self) -> int:
        return LAMMPS_INPUT_BUILDER_JSON_MINOR_VERSION
