#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from uuid import uuid4
import os
import logging

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecule
from lammpsinputbuilder.workflowBuilder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.fileIO import DumpTrajectoryFileIO
from lammpsinputbuilder.group import AllGroup

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
#logger.addHandler(logging.StreamHandler())


def main(): 
    modelData = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecule(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )
    typedMolecule.loadFromFile(modelData, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder ()
    workflow.setTypedMolecule(typedMolecule)

    # Create a NVE Section
    section = IntegratorSection(integrator=NVEIntegrator())
    io = DumpTrajectoryFileIO(fileIOName="fulltrajectory", addDefaultFields=True, interval=10, group=AllGroup())
    section.addFileIO(io)

    workflow.addSection(section)


    # Generate the inputs
    jobFolder = workflow.generateInputs()

    logger.info(f"Inputs generated in the job folder: {jobFolder}")

if __name__ == "__main__":
    main()