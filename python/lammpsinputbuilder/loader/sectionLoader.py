import copy 

from lammpsinputbuilder.section import * 

class SectionLoader():
    def __init__(self) -> None:
            pass

    def dictToSection(self, d:dict, version:int=0):
        sectionTable = {}
        sectionTable[IntegratorSection.__name__] = IntegratorSection()
        sectionTable[RecusiveSection.__name__] = RecusiveSection()
        sectionTable[CommandsSection.__name__] = CommandsSection()

        if "class" not in d.keys():
            raise RuntimeError(f"Missing 'class' key in {d}.")
        className = d["class"]
        if className not in sectionTable.keys():
            raise RuntimeError(f"Unknown Section class {className}.")
        # Create a copy of the base object, and we will update the settings of the object from the dictionary
        obj = copy.deepcopy(sectionTable[className])
        obj.fromDict(d, version)

        return obj