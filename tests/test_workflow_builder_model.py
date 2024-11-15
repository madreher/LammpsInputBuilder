import json 
from pathlib import Path

from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
from lammpsinputbuilder.workflow_builder import WorkflowBuilder
from lammpsinputbuilder.section import IntegratorSection 
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.fileio import DumpTrajectoryFileIO, ReaxBondFileIO, ThermoFileIO
from lammpsinputbuilder.group import AllGroup

from lammpsinputbuilder.model.workflow_builder_model import WorkflowBuilderModel

def test_workflow_builder_model():
    # Create a molecule
    molecule_path = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield_path=Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typed_molecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )

    typed_molecule.load_from_file(molecule_path, forcefield_path)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder()
    workflow.set_typed_molecular_system(typed_molecule)

    # Create a NVE Section
    section = IntegratorSection(integrator=NVEIntegrator())
    pos = DumpTrajectoryFileIO(fileio_name="fulltrajectory",
                               add_default_fields=True, interval=10, group=AllGroup())
    section.add_fileio(pos)
    bonds = ReaxBondFileIO(fileio_name="bonds", interval=10, group=AllGroup())
    section.add_fileio(bonds)
    thermo = ThermoFileIO(fileio_name="thermo", add_default_fields=True, interval=10)
    section.add_fileio(thermo)

    workflow.add_section(section)

    obj_dict = workflow.to_dict()
    obj_dict_str = json.dumps(obj_dict, indent=4)

    obj_model1 = WorkflowBuilderModel.model_validate_json(obj_dict_str)
    assert obj_model1.header.major_version == 1
    assert obj_model1.header.minor_version == 0
    assert obj_model1.header.format == "WorkflowBuilder"

    assert obj_model1.sections[0].class_name == "IntegratorSection"
    assert obj_model1.sections[0].integrator.class_name == "NVEIntegrator"
    assert obj_model1.sections[0].fileios[0].class_name == "DumpTrajectoryFileIO"
    assert obj_model1.sections[0].fileios[1].class_name == "ReaxBondFileIO"
    assert obj_model1.sections[0].fileios[2].class_name == "ThermoFileIO"

    # Populate the model from the dictionnary
    obj_model2 = WorkflowBuilderModel(**obj_dict)
    assert obj_model2.header.major_version == 1
    assert obj_model2.header.minor_version == 0
    assert obj_model2.header.format == "WorkflowBuilder"

    assert obj_model2.sections[0].class_name == "IntegratorSection"
    assert obj_model2.sections[0].integrator.class_name == "NVEIntegrator"
    assert obj_model2.sections[0].fileios[0].class_name == "DumpTrajectoryFileIO"
    assert obj_model2.sections[0].fileios[1].class_name == "ReaxBondFileIO"
    assert obj_model2.sections[0].fileios[2].class_name == "ThermoFileIO"

def test_model_to_building():
    workflow = {
    "header": {
        "format": "WorkflowBuilder",
        "major_version": 1,
        "minor_version": 0,
        "generator": "lammpsinputbuilder"
    },
    "molecular_system": {
        "class_name": "ReaxTypedMolecularSystem",
        "forcefield": 1,
        "bbox_style": 1,
        "electrostatic_method": 2,
        "is_model_loaded": True,
        "forcefield_name": "ffield.reax.Fe_O_C_H.reax",
        "molecule_name": "benzene.xyz",
        "molecule_format": 1,
        "forcefield_content": "DATE: 2011-02-18 UNITS: real CONTRIBUTOR: Aidan Thompson, athomps@sandia.gov CITATION: Aryanpour, van Duin and Kubicki, J Phys Chem A, 114, 6298-6307 (2010) COMMENT Reactive MD-force field: Fe/O/water: Aryanpour, M.; van Duin, A. C. T.; Kubicki, J. D. J. Phys. Chem. A 2010, 114, 6298-6307\n 39       ! Number of general parameters                                        \n   50.0000 !Overcoordination parameter                                          \n    9.5469 !Overcoordination parameter                                          \n    1.6725 !Valency angle conjugation parameter                                 \n    1.7224 !Triple bond stabilisation parameter                                 \n    6.8702 !Triple bond stabilisation parameter                                 \n   60.4850 !C2-correction                                                       \n    1.0588 !Undercoordination parameter                                         \n    4.6000 !Triple bond stabilisation parameter                                 \n   12.1176 !Undercoordination parameter                                         \n   13.3056 !Undercoordination parameter                                         \n  -55.1978 !Triple bond stabilization energy                                    \n    0.0000 !Lower Taper-radius                                                  \n   10.0000 !Upper Taper-radius                                                  \n    2.8793 !Not used                                                            \n   33.8667 !Valency undercoordination                                           \n    6.0891 !Valency angle/lone pair parameter                                   \n    1.0563 !Valency angle                                                       \n    2.0384 !Valency angle parameter                                             \n    6.1431 !Not used                                                            \n    6.9290 !Double bond/angle parameter                                         \n    0.3989 !Double bond/angle parameter: overcoord                              \n    3.9954 !Double bond/angle parameter: overcoord                              \n   -2.4837 !Not used                                                            \n    5.7796 !Torsion/BO parameter                                                \n   10.0000 !Torsion overcoordination                                            \n    1.9487 !Torsion overcoordination                                            \n   -1.2327 !Conjugation 0 (not used)                                            \n    2.1645 !Conjugation                                                         \n    1.5591 !vdWaals shielding                                                   \n    0.1000 !Cutoff for bond order (*100)                                        \n    1.7602 !Valency angle conjugation parameter                                 \n    0.6991 !Overcoordination parameter                                          \n   50.0000 !Overcoordination parameter                                          \n    1.8512 !Valency/lone pair parameter                                         \n    0.5000 !Not used                                                            \n   20.0000 !Not used                                                            \n    5.0000 !Molecular energy (not used)                                         \n    0.0000 !Molecular energy (not used)                                         \n    0.7903 !Valency angle conjugation parameter                                 \n  4    ! Nr of atoms; cov.r; valency;a.m;Rvdw;Evdw;gammaEEM;cov.r2;#            \n            alfa;gammavdW;valency;Eunder;Eover;chiEEM;etaEEM;n.u.               \n            cov r3;Elp;Heat inc.;n.u.;n.u.;n.u.;n.u.                            \n            ov/un;val1;n.u.;val3,vval4                                          \n C    1.3817   4.0000  12.0000   1.8903   0.1838   0.9000   1.1341   4.0000     \n      9.7559   2.1346   4.0000  34.9350  79.5548   5.9666   7.0000   0.0000     \n      1.2114   0.0000 202.6057   8.9539  34.9289  13.5366   0.8563   0.0000     \n     -2.8983   2.5000   1.0564   4.0000   2.9663   0.0000   0.0000   0.0000     \n H    0.8930   1.0000   1.0080   1.3550   0.0930   0.8203  -0.1000   1.0000     \n      8.2230  33.2894   1.0000   0.0000 121.1250   3.7248   9.6093   1.0000     \n     -0.1000   0.0000  61.6606   3.0408   2.4197   0.0003   1.0698   0.0000     \n    -19.4571   4.2733   1.0338   1.0000   2.8793   0.0000   0.0000   0.0000     \n O    1.2450   2.0000  15.9990   2.3890   0.1000   1.0898   1.0548   6.0000     \n      9.7300  13.8449   4.0000  37.5000 116.0768   8.5000   8.3122   2.0000     \n      0.9049   0.4056  59.0626   3.5027   0.7640   0.0021   0.9745   0.0000     \n     -3.5500   2.9000   1.0493   4.0000   2.9225   0.0000   0.0000   0.0000     \n Fe   1.9506   3.0000  55.8450   2.0308   0.1274   0.7264  -1.0000   3.0000     \n     11.0534   2.2637   3.0000   0.0000  18.3725   1.2457   7.3021   0.0000     \n     -1.2000   0.0000  66.4838  30.0000   1.0000   0.0000   0.8563   0.0000     \n    -16.2040   2.7917   1.0338   6.0000   2.5791   0.0000   0.0000   0.0000     \n 10      ! Nr of bonds; Edis1;LPpen;n.u.;pbe1;pbo5;13corr;pbo6                  \n                         pbe2;pbo3;pbo4;Etrip;pbo1;pbo2;ovcorr                  \n  1  1 158.2004  99.1897  78.0000  -0.7738  -0.4550   1.0000  37.6117   0.4147  \n         0.4590  -0.1000   9.1628   1.0000  -0.0777   6.7268   1.0000   0.0000  \n  1  2 169.4760   0.0000   0.0000  -0.6083   0.0000   1.0000   6.0000   0.7652  \n         5.2290   1.0000   0.0000   1.0000  -0.0500   6.9136   0.0000   0.0000  \n  2  2 153.3934   0.0000   0.0000  -0.4600   0.0000   1.0000   6.0000   0.7300  \n         6.2500   1.0000   0.0000   1.0000  -0.0790   6.0552   0.0000   0.0000  \n  1  3 164.4303  82.6772  60.8077  -0.3739  -0.2351   1.0000  10.5036   1.0000  \n         0.4475  -0.2288   7.0250   1.0000  -0.1363   4.8734   0.0000   0.0000  \n  3  3 142.2858 145.0000  50.8293   0.2506  -0.1000   1.0000  29.7503   0.6051  \n         0.3451  -0.1055   9.0000   1.0000  -0.1225   5.5000   1.0000   0.0000  \n  2  3 160.0000   0.0000   0.0000  -0.5725   0.0000   1.0000   6.0000   0.5626  \n         1.1150   1.0000   0.0000   0.0000  -0.0920   4.2790   0.0000   0.0000  \n  1  4 133.0514   0.0000   0.0000   1.0000  -0.3000   1.0000  36.0000   0.0673  \n         0.2350  -0.3500  15.0000   1.0000  -0.1143   4.5217   1.0000   0.0000  \n  2  4 105.0054   0.0000   0.0000  -0.0717   0.0000   0.0000   6.0000   0.0505  \n         0.1000   1.0000   0.0000   1.0000  -0.1216   4.5062   0.0000   0.0000  \n  3  4  65.7713   0.0000   0.0000   0.1366  -0.3000   1.0000  36.0000   0.0494  \n         0.9495  -0.3500  15.0000   1.0000  -0.0555   7.9897   1.0000   0.0000  \n  4  4  38.7471   0.0000   0.0000   0.3595  -0.2000   0.0000  16.0000   0.2749  \n         1.0000  -0.2000  15.0000   1.0000  -0.0771   6.4477   0.0000   0.0000  \n  6    ! Nr of off-diagonal terms; Ediss;Ro;gamma;rsigma;rpi;rpi2               \n  1  2   0.1239   1.4004   9.8467   1.1210  -1.0000  -1.0000                    \n  2  3   0.0283   1.2885  10.9190   0.9215  -1.0000  -1.0000                    \n  1  3   0.1345   1.8422   9.7725   1.2835   1.1576   1.0637                    \n  1  4   0.1358   1.8293  10.0425   1.6096  -1.0000  -1.0000                    \n  2  4   0.0640   1.6974  11.5167   1.3517  -1.0000  -1.0000                    \n  3  4   0.0846   1.4284  10.0808   1.8339  -1.0000  -1.0000                    \n 37    ! Nr of angles;at1;at2;at3;Thetao,o;ka;kb;pv1;pv2                        \n  1  1  1  59.0573  30.7029   0.7606   0.0000   0.7180   6.2933   1.1244        \n  1  1  2  65.7758  14.5234   6.2481   0.0000   0.5665   0.0000   1.6255        \n  2  1  2  70.2607  25.2202   3.7312   0.0000   0.0050   0.0000   2.7500        \n  1  2  2   0.0000   0.0000   6.0000   0.0000   0.0000   0.0000   1.0400        \n  1  2  1   0.0000   3.4110   7.7350   0.0000   0.0000   0.0000   1.0400        \n  2  2  2   0.0000  27.9213   5.8635   0.0000   0.0000   0.0000   1.0400        \n  1  1  3  53.9517   7.8968   2.6122   0.0000   3.0000  58.6562   1.0338        \n  3  1  3  76.9627  44.2852   2.4177 -25.3063   1.6334 -50.0000   2.7392        \n  2  1  3  65.0000  16.3141   5.2730   0.0000   0.4448   0.0000   1.4077        \n  1  3  1  72.6199  42.5510   0.7205   0.0000   2.9294   0.0000   1.3096        \n  1  3  3  81.9029  32.2258   1.7397   0.0000   0.9888  68.1072   1.7777        \n  3  3  3  80.7324  30.4554   0.9953   0.0000   3.0000  50.0000   1.0783        \n  1  3  2  70.1101  13.1217   4.4734   0.0000   0.8433   0.0000   3.0000        \n  2  3  3  75.6935  50.0000   2.0000   0.0000   1.0000   0.0000   1.1680        \n  2  3  2  85.8000   9.8453   2.2720   0.0000   2.8635   0.0000   1.5800        \n  1  2  3   0.0000  25.0000   3.0000   0.0000   1.0000   0.0000   1.0400        \n  3  2  3   0.0000  15.0000   2.8900   0.0000   0.0000   0.0000   2.8774        \n  2  2  3   0.0000   8.5744   3.0000   0.0000   0.0000   0.0000   1.0421        \n  1  4  1  29.1655   3.3035   0.2000   0.0000   1.1221   0.0000   1.0562        \n  1  1  4  59.8697   2.8115   1.9262   0.0000   0.7602   0.0000   1.4056        \n  1  4  4  25.4591  15.9430   0.9664   0.0000   2.2242   0.0000   1.1088        \n  4  1  4  88.6279  26.0015   1.0328   0.0000   0.2361   0.0000   2.0576        \n  2  1  4  47.3695  16.9204   4.1052   0.0000   0.1000   0.0000   1.0050        \n  2  4  2  34.1965   6.6782   6.5943   0.0000   1.3895   0.0000   1.5365        \n  2  2  4   0.1000  30.0000   3.4094   0.0000   2.4379   0.0000   1.5166        \n  4  2  4   0.0000   8.2994   5.7832   0.0000   2.9873   0.0000   1.7716        \n  2  4  4  21.2590   6.5954   0.9951   0.0000   2.8006   0.0000   1.0000        \n  2  4  4 180.0000  -6.9970  24.3956   0.0000   0.7878   0.0000   1.3672        \n  1  3  4  90.0000  12.8684   1.4601   0.0000   0.8757   0.0000   1.0000        \n  3  1  4  18.8567  24.3753   3.9647   0.0000   0.1000   0.0000   1.5314        \n  3  4  3  79.7335   0.0100   0.1392   0.0000   0.4968   0.0000   2.1948        \n  4  3  4  57.6787   4.8566   2.5768   0.0000   0.7552   0.0000   1.0000        \n  2  3  4  59.4556  10.2025   0.7481   0.0000   1.4521   0.0000   1.0000        \n  3  3  4  73.6721  32.6330   1.7223   0.0000   1.0221   0.0000   1.4351        \n  3  4  4  65.7545   5.6268   4.0645   0.0000   1.7794   0.0000   2.6730        \n  3  2  4   0.0000   4.6026   2.5343   0.0000   0.7284   0.0000   1.1051        \n  2  4  3  34.0653  20.1868   4.7461   0.0000   0.1000   0.0000   1.6752        \n 29    ! Nr of torsions;at1;at2;at3;at4;;V1;V2;V3;V2(BO);vconj;n.u;n            \n  1  1  1  1  -0.2500  34.7453   0.0288  -6.3507  -1.6000   0.0000   0.0000     \n  1  1  1  2  -0.2500  29.2131   0.2945  -4.9581  -2.1802   0.0000   0.0000     \n  2  1  1  2  -0.2500  31.2081   0.4539  -4.8923  -2.2677   0.0000   0.0000     \n  1  1  1  3   1.2799  20.7787  -0.5249  -2.5000  -1.0000   0.0000   0.0000     \n  2  1  1  3   1.9159  19.8113   0.7914  -4.6995  -1.0000   0.0000   0.0000     \n  3  1  1  3  -1.4477  16.6853   0.6461  -4.9622  -1.0000   0.0000   0.0000     \n  1  1  3  1   0.4816  19.6316  -0.0057  -2.5000  -1.0000   0.0000   0.0000     \n  1  1  3  2   1.2044  80.0000  -0.3139  -6.1481  -1.0000   0.0000   0.0000     \n  2  1  3  1  -2.5000  31.0191   0.6165  -2.7733  -2.9807   0.0000   0.0000     \n  2  1  3  2  -2.4875  70.8145   0.7582  -4.2274  -3.0000   0.0000   0.0000     \n  1  1  3  3  -0.3566  10.0000   0.0816  -2.6110  -1.9631   0.0000   0.0000     \n  2  1  3  3  -1.4383  80.0000   1.0000  -3.6877  -2.8000   0.0000   0.0000     \n  3  1  3  1  -1.1390  78.0747  -0.0964  -4.5172  -3.0000   0.0000   0.0000     \n  3  1  3  2  -2.5000  70.3345  -1.0000  -5.5315  -3.0000   0.0000   0.0000     \n  3  1  3  3  -2.0234  80.0000   0.1684  -3.1568  -2.6174   0.0000   0.0000     \n  1  3  3  1   1.1637 -17.3637   0.5459  -3.6005  -2.6938   0.0000   0.0000     \n  1  3  3  2  -2.1289  12.8382   1.0000  -5.6657  -2.9759   0.0000   0.0000     \n  2  3  3  2   2.5000 -22.9397   0.6991  -3.3961  -1.0000   0.0000   0.0000     \n  1  3  3  3   2.5000 -25.0000   1.0000  -2.5000  -1.0000   0.0000   0.0000     \n  2  3  3  3  -2.5000  -2.5103  -1.0000  -2.5000  -1.0000   0.0000   0.0000     \n  3  3  3  3  -2.5000 -25.0000   1.0000  -2.5000  -1.0000   0.0000   0.0000     \n  0  1  2  0   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000     \n  0  2  2  0   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000   0.0000     \n  0  2  3  0   0.0000   0.1000   0.0200  -2.5415   0.0000   0.0000   0.0000     \n  0  1  1  0   0.0000  50.0000   0.3000  -4.0000  -2.0000   0.0000   0.0000     \n  0  3  3  0   0.5511  25.4150   1.1330  -5.1903  -1.0000   0.0000   0.0000     \n  1  1  3  3  -0.0002  20.1851   0.1601  -9.0000  -2.0000   0.0000   0.0000     \n  1  3  3  1   0.0002  80.0000  -1.5000  -4.4848  -2.0000   0.0000   0.0000     \n  3  1  3  3  -0.1583  20.0000   1.5000  -9.0000  -2.0000   0.0000   0.0000     \n  1    ! Nr of hydrogen bonds;at1;at2;at3;Rhb;Dehb;vhb1                         \n  3  2  3   2.1200  -3.5800   1.4500  19.5000                                   \n",
        "molecule_content": "12\n Atoms. Timestep: 0\nC 53.88 52.15 50\nC 53.18 53.36 50\nC 51.78 53.36 50\nC 51.08 52.15 50\nC 51.78 50.94 50\nC 53.18 50.94 50\nH 54.96 52.15 50\nH 53.72 54.3 50\nH 51.24 54.3 50\nH 50 52.15 50\nH 51.24 50 50\nH 53.72 50 50\n"
    },
    "sections": [
        {
            "id_name": "defaultSection",
            "class_name": "IntegratorSection",
            "integrator": {
                "id_name": "NVEID",
                "class_name": "NVEIntegrator",
                "group_name": "all",
                "nb_steps": 5000
            },
            "fileios": [
                {
                    "id_name": "fulltrajectory",
                    "class_name": "DumpTrajectoryFileIO",
                    "user_fields": [],
                    "add_default_fields": True,
                    "interval": 10,
                    "group_name": "all",
                    "style": 1
                },
                {
                    "id_name": "bonds",
                    "class_name": "ReaxBondFileIO",
                    "group_name": "all",
                    "interval": 10
                },
                {
                    "id_name": "thermo",
                    "class_name": "ThermoFileIO",
                    "user_fields": [],
                    "add_default_fields": True,
                    "interval": 10
                }
            ],
            "extensions": [],
            "post_extensions": [],
            "groups": [],
            "instructions": []
        }
    ]
}

    obj_model = WorkflowBuilderModel(**workflow)

    dict_obj = obj_model.model_dump()
    builder = WorkflowBuilder()
    builder.from_dict(dict_obj, 0)

    # Generate the LAMMPS inputs
    job_folder = builder.generate_inputs()

    # Get the data and input files
    data_file = job_folder / "model.data"
    input_file = job_folder / "workflow.input"

    assert data_file.is_file()
    assert input_file.is_file()
