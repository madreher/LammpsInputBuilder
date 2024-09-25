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
from lammpsinputbuilder.integrator import NVEIntegrator, MinimizeIntegrator, MinimizeStyle
from lammpsinputbuilder.fileIO import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.extensions import LangevinCompute
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity

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

    # Create a minimization Section 
    sectionMin = IntegratorSection(
        integrator=MinimizeIntegrator(
            integratorName="Minimize",
            style=MinimizeStyle.CG, 
            etol=0.01,
            ftol=0.01, 
            maxiter=100, 
            maxeval=10000))
    workflow.addSection(sectionMin)

    # Create a Langevin Section
    sectionWarmup = IntegratorSection(
        integrator=NVEIntegrator(
            integratorName="warmup",
            group=AllGroup(),
            nbSteps=10000
        )
    )
    langevinWarmup = LangevinCompute(
        computeName="langevin",
        group=AllGroup(), 
        startTemp=TemperatureQuantity(1, "K"),
        endTemp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    sectionWarmup.addExtension(langevinWarmup)
    workflow.addSection(sectionWarmup)

    # Create a NVE Section
    sectionNVE = IntegratorSection(integrator=NVEIntegrator(
        integratorName="equilibrium",
        group=AllGroup(),
        nbSteps=100000
    ))
    langevinWarmup = LangevinCompute(
        computeName="langevin",
        group=AllGroup(), 
        startTemp=TemperatureQuantity(300, "K"),
        endTemp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    pos = DumpTrajectoryFileIO(fileIOName="fulltrajectory", addDefaultFields=True, interval=10, group=AllGroup())
    sectionNVE.addFileIO(pos)
    bonds = ReaxBondFileIO(fileIOName="bonds", interval=10, group=AllGroup())
    sectionNVE.addFileIO(bonds)
    thermo = ThermoFileIO(fileIOName="thermo", addDefaultFields=True, interval=10, userFields=typedMolecule.getDefaultThermoVariables())
    sectionNVE.addFileIO(thermo)

    workflow.addSection(sectionNVE)


    # Generate the inputs
    jobFolder = workflow.generateInputs()

    logger.info(f"Inputs generated in the job folder: {jobFolder}")

if __name__ == "__main__":
    main()