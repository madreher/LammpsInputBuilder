#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from uuid import uuid4
import os
import logging

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedMolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflowBuilder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection
from lammpsinputbuilder.integrator import NVEIntegrator, MinimizeIntegrator, MinimizeStyle
from lammpsinputbuilder.fileIO import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.extensions import LangevinExtension
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
#logger.addHandler(logging.StreamHandler())


def main(): 
    modelData = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bboxStyle=BoundingBoxStyle.PERIODIC,
        electrostaticMethod=ElectrostaticMethod.QEQ
    )
    typedMolecule.loadFromFile(modelData, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder ()
    workflow.set_typed_molecular_system(typedMolecule)

    # Create a minimization Section 
    sectionMin = IntegratorSection(
        integrator=MinimizeIntegrator(
            integrator_name="Minimize",
            style=MinimizeStyle.CG, 
            etol=0.01,
            ftol=0.01, 
            maxiter=100, 
            maxeval=10000))
    workflow.add_section(sectionMin)

    # Create a Langevin Section
    sectionWarmup = IntegratorSection(
        integrator=NVEIntegrator(
            integrator_name="warmup",
            group=AllGroup(),
            nbSteps=10000
        )
    )
    langevinWarmup = LangevinExtension(
        extension_name="langevin",
        group=AllGroup(), 
        startTemp=TemperatureQuantity(1, "K"),
        endTemp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    sectionWarmup.add_extension(langevinWarmup)
    workflow.add_section(sectionWarmup)

    # Create a NVE Section
    sectionNVE = IntegratorSection(integrator=NVEIntegrator(
        integrator_name="equilibrium",
        group=AllGroup(),
        nbSteps=100000
    ))
    langevinWarmup = LangevinExtension(
        extension_name="langevin",
        group=AllGroup(), 
        startTemp=TemperatureQuantity(300, "K"),
        endTemp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    pos = DumpTrajectoryFileIO(fileio_name="fulltrajectory", add_default_fields=True, interval=10, group=AllGroup())
    sectionNVE.add_fileio(pos)
    bonds = ReaxBondFileIO(fileio_name="bonds", interval=10, group=AllGroup())
    sectionNVE.add_fileio(bonds)
    thermo = ThermoFileIO(fileio_name="thermo", add_default_fields=True, interval=10, user_fields=typedMolecule.getDefaultThermoVariables())
    sectionNVE.add_fileio(thermo)

    workflow.add_section(sectionNVE)


    # Generate the inputs
    job_folder = workflow.generate_inputs()

    logger.info(f"Inputs generated in the job folder: {job_folder}")

if __name__ == "__main__":
    main()