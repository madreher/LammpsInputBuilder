from pathlib import Path
import logging

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection
from lammpsinputbuilder.integrator import MinimizeIntegrator, MinimizeStyle

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def main():
    modelData = Path(__file__).parent.parent / 'data' / \
        'models' / 'benzene.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / \
        'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(modelData, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder()
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

    # Generate the inputs
    job_folder = workflow.generate_inputs()
    logger.info(f"Inputs generated in the job folder: {job_folder}")

if __name__ == "__main__":
    main()
