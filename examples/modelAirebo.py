#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import logging

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import AireboTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())


def main():
    model_data = Path(__file__).parent.parent / \
        'data' / 'models' / 'benzene.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / \
        'potentials' / 'CH.airebo'

    typed_molecule = AireboTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typed_molecule.load_from_file(model_data, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder()
    workflow.set_typed_molecular_system(typed_molecule)

    # Generate the inputs
    job_folder = workflow.generate_inputs()

    logger.info(f"Inputs generated in the job folder: {job_folder}")


if __name__ == "__main__":
    main()
