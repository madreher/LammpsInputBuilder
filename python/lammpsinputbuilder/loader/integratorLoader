import copy 

from lammpsinputbuilder.integrator import * 

class IntegratorLoader():
    def __init__(self) -> None:
            pass

    def dictToIntegrator(self, d:dict, version:int=0):
        integratorTable = {}
        integratorTable[RunZeroIntegrator.__name__] = RunZeroIntegrator()
        integratorTable[NVEIntegrator.__name__] = NVEIntegrator()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in integratorTable.keys():
            raise RuntimeError(f"Unknown Integrator class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(integratorTable[className])
        obj.fromDict(d, version)

        return obj