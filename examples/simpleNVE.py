#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import logging
import argparse

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem, AireboTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection
from lammpsinputbuilder.integrator import NVEIntegrator, MinimizeIntegrator, MinimizeStyle
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.extensions import LangevinExtension
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.quantities import TemperatureQuantity, TimeQuantity

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
#logger.addHandler(logging.StreamHandler())


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--reax', action='store_true', help="Use the default reax potential file.")
    parser.add_argument('--airebo', action='store_true', help="Use the default airebo potential file.")
    args = parser.parse_args()

    if args.reax and args.airebo:
        raise ValueError("Only one of --reax or --airebo can be specified.")
    
    use_reax = args.reax

    if args.reax:
        forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'
    elif args.airebo:
        forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'CH.airebo'
        use_reax = False
    else:
        forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'
    logger.info(f"Using forcefield: {forcefield}")
    
    model_data = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'


    if use_reax:
        typed_molecule = ReaxTypedMolecularSystem(
            bbox_style=BoundingBoxStyle.PERIODIC,
            electrostatic_method=ElectrostaticMethod.QEQ
        )
    else:
        typed_molecule = AireboTypedMolecularSystem(
            bbox_style=BoundingBoxStyle.PERIODIC,
            electrostatic_method=ElectrostaticMethod.QEQ
        )
    typed_molecule.load_from_file(model_data, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder ()
    workflow.set_typed_molecular_system(typed_molecule)

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
            nb_steps=10000
        )
    )
    langevinWarmup = LangevinExtension(
        extension_name="langevin",
        group=AllGroup(), 
        start_temp=TemperatureQuantity(1, "K"),
        end_temp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    sectionWarmup.add_extension(langevinWarmup)
    workflow.add_section(sectionWarmup)

    # Create a NVE Section
    sectionNVE = IntegratorSection(integrator=NVEIntegrator(
        integrator_name="equilibrium",
        group=AllGroup(),
        nb_steps=100000
    ))
    langevinWarmup = LangevinExtension(
        extension_name="langevin",
        group=AllGroup(), 
        start_temp=TemperatureQuantity(300, "K"),
        end_temp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    pos = DumpTrajectoryFileIO(fileio_name="fulltrajectory", add_default_fields=True, interval=100, group=AllGroup())
    sectionNVE.add_fileio(pos)
    if use_reax:
        bonds = ReaxBondFileIO(fileio_name="bonds", interval=100, group=AllGroup())
        sectionNVE.add_fileio(bonds)
    thermo = ThermoFileIO(fileio_name="thermo", add_default_fields=True, interval=100, user_fields=typed_molecule.get_default_thermo_variables())
    sectionNVE.add_fileio(thermo)

    workflow.add_section(sectionNVE)


    # Generate the inputs
    job_folder = workflow.generate_inputs()

    logger.info(f"Inputs generated in the job folder: {job_folder}")

if __name__ == "__main__":
    main()