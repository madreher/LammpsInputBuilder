"""Module faciliating the instanciation of Integrator classes."""

import copy

from lammpsinputbuilder.integrator import NVEIntegrator, RunZeroIntegrator, \
    MinimizeIntegrator, MultipassMinimizeIntegrator, ManualIntegrator


class IntegratorLoader():
    def __init__(self) -> None:
        pass

    def dict_to_integrator(self, d: dict, version: int = 0):
        integrator_table = {}
        integrator_table[RunZeroIntegrator.__name__] = RunZeroIntegrator()
        integrator_table[NVEIntegrator.__name__] = NVEIntegrator()
        integrator_table[MinimizeIntegrator.__name__] = MinimizeIntegrator()
        integrator_table[MultipassMinimizeIntegrator.__name__] = MultipassMinimizeIntegrator()
        integrator_table[ManualIntegrator.__name__] = ManualIntegrator()

        if "class_name" not in d:
            raise RuntimeError(f"Missing 'class_name' key in {d}.")
        class_name = d["class_name"]
        if class_name not in integrator_table:
            raise RuntimeError(f"Unknown Integrator class {class_name}.")
        # Create a copy of the base object, and we will update the settings of
        # the object from the dictionary
        obj = copy.deepcopy(integrator_table[class_name])
        obj.from_dict(d, version)

        return obj
