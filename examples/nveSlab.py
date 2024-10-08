from pathlib import Path
import logging

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection, RecursiveSection, InstructionsSection
from lammpsinputbuilder.integrator import NVEIntegrator, MinimizeStyle, RunZeroIntegrator
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO, DumpStyle
from lammpsinputbuilder.group import IndicesGroup, OperationGroup, OperationGroupEnum, AllGroup, ReferenceGroup
from lammpsinputbuilder.templates.minimize_template import MinimizeTemplate
from lammpsinputbuilder.instructions import ResetTimestepInstruction, SetTimestepInstruction
from lammpsinputbuilder.quantities import TimeQuantity

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def main():
    modelData = Path(__file__).parent.parent / 'data' / \
        'models' / 'scan.fullmodel.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / \
        'potentials' / 'Si_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(modelData, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder()
    workflow.set_typed_molecular_system(typedMolecule)

    # Selection of 1-based indices, extracted from scanSelections.json
    indicesTooltip = [312, 313, 314, 315, 316, 317,
                      322, 323, 324, 325, 326, 327, 328, 329, 330]
    indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165,
                   166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
    indiceHead = [339]
    indiceAnchorTooltip = [312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323,
                           324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339]
    indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31,
                        32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 107, 125, 192, 193, 200, 207, 208, 217, 240, 244, 251]

    # Create the groups
    groupTooltip = IndicesGroup(group_name="tooltip", indices=indicesTooltip)
    groupAnchorTooltip = IndicesGroup(
        group_name="anchorTooltip", indices=indiceAnchorTooltip)
    groupAnchorSlab = IndicesGroup(
        group_name="anchorSlab", indices=indiceAnchorSlab)
    groupAnchors = OperationGroup(
        group_name="anchors",
        op=OperationGroupEnum.UNION, 
        other_groups=[groupAnchorSlab, groupAnchorTooltip])
    groupFree = OperationGroup(
        group_name="free",
        op=OperationGroupEnum.SUBTRACT, 
        other_groups=[AllGroup(), groupAnchors])

    # Declare the global groups and IOs which are going to run for every operation
    globalSection = RecursiveSection(section_name="GlobalSection")
    globalSection.add_group(groupTooltip)
    globalSection.add_group(groupAnchorSlab)
    globalSection.add_group(groupAnchorTooltip)
    globalSection.add_group(groupAnchors)
    globalSection.add_group(groupFree)

    # First section: Minimization
    sectionMinimization = MinimizeTemplate(section_name="MinimizeSection", style=MinimizeStyle.CG, etol=0.01, ftol=0.01,
                                           maxiter=100, maxeval=10000, use_anchors=True, anchor_group=ReferenceGroup(group_name="refAnchor", reference=groupAnchors))
    globalSection.add_section(sectionMinimization)

    # Second section: reset timestep
    sectionReset = InstructionsSection(section_name="ResetSection")
    sectionReset.add_instruction(ResetTimestepInstruction(
        instruction_name="resetTS", new_timestep=0))
    sectionReset.add_instruction(SetTimestepInstruction(
        instruction_name="setDT", timestep=TimeQuantity(value=1.0, units="fs")))
    globalSection.add_section(sectionReset)

    # Third section: NVE
    sectionNVE = IntegratorSection(section_name="NVESection", integrator=NVEIntegrator(
        integrator_name="NVE", group=groupFree, nb_steps=1000))
    # Declare the IOs for the entire workflow, will split into 2 trajectory later
    thermoTrajectory = ThermoFileIO(
        fileio_name="nve", add_default_fields=True, interval=50)
    thermoTrajectory.set_user_fields(typedMolecule.get_default_thermo_variables())
    dumpTrajectory = DumpTrajectoryFileIO(
        fileio_name="nve", add_default_fields=True, interval=50, group=AllGroup())
    reaxBond = ReaxBondFileIO(fileio_name="nve", interval=50, group=AllGroup())
    sectionNVE.add_fileio(dumpTrajectory)
    sectionNVE.add_fileio(reaxBond)
    sectionNVE.add_fileio(thermoTrajectory)
    globalSection.add_section(sectionNVE)

    # Fourth section: write final state
    # We use a RunZero section instead of a InstructionSection because reax bonds
    # can only be written by a fix, not a single instruction
    sectionFinalState = IntegratorSection(
        section_name="FinalSection", integrator=RunZeroIntegrator())
    finalDump = DumpTrajectoryFileIO(
        fileio_name="finalState", style=DumpStyle.XYZ, interval=1, group=AllGroup())
    finalBond = ReaxBondFileIO(
        fileio_name="finalState", interval=1, group=AllGroup())
    sectionFinalState.add_fileio(finalDump)
    sectionFinalState.add_fileio(finalBond)
    globalSection.add_section(sectionFinalState)

    # Add the section to the workflow
    workflow.add_section(globalSection)

    # Generate the inputs
    job_folder = workflow.generate_inputs()
    print(f"Inputs generated in the job folder: {job_folder}")

    return


if __name__ == "__main__":
    main()
