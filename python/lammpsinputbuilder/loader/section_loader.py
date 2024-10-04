"""Module faciliating the instanciation of Section classes."""

import copy

from lammpsinputbuilder.section import IntegratorSection, RecursiveSection, InstructionsSection
from lammpsinputbuilder.templates.template_section import TemplateSection
from lammpsinputbuilder.templates.minimize_template import MinimizeTemplate


class SectionLoader():
    def __init__(self) -> None:
        pass

    def dict_to_section(self, d: dict, version: int = 0):
        section_table = {}
        section_table[IntegratorSection.__name__] = IntegratorSection()
        section_table[RecursiveSection.__name__] = RecursiveSection()
        section_table[InstructionsSection.__name__] = InstructionsSection()
        section_table[TemplateSection.__name__] = TemplateSection()
        section_table[MinimizeTemplate.__name__] = MinimizeTemplate()

        if "class_name" not in d:
            raise RuntimeError(f"Missing 'class_name' key in {d}.")
        class_name = d["class_name"]
        if class_name not in section_table:
            raise RuntimeError(f"Unknown Section class {class_name}.")
        # Create a copy of the base object, and we will update the settings of
        # the object from the dictionary
        obj = copy.deepcopy(section_table[class_name])
        obj.from_dict(d, version)

        return obj
