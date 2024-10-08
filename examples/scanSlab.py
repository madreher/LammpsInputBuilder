from pathlib import Path
import logging
import argparse
import subprocess
import numpy as np
import lammps_logfile

import matplotlib.pyplot as plt

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection, RecursiveSection, InstructionsSection
from lammpsinputbuilder.integrator import MinimizeStyle, RunZeroIntegrator
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO, DumpStyle
from lammpsinputbuilder.group import IndicesGroup, OperationGroup, OperationGroupEnum, AllGroup, ReferenceGroup
from lammpsinputbuilder.templates.minimize_template import MinimizeTemplate
from lammpsinputbuilder.instructions import DisplaceAtomsInstruction
from lammpsinputbuilder.quantities import LengthQuantity

import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def readBondPairsFromFrame(filePath: Path, minbondOrder:float) -> list:
    result = []
    ignoredBondPairs = 0
    with open(filePath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                continue

            # Column format:
            # id type nb id_1...id_nb mol bo_1...bo_nb abo nlp q
            # 48 1 1 23 0         1.127         1.127         1.000         0.000
            #print(f"Line {counter}, current line:" + line)
            fields = line.split()
            atomID = int(fields[0])
            nbBonds = int(fields[2])
            if nbBonds <= 0:
                continue
            bonded = []
            if nbBonds > 0:
                for i in range(3, 3 + nbBonds):
                    bonded.append(int(fields[i]))
            startBondOrder = 3 + nbBonds + 1
            bondOrders = []
            for i in range(startBondOrder, startBondOrder + nbBonds):
                bondOrders.append(float(fields[i]))
            for i in range(0, nbBonds):
                # We only keep bonds with higher ID to avoid duplicate when considering the inversed bond pair
                # We only care about bonds with order > 0.5, below would not really be a bond in the chemistry sense
                if bonded[i] > atomID:
                    if bondOrders[i] > minbondOrder: 
                        result.append([atomID, bonded[i]])
                    else:
                        logger.debug(f"Skipping bond {atomID} - {bonded[i]} with bond order {bondOrders[i]} in file {filePath}")
                        ignoredBondPairs += 1

    return result, ignoredBondPairs


def runMinimizationSlab(lmpExecPath: Path, model: str) -> Path:
    # In the first workflow, we're going to minimize the system only
    if model == "passivated":
        modelData = Path(__file__).parent.parent / 'data' / 'models' / 'scan.fullmodel.xyz'
    elif model == "headopen":
        modelData = Path(__file__).parent.parent / 'data' / 'models' / 'scan.head.depassivated.fullmodel.xyz'
    elif model == "headslabopen":
        modelData = Path(__file__).parent.parent / 'data' / 'models' / 'scan.slab.head.depassivated.fullmodel.xyz'
    else:
        raise ValueError(f"Unknown model {model}")
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'Si_C_H.reax'
    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(modelData, forcefield)
    workflow = WorkflowBuilder ()
    workflow.set_typed_molecular_system(typedMolecule)

    # Selection of 1-based indices, extracted from scanSelections.json
    if model == "passivated":
        indiceAnchorTooltip = [312, 313, 314, 315, 316, 317, 322, 323, 324, 325, 326, 327, 328, 329, 330]
        indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
        indiceHead = [339]
        indicesTooltip = [312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339]
        indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 107, 125, 192, 193, 200, 207, 208, 217, 240, 244, 251]
    elif model == "headopen":
        indiceAnchorTooltip = [312, 313, 314, 315, 316, 317, 322, 323, 324, 325, 326, 327, 328, 329, 330]
        indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
        indiceHead = [338]
        indicesTooltip = [312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338]
        indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 107, 125, 192, 193, 200, 207, 208, 217, 240, 244, 251]
    elif model == "headslabopen":
        indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 192, 200, 207, 217, 238, 240, 241, 244, 251]
        indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310]
        indiceHead = [337]
        indiceAnchorTooltip = [311, 312, 313, 314, 315, 316, 321, 322, 323, 324, 325, 326, 327, 328, 329]
        indicesTooltip = [311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337]
    else:
        raise ValueError(f"Unknown model {model}")
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'Si_C_H.reax'

    # Create the groups 
    groupTooltip  = IndicesGroup(group_name="tooltip", indices=indicesTooltip)
    groupAnchorTooltip = IndicesGroup(group_name="anchorTooltip", indices=indiceAnchorTooltip)
    groupAnchorSlab = IndicesGroup(group_name="anchorSlab", indices=indiceAnchorSlab)
    groupAnchors = OperationGroup(group_name="anchors", op=OperationGroupEnum.UNION, other_groups=[groupAnchorSlab, groupAnchorTooltip])
    groupFree = OperationGroup(group_name="free", op=OperationGroupEnum.SUBTRACT, other_groups=[AllGroup(), groupAnchors])

    # Declare the global groups and IOs which are going to run for every operation
    globalSection = RecursiveSection(section_name="GlobalSection")
    globalSection.add_group(groupTooltip)
    globalSection.add_group(groupAnchorSlab)
    globalSection.add_group(groupAnchorTooltip)
    globalSection.add_group(groupAnchors)
    globalSection.add_group(groupFree)

    # First section: Minimization 
    sectionMinimization = MinimizeTemplate(section_name="MinimizeSection", style=MinimizeStyle.CG, etol = 0.01, ftol = 0.01, maxiter = 100, maxeval = 10000, use_anchors=True, anchor_group=ReferenceGroup(group_name="refAnchor", reference=groupAnchors))
    globalSection.add_section(sectionMinimization)

    sectionFinalState = IntegratorSection(section_name="FinalSection", integrator=RunZeroIntegrator())
    finalDump = DumpTrajectoryFileIO(fileio_name="finalState", style=DumpStyle.CUSTOM, interval=1, group=AllGroup(), user_fields=["id", "type", "element", "x", "y", "z"])
    finalBond = ReaxBondFileIO(fileio_name="finalState", interval=1, group=AllGroup())
    sectionFinalState.add_fileio(finalDump)
    sectionFinalState.add_fileio(finalBond)
    globalSection.add_section(sectionFinalState)

    # Add the section to the workflow
    workflow.add_section(globalSection)

    # Generate the inputs
    job_folder = workflow.generate_inputs()
    logger.info(f"Minimization inputs generated in the job folder: {job_folder}")

    # Run the workflow
    subprocess.run("mpirun -np 1 " + str(lmpExecPath) + " -in " + str(job_folder / "workflow.input"), shell=True, check=True, capture_output=True, cwd=job_folder)

    # Check that the final position state exists
    if not (job_folder / finalDump.get_associated_file_path()).exists():
        raise FileNotFoundError(f"Could not find the final dump file at {job_folder / finalDump.get_associated_file_path()}")

    if not (job_folder / finalBond.get_associated_file_path()).exists():
        raise FileNotFoundError(f"Could not find the final bond file at {job_folder / finalBond.get_associated_file_path()}")
    
    return job_folder / finalDump.get_associated_file_path()

def scanSurface(lmpExecPath: Path, xyzPath: Path, model: str, zplane:float, xydelta:float):

    # Load the model to get atom positions
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'Si_C_H.reax'
    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(xyzPath, forcefield)

    # List of relevant atoms 
    # Selection of 1-based indices, extracted from scanSelections.json
    if model == "passivated":
        indiceAnchorTooltip = [312, 313, 314, 315, 316, 317, 322, 323, 324, 325, 326, 327, 328, 329, 330]
        indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
        indiceHead = [339]
        indicesTooltip = [312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339]
        indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 107, 125, 192, 193, 200, 207, 208, 217, 240, 244, 251]
    elif model == "headopen":
        indiceAnchorTooltip = [312, 313, 314, 315, 316, 317, 322, 323, 324, 325, 326, 327, 328, 329, 330]
        indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
        indiceHead = [338]
        indicesTooltip = [312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338]
        indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 107, 125, 192, 193, 200, 207, 208, 217, 240, 244, 251]
    elif model == "headslabopen":
        indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 192, 200, 207, 217, 238, 240, 241, 244, 251]
        indiceHead = [337]
        indiceAnchorTooltip = [311, 312, 313, 314, 315, 316, 321, 322, 323, 324, 325, 326, 327, 328, 329]
        indicesTooltip = [311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337]
        indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310]
    else:
        raise ValueError(f"Unknown model {model}")
   
    # Get the positions and the list of atoms for the slab to compute its bounding box
    positions = typedMolecule.get_ase_model().get_positions()
    slabIndicesZeroBased = np.array(indicesSlab) - 1
    slabPositions = np.take(positions, slabIndicesZeroBased, axis=0)

    # Compute the bounding box oif the slab
    slabBoundingBox = np.min(slabPositions, axis=0), np.max(slabPositions, axis=0)
    print(slabBoundingBox)

    # Get the position of the head 
    headInitialPosition = positions[indiceHead[0] - 1]

    # Now that we know where the slab is, and where the head is, we can plan a trajectory
    # For this example, we are going to put the head 2A abobe the slab, and scan every 1A on x and y axis 
    desiredZDelta = LengthQuantity(zplane, 'angstrom').get_magnitude()
    desiredXDelta = LengthQuantity(xydelta, 'angstrom').get_magnitude()
    desiredYDelta = LengthQuantity(xydelta, 'angstrom').get_magnitude()
    logger.info(f"Generating trajectory with the following parameters in A: zplane={zplane}, xdelta={desiredXDelta}, ydelta={desiredYDelta}")
    heightTip = slabBoundingBox[1][2] + desiredZDelta
    headTargetPositions = []
    headPixel = []
    trajectoryFiles = []
    bondFiles = []

    # Generate a grid of target positions
    for i,x in enumerate(np.arange(slabBoundingBox[0][0], slabBoundingBox[1][0], desiredXDelta)):
        for j,y in enumerate(np.arange(slabBoundingBox[0][1], slabBoundingBox[1][1], desiredYDelta)):
            headTargetPosition = np.array([x, y, heightTip])
            headTargetPositions.append(headTargetPosition)
            headPixel.append([i, j])

    # Now that we have the target positions, we can prepare the lammps script
    workflow = WorkflowBuilder ()
    workflow.set_typed_molecular_system(typedMolecule)

    # Create the groups 
    groupTooltip  = IndicesGroup(group_name="tooltip", indices=indicesTooltip)
    groupAnchorTooltip = IndicesGroup(group_name="anchorTooltip", indices=indiceAnchorTooltip)
    groupAnchorSlab = IndicesGroup(group_name="anchorSlab", indices=indiceAnchorSlab)
    groupAnchors = OperationGroup(group_name="anchors", op=OperationGroupEnum.UNION, other_groups=[groupAnchorSlab, groupAnchorTooltip])
    groupFree = OperationGroup(group_name="free", op=OperationGroupEnum.SUBTRACT, other_groups=[AllGroup(), groupAnchors])

    # Declare the global groups and IOs which are going to run for every operation
    globalSection = RecursiveSection(section_name="GlobalSection")
    globalSection.add_group(groupTooltip)
    globalSection.add_group(groupAnchorSlab)
    globalSection.add_group(groupAnchorTooltip)
    globalSection.add_group(groupAnchors)
    globalSection.add_group(groupFree)

    for i, headTargetPosition in enumerate(headTargetPositions):

        # For each target, we are going to do the following:
        # 1. Move the head to the target
        # 2. Perform a SPE 
        # 4. Write the positions and bonds
        # 3. Move the head back to the initial position

        stepSection = RecursiveSection(section_name=f"Section_{headPixel[i][0]}_{headPixel[i][1]}")
        moveForwardSection = InstructionsSection(section_name="MoveForwardSection")

        # Unit note: ASE positions are in Angstroms
        moveForwardSection.add_instruction(instruction=DisplaceAtomsInstruction(instruction_name="moveforward", group=ReferenceGroup(group_name="tooltip", reference=groupTooltip), 
                                                                        dx=LengthQuantity(value=headTargetPosition[0] - headInitialPosition[0], units="angstrom"),
                                                                        dy=LengthQuantity(value=headTargetPosition[1] - headInitialPosition[1], units="angstrom"),
                                                                        dz=LengthQuantity(value=headTargetPosition[2] - headInitialPosition[2], units="angstrom")))
        speSection = IntegratorSection(section_name="SPESection", integrator=RunZeroIntegrator())
        dumpIO = DumpTrajectoryFileIO(fileio_name=f"pxl_{headPixel[i][0]}_{headPixel[i][1]}", style=DumpStyle.CUSTOM, user_fields=["id", "type", "element", "x", "y", "z"], interval=1, group=AllGroup())
        trajectoryFiles.append(dumpIO.get_associated_file_path())
        bondIO = ReaxBondFileIO(fileio_name=f"pxl_{headPixel[i][0]}_{headPixel[i][1]}", group=AllGroup(), interval=1)
        bondFiles.append(bondIO.get_associated_file_path())
        thermoIO = ThermoFileIO(fileio_name=f"pxl_{headPixel[i][0]}_{headPixel[i][1]}", interval=1, user_fields=typedMolecule.get_default_thermo_variables())
        speSection.add_fileio(dumpIO)
        speSection.add_fileio(bondIO)
        speSection.add_fileio(thermoIO)
        moveBackwardSection = InstructionsSection(section_name="MoveBackwardSection")
        moveBackwardSection.add_instruction(instruction=DisplaceAtomsInstruction(instruction_name="movebackward", group=ReferenceGroup(group_name="tooltip", reference=groupTooltip), 
                                                                        dx=LengthQuantity(value=headInitialPosition[0] - headTargetPosition[0], units="angstrom"),
                                                                        dy=LengthQuantity(value=headInitialPosition[1] - headTargetPosition[1], units="angstrom"),
                                                                        dz=LengthQuantity(value=headInitialPosition[2] - headTargetPosition[2], units="angstrom")))
        stepSection.add_section(moveForwardSection)
        stepSection.add_section(speSection)
        stepSection.add_section(moveBackwardSection)
        globalSection.add_section(stepSection)


    workflow.add_section(globalSection)

    # Generate the inputs
    job_folder = workflow.generate_inputs()
    logger.info(f"Scan inputs generated in the job folder: {job_folder}")

    # Run the workflow
    logger.info(f"Starting the scan process...")
    subprocess.run("mpirun -np 1 " + str(lmpExecPath) + " -in " + str(job_folder / "workflow.input"), shell=True, check=True, capture_output=True, cwd=job_folder)
    logger.info(f"Scan completed in the job folder: {job_folder}")

    # Concatenate the trajectories
    logger.info("Concatenating trajectories...")
    
    concatTrajectoryFile = job_folder / "positions.fulltrajectory.lammpstrj"
    concatBondFile = job_folder / "reaxbonds.fulltrajectory.txt"
    for i in range(len(trajectoryFiles)):
        trajectoryFiles[i] = str(job_folder / trajectoryFiles[i])
        bondFiles[i] = str(job_folder / bondFiles[i])

    # Not using a single command with join because it leads to a command line too long when many files are concatenated
    #subprocess.run("cat " + " ".join(trajectoryFiles) + " > " + str(concatTrajectoryFile), shell=True, check=True, capture_output=True, cwd=job_folder)
    #subprocess.run("cat " + " ".join(bondFiles) + " >> " + str(concatBondFile), shell=True, check=True, capture_output=True, cwd=job_folder)
    for file in trajectoryFiles:
        subprocess.run("cat " + str(file) + " >> " + str(concatTrajectoryFile), shell=True, check=True, capture_output=True, cwd=job_folder)
    for file in bondFiles:
        subprocess.run("cat " + str(file) + " >> " + str(concatBondFile), shell=True, check=True, capture_output=True, cwd=job_folder)

    
    logger.info("Concatenated position trajectories saved in: " + str(concatTrajectoryFile))
    logger.info("Concatenated bonds trajectories saved in: " + str(concatBondFile))

    # Move all the files from trajectory files to the new folder
    frameFolder = job_folder / "frames"
    frameFolder.mkdir()
    subprocess.run("mv dump.* " + str(frameFolder), shell=True, check=True, capture_output=True, cwd=job_folder)
    subprocess.run("mv bonds.* " + str(frameFolder), shell=True, check=True, capture_output=True, cwd=job_folder)
    logger.info("Frames saved in: " + str(frameFolder))

    return job_folder, headPixel

def drawPotentialEnergyMap(job_folder: Path, headPixel: list):

    # We are going to create an imaage with a color map corresponding to the potential energy of each pixel

    # First, create an empty array
    data = np.zeros((headPixel[-1][0] + 1, headPixel[-1][1] + 1), dtype=np.float64)

    # Get the log file 
    logFile = job_folder / "log.lammps"
    log = lammps_logfile.File(logFile)

    # Loop over the frames
    for i in range(len(headPixel)):
        # Get the frame
        dataFrame = log.get(entry_name="PotEng", run_num=i)
        #print(dataFrame)
        # Some frames can have ["warning"] as their first value, query for the last one ro be safe
        data[headPixel[i][0], headPixel[i][1]] = dataFrame[-1]

    # Create a colormap with mathplotlib
    cmap = plt.get_cmap('inferno')
    plt.imshow(data, cmap=cmap, origin='lower')
    plt.colorbar()
    plt.savefig(job_folder / "potentialEnergyMap.png")
    plt.clf()

    logger.info("Potential energy map saved in: " + str(job_folder / "potentialEnergyMap.png"))

def drawBondConfigurationMap(job_folder: Path, headPixel: list, minbondOrder:float):

    # We create an image where each pixel corresponds to a bond configuration, i.e an set of bond pairs
    # Currently, we only consider bond pairs, regardless of the type. Should probably be refined in the next iteration

    colorMap = {}
    data = np.zeros((headPixel[-1][0] + 1, headPixel[-1][1] + 1), dtype=np.int32)

    frameFolder = job_folder / "frames"
    currentID = 0
    totalIgnoredBondPaired = 0
    logger.info("Start computing bond configurations with a minimum bond order of " + str(minbondOrder))

    for i in range(len(headPixel)):

        bondsFile = frameFolder / f"bonds.pxl_{headPixel[i][0]}_{headPixel[i][1]}.txt"
        bondPairs, ignoredPaired = readBondPairsFromFrame(bondsFile, minbondOrder)
        totalIgnoredBondPaired += ignoredPaired

        # Sort the pairs first by the first atom id, then by the second atom id
        npBondPairs = np.array(bondPairs)
        sortedPairs = npBondPairs[np.lexsort((npBondPairs[:,1], npBondPairs[:,0]))]

        # Compute a unique ID corresponding to this list of bond pairs
        hashObj = hashlib.new("md5")
        hashObj.update(sortedPairs.tobytes())
        id = hashObj.hexdigest()

        if id not in colorMap:
            # We found a new bond configuration, adding it to the color map
            colorMap[id] = currentID
            data[headPixel[i][0], headPixel[i][1]] = currentID
            currentID += 1
        else:
            # We have seen this bond configuration before, just use the same ID
            data[headPixel[i][0], headPixel[i][1]] = colorMap[id]

    # Create a colormap with mathplotlib
    #cmap = plt.get_cmap('inferno')
    cmap = plt.get_cmap('tab20')
    plt.imshow(data, cmap=cmap, origin='lower', interpolation='none')
    plt.colorbar()
    plt.savefig(job_folder / "bondConfigurationMap.png")
    plt.clf()

    logger.info("Number of configurations found: " + str(len(colorMap)))
    if totalIgnoredBondPaired > 0:
        logger.warning("Number of ignored bond pairs: " + str(totalIgnoredBondPaired) + ". Rerun with \'debug\' log level to list the ignored bonds.")
    else:
        logger.info("No bond pairs ignored.")

    logger.info("Bonds configuration map saved in: " + str(job_folder / "bondConfigurationMap.png"))





    


def main(): 
    modelAvailables = ['passivated', 'headopen', "headslabopen"]
    logLevelAvailables = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--lmpexec', type=str, required=True, help="Path to the lammps executable.")
    argparser.add_argument('--model', type=str, required=True, help="Model to use {}".format(modelAvailables))
    argparser.add_argument('--zplane', type=float, default=2.0, help="Z plane above the slab to scan")
    argparser.add_argument('--deltaxy', type=float, default=1.0, help="Delta x and y for the scan")
    argparser.add_argument('--loglevel', type=str, default="INFO", help="Log level")
    argparser.add_argument('--min-bond-order', type=float, default=0.5, help="Minimum bond order to consider a bond pair. Pairs with a lower bond order will be ignored.")

    args = argparser.parse_args()
    
    lmpexec = Path(args.lmpexec)
    if not lmpexec.exists():
        raise FileNotFoundError(f"Could not find lammps executable at {lmpexec}")

    if args.model not in modelAvailables:
        raise ValueError(f"Model must be one of the following: {modelAvailables}")
    
    if args.loglevel not in logLevelAvailables:
        raise ValueError(f"Log level must be one of the following: {logLevelAvailables}")
    
    logger.setLevel(args.loglevel)
    zplane = args.zplane
    xydelta = args.deltaxy
    minBondOrder = args.min_bond_order
    
    minimizedModelPath = runMinimizationSlab(lmpexec, args.model)
    logger.info(f"Minimized model path: {minimizedModelPath}")

    job_folder, headPixel = scanSurface(lmpexec, minimizedModelPath, args.model, zplane, xydelta)

    drawPotentialEnergyMap(job_folder, headPixel)

    drawBondConfigurationMap(job_folder, headPixel, minBondOrder)

        


if __name__ == "__main__":
    main()


    