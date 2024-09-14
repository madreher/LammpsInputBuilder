from pathlib import Path
import logging
import argparse
import subprocess
import numpy as np
from os import system
import lammps_logfile

import matplotlib.pyplot as plt

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecule
from lammpsinputbuilder.workflowBuilder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection, RecusiveSection, InstructionsSection
from lammpsinputbuilder.integrator import NVEIntegrator, MinimizeStyle, RunZeroIntegrator
from lammpsinputbuilder.fileIO import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO, DumpStyle
from lammpsinputbuilder.group import IndicesGroup, OperationGroup, OperationGroupEnum, AllGroup, ReferenceGroup
from lammpsinputbuilder.templates.minimizeTemplate import MinimizeTemplate
from lammpsinputbuilder.instructions import DisplaceAtomsInstruction
from lammpsinputbuilder.quantities import LengthQuantity

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def runMinimizationSlab(lmpExecPath: Path) -> Path:
    # In the first workflow, we're going to minimize the system only
    modelData = Path(__file__).parent.parent / 'data' / 'models' / 'scan.fullmodel.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'Si_C_H.reax'
    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )
    typedMolecule.loadFromFile(modelData, forcefield)
    workflow = WorkflowBuilder ()
    workflow.setTypedMolecule(typedMolecule)

    # Selection of 1-based indices, extracted from scanSelections.json
    indiceAnchorTooltip = [312, 313, 314, 315, 316, 317, 322, 323, 324, 325, 326, 327, 328, 329, 330]
    indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
    indiceHead = [339]
    indicesTooltip = [312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339]
    indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 107, 125, 192, 193, 200, 207, 208, 217, 240, 244, 251]

    # Create the groups 
    groupTooltip  = IndicesGroup(groupName="tooltip", indices=indicesTooltip)
    groupAnchorTooltip = IndicesGroup(groupName="anchorTooltip", indices=indiceAnchorTooltip)
    groupAnchorSlab = IndicesGroup(groupName="anchorSlab", indices=indiceAnchorSlab)
    groupAnchors = OperationGroup(groupName="anchors", op=OperationGroupEnum.UNION, otherGroups=[groupAnchorSlab, groupAnchorTooltip])
    groupFree = OperationGroup(groupName="free", op=OperationGroupEnum.SUBTRACT, otherGroups=[AllGroup(), groupAnchors])

    # Declare the global groups and IOs which are going to run for every operation
    globalSection = RecusiveSection(sectionName="GlobalSection")
    globalSection.addGroup(groupTooltip)
    globalSection.addGroup(groupAnchorSlab)
    globalSection.addGroup(groupAnchorTooltip)
    globalSection.addGroup(groupAnchors)
    globalSection.addGroup(groupFree)

    # First section: Minimization 
    sectionMinimization = MinimizeTemplate(sectionName="MinimizeSection", style=MinimizeStyle.CG, etol = 0.01, ftol = 0.01, maxiter = 100, maxeval = 10000, useAnchors=True, anchorGroup=ReferenceGroup(groupName="refAnchor", reference=groupAnchors))
    globalSection.addSection(sectionMinimization)

    sectionFinalState = IntegratorSection(sectionName="FinalSection", integrator=RunZeroIntegrator())
    finalDump = DumpTrajectoryFileIO(fileIOName="finalState", style=DumpStyle.CUSTOM, interval=1, group=AllGroup(), userFields=["id", "type", "element", "x", "y", "z"])
    finalBond = ReaxBondFileIO(fileIOName="finalState", interval=1, group=AllGroup())
    sectionFinalState.addFileIO(finalDump)
    sectionFinalState.addFileIO(finalBond)
    globalSection.addSection(sectionFinalState)

    # Add the section to the workflow
    workflow.addSection(globalSection)

    # Generate the inputs
    jobFolder = workflow.generateInputs()
    logger.info(f"Minimization inputs generated in the job folder: {jobFolder}")

    # Run the workflow
    subprocess.run("mpirun -np 1 " + str(lmpExecPath) + " -in " + str(jobFolder / "workflow.input"), shell=True, check=True, capture_output=True, cwd=jobFolder)

    # Check that the final position state exists
    if not (jobFolder / finalDump.getAssociatedFilePath()).exists():
        raise FileNotFoundError(f"Could not find the final dump file at {jobFolder / finalDump.getAssociatedFilePath()}")

    if not (jobFolder / finalBond.getAssociatedFilePath()).exists():
        raise FileNotFoundError(f"Could not find the final bond file at {jobFolder / finalBond.getAssociatedFilePath()}")
    
    return jobFolder / finalDump.getAssociatedFilePath()

def scanSurface(lmpExecPath: Path, xyzPath: Path):

    # Load the model to get atom positions
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'Si_C_H.reax'
    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )
    typedMolecule.loadFromFile(xyzPath, forcefield)

    # List of relevant atoms 
    # Selection of 1-based indices, extracted from scanSelections.json
    indiceAnchorTooltip = [312, 313, 314, 315, 316, 317, 322, 323, 324, 325, 326, 327, 328, 329, 330]
    indicesSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
    indiceHead = [339]
    indicesTooltip = [312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339]
    indiceAnchorSlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 100, 107, 125, 192, 193, 200, 207, 208, 217, 240, 244, 251]

   
    # Get the positions and the list of atoms for the slab to compute its bounding box
    positions = typedMolecule.getASEAtoms().get_positions()
    slabIndicesZeroBased = np.array(indicesSlab) - 1
    slabPositions = np.take(positions, slabIndicesZeroBased, axis=0)

    # Compute the bounding box oif the slab
    slabBoundingBox = np.min(slabPositions, axis=0), np.max(slabPositions, axis=0)
    print(slabBoundingBox)

    # Get the position of the head 
    headInitialPosition = positions[indiceHead[0] - 1]

    # Now that we know where the slab is, and where the head is, we can plan a trajectory
    # For this example, we are going to put the head 2A abobe the slab, and scan every 1A on x and y axis 
    desiredZDelta = 2.0
    desiredXDelta = 0.2
    desiredYDelta = 0.2
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
    workflow.setTypedMolecule(typedMolecule)

    # Create the groups 
    groupTooltip  = IndicesGroup(groupName="tooltip", indices=indicesTooltip)
    groupAnchorTooltip = IndicesGroup(groupName="anchorTooltip", indices=indiceAnchorTooltip)
    groupAnchorSlab = IndicesGroup(groupName="anchorSlab", indices=indiceAnchorSlab)
    groupAnchors = OperationGroup(groupName="anchors", op=OperationGroupEnum.UNION, otherGroups=[groupAnchorSlab, groupAnchorTooltip])
    groupFree = OperationGroup(groupName="free", op=OperationGroupEnum.SUBTRACT, otherGroups=[AllGroup(), groupAnchors])

    # Declare the global groups and IOs which are going to run for every operation
    globalSection = RecusiveSection(sectionName="GlobalSection")
    globalSection.addGroup(groupTooltip)
    globalSection.addGroup(groupAnchorSlab)
    globalSection.addGroup(groupAnchorTooltip)
    globalSection.addGroup(groupAnchors)
    globalSection.addGroup(groupFree)

    for i, headTargetPosition in enumerate(headTargetPositions):

        # For each target, we are going to do the following:
        # 1. Move the head to the target
        # 2. Perform a SPE 
        # 4. Write the positions and bonds
        # 3. Move the head back to the initial position

        stepSection = RecusiveSection(sectionName=f"Section_{headPixel[i][0]}_{headPixel[i][1]}")
        moveForwardSection = InstructionsSection(sectionName="MoveForwardSection")
        moveForwardSection.addInstruction(instruction=DisplaceAtomsInstruction(instructionName="moveforward", group=ReferenceGroup(groupName="tooltip", reference=groupTooltip), 
                                                                        dx=LengthQuantity(value=headTargetPosition[0] - headInitialPosition[0], units="lmp_real_length"),
                                                                        dy=LengthQuantity(value=headTargetPosition[1] - headInitialPosition[1], units="lmp_real_length"),
                                                                        dz=LengthQuantity(value=headTargetPosition[2] - headInitialPosition[2], units="lmp_real_length")))
        speSection = IntegratorSection(sectionName="SPESection", integrator=RunZeroIntegrator())
        dumpIO = DumpTrajectoryFileIO(fileIOName=f"{headPixel[i][0]}_{headPixel[i][1]}", style=DumpStyle.CUSTOM, userFields=["id", "type", "element", "x", "y", "z"], interval=1, group=AllGroup())
        trajectoryFiles.append(dumpIO.getAssociatedFilePath())
        bondIO = ReaxBondFileIO(fileIOName=f"{headPixel[i][0]}_{headPixel[i][1]}", group=AllGroup(), interval=1)
        bondFiles.append(bondIO.getAssociatedFilePath())
        thermoIO = ThermoFileIO(fileIOName=f"{headPixel[i][0]}_{headPixel[i][1]}", interval=1, userFields=typedMolecule.getDefaultThermoVariables())
        speSection.addFileIO(dumpIO)
        speSection.addFileIO(bondIO)
        speSection.addFileIO(thermoIO)
        moveBackwardSection = InstructionsSection(sectionName="MoveBackwardSection")
        moveBackwardSection.addInstruction(instruction=DisplaceAtomsInstruction(instructionName="movebackward", group=ReferenceGroup(groupName="tooltip", reference=groupTooltip), 
                                                                        dx=LengthQuantity(value=headInitialPosition[0] - headTargetPosition[0], units="lmp_real_length"),
                                                                        dy=LengthQuantity(value=headInitialPosition[1] - headTargetPosition[1], units="lmp_real_length"),
                                                                        dz=LengthQuantity(value=headInitialPosition[2] - headTargetPosition[2], units="lmp_real_length")))
        stepSection.addSection(moveForwardSection)
        stepSection.addSection(speSection)
        stepSection.addSection(moveBackwardSection)
        globalSection.addSection(stepSection)


    workflow.addSection(globalSection)

    # Generate the inputs
    jobFolder = workflow.generateInputs()
    logger.info(f"Scan inputs generated in the job folder: {jobFolder}")

    # Run the workflow
    subprocess.run("mpirun -np 1 " + str(lmpExecPath) + " -in " + str(jobFolder / "workflow.input"), shell=True, check=True, capture_output=True, cwd=jobFolder)
    logger.info(f"Scan completed in the job folder: {jobFolder}")

    # Concatenate the trajectories
    logger.info("Concatenating trajectories...")
    
    concatTrajectoryFile = jobFolder / "positions.fulltrajectory.lammpstrj"
    concatBondFile = jobFolder / "reaxbonds.fulltrajectory.txt"
    for i in range(len(trajectoryFiles)):
        trajectoryFiles[i] = str(jobFolder / trajectoryFiles[i])
        bondFiles[i] = str(jobFolder / bondFiles[i])
    #subprocess.run("cat " + " ".join(trajectoryFiles) + " > " + str(concatTrajectoryFile), shell=True, check=True, capture_output=True, cwd=jobFolder)
    #subprocess.run("cat " + " ".join(bondFiles) + " >> " + str(concatBondFile), shell=True, check=True, capture_output=True, cwd=jobFolder)
    for file in trajectoryFiles:
        subprocess.run("cat " + str(file) + " >> " + str(concatTrajectoryFile), shell=True, check=True, capture_output=True, cwd=jobFolder)
    for file in bondFiles:
        subprocess.run("cat " + str(file) + " >> " + str(concatBondFile), shell=True, check=True, capture_output=True, cwd=jobFolder)

    
    logger.info("Concatenated position trajectories saved in: " + str(concatTrajectoryFile))
    logger.info("Concatenated bonds trajectories saved in: " + str(concatBondFile))

    # Move all the files from trajectory files to the new folder
    frameFolder = jobFolder / "frames"
    frameFolder.mkdir()
    subprocess.run("mv dump.* " + str(frameFolder), shell=True, check=True, capture_output=True, cwd=jobFolder)
    subprocess.run("mv bonds.* " + str(frameFolder), shell=True, check=True, capture_output=True, cwd=jobFolder)
    logger.info("Frames saved in: " + str(frameFolder))

    return jobFolder, headPixel

def analyseFrames(jobFolder: Path, headPixel: list):

    # We are going to create an imaage with a color map corresponding to the potential energy of each pixel

    # First, create an empty array
    data = np.zeros((headPixel[-1][0] + 1, headPixel[-1][1] + 1), dtype=np.float64)

    # Get the log file 
    logFile = jobFolder / "log.lammps"
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
    plt.savefig(jobFolder / "potentialEnergyMap.png")

    logger.info("Potential energy map saved in: " + str(jobFolder / "potentialEnergyMap.png"))

    


def main(): 
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--lmpexec', type=str, required=True, help="Path to the lammps executable.")

    args = argparser.parse_args()
    
    lmpexec = Path(args.lmpexec)
    if not lmpexec.exists():
        raise FileNotFoundError(f"Could not find lammps executable at {lmpexec}")
    
    minimizedModelPath = runMinimizationSlab(lmpexec)
    logger.info(f"Minimized model path: {minimizedModelPath}")

    jobFolder, headPixel = scanSurface(lmpexec, minimizedModelPath)

    analyseFrames(jobFolder, headPixel)

        


if __name__ == "__main__":
    main()


    