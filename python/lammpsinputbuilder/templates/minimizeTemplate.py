from typing import List
from lammpsinputbuilder.section import Section, IntegratorSection
from lammpsinputbuilder.templates.templateSection import TemplateSection
from lammpsinputbuilder.integrator import MinimizeIntegrator, MinimizeStyle
from lammpsinputbuilder.group import Group, AllGroup
from lammpsinputbuilder.extensions import SetForceExtension
from lammpsinputbuilder.quantities import ForceQuantity

class MinimizeTemplate(TemplateSection):
    def __init__(self, sectionName: str = "minimizeSection", style: MinimizeStyle = MinimizeStyle.CG, etol: float = 0.01, ftol: float = 0.01, maxiter: int = 100, maxeval: int = 10000, useAnchors: bool = False, anchorGroup: Group = AllGroup()) -> None:
        super().__init__(sectionName=sectionName)
        self.style = style
        self.etol = etol
        self.ftol = ftol
        self.maxiter = maxiter
        self.maxeval = maxeval
        self.useAnchors = useAnchors
        # We keep the group object instead of the name because the group object is needed when unrolling the template into base sections
        self.anchorGroup = anchorGroup


    def toDict(self) -> dict:
        result = super().toDict()
        result["class"] = self.__class__.__name__
        result["style"] = self.style.value
        result["etol"] = self.etol
        result["ftol"] = self.ftol
        result["maxiter"] = self.maxiter
        result["maxeval"] = self.maxeval
        result["useAnchors"] = self.useAnchors
        result["anchorGroup"] = self.anchorGroup.toDict()
        return result
    
    def fromDict(self, d: dict, version: int):
        if d["class"] != self.__class__.__name__:
            raise ValueError(f"Expected class {self.__class__.__name__}, got {d['class']}.")
        super().fromDict(d, version=version)
        self.style = MinimizeStyle(d["style"])
        self.etol = d["etol"]
        self.ftol = d["ftol"]
        self.maxiter = d["maxiter"]
        self.maxeval = d["maxeval"]
        self.useAnchors = d["useAnchors"]
        if "anchorGroup" in d:
            from lammpsinputbuilder.loader.groupLoader import GroupLoader
            loader = GroupLoader()

            self.anchorGroup = loader.dictToGroup(d["anchorGroup"])

    def generateSections(self) -> List[Section]:
        section = IntegratorSection("minimizationTemplate", integrator=MinimizeIntegrator("minimizer", style=self.style, etol=self.etol, ftol=self.ftol, maxiter=self.maxiter, maxeval=self.maxeval))
        if self.useAnchors:
            # Minimization is always done on all the atoms. 
            # To create anchors during the minimization, we need to set the force to 0 on the anchor group
            section.addGroup(self.anchorGroup)
            section.addExtension(SetForceExtension(extensionName="zeroForceAnchor", group=self.anchorGroup, fx=ForceQuantity(0.0), fy=ForceQuantity(0.0), fz=ForceQuantity(0.0)))


        return [section]