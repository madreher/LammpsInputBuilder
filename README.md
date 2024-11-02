# LammpsInputBuilder

[![LIB CI/CD](https://github.com/madreher/lammpsinputbuilder/actions/workflows/ci.yml/badge.svg)](https://github.com/madreher/lammpsinputbuilder/actions/workflows/ci.yml)
[![Coverage badge](https://raw.githubusercontent.com/madreher/lammpsinputbuilder/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/madreher/lammpsinputbuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)
![PyLint](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/madreher/bc29e267d35fad12ca2de2bd7138ecfc/raw/test.json)

## TLDR

LammpsInputBuilder (or LIB) is a Python library designed to generate Lammps inputs from a molecular model, a forcefield, and a high level definition of a simulation workflow.

The goal is to provide an API able to create a Lammps input and data scripts to load a molecular model, assign a forcefield to it, and execute a sequence of operations. The current implementation supports ReaxFF and Rebo potentials for the model defintion, with the possibility to extend to other types of forcefields later on. 

Operations are organized in Sections, where each section is organized around typically but not necessary a time integration operations (minimize, nve, run 0, etc). Each Section can be extended to added addition computations (fix, compute, etc) running at the same time of the main time integration operation. 

With this organization, the main objectives of LammpsInputBuilder are:
- Provide an easy way to generate base Lammps input scripts via a simple Python API
- Create a reusable library of common Sections types to easily chain common operations without having to copy Lammps code
- Make is possible for external tools to generate Lammps inputs via a JSON representation of a workflow (under construction)

Here is a simple example (`examples/tldr.py`) on how to load a molecular model, assign a reax potential to it, and minimize the model: 
```
    from lammpsinputbuilder.types import BoundingBoxStyle, ElectrostaticMethod
    from lammpsinputbuilder.typedmolecule import ReaxTypedMolecularSystem
    from lammpsinputbuilder.workflow_builder import WorkflowBuilder
    from lammpsinputbuilder.section import IntegratorSection
    from lammpsinputbuilder.integrator import MinimizeIntegrator, MinimizeStyle

    modelData = Path('benzene.xyz')
    forcefield = Path('ffield.reax.Fe_O_C_H.reax') 

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
```

## How does a Workflow work?

### Main Objects

A LammpsInputBuilder starts by declaring a `WorkflowBuilder` object. This object is responsible for hosting the workflow definition and converting it into a Lammps script.
The `WorkflowBuilder` is composed of two main parts: a `TypedMolecularSystem`, and a list of `Section`.

<img src="data/images/WorkflowBuilder.svg" alt="WorkflowBuilder chart" height="400" />

A `TypedMolecularSystem` represents a molecular model with a forcefield assigned to it. Currently, LIB supports ReaxFF and Airebo potentials but other could be added in the future. With a `TypedMolecularSystem`, the `WorkflowBuilder` can generate a Lammps data file as well as the beginning of the input script.

A `Section` generally represents a phase in a simulation workflow which could be reused in another workflow. A `Section` can represent a minimization protocol, a NVE, a system warmup, etc. A `Section` can be recursive and be decomposed into a sequence of sub sections as well. A non recursive `Section` is often tied to a integration process (minimize, nve, nvt), but certain `Section` can also be used as a way to modify the current state of the simulation, for instance to reset the timestep counter after a minimization or setup the velocity vectors of the atoms. 

A non recursive `Section` is usually built around an `Integrator` object. The `Integrator` object represents the process advancing the simulation. Current `Integrator` include the `MinimizeIntegrator`, `NVEIntegrator`, or `RunZeroIntegrator`, each of which is responsible for generating a `run` command or equivalent during their execution. In addition to the `Integrator`, a `Section` can host a list of `Group`, `Instruction`, `Extension`, and `FileIO` objects. A `Group` object represents a list of atoms selected based on different criterias. This object is a wrapper around the different ways Lammps offers to create atom selections. The `Instruction` object is a wrapper around commands which modify the current state of the simulation but without involving any time integration step. The `FileIO` objects are wrapper around the different methods that Lammps offer to write trajectory files during the time integration process. Finally, `Extension` objects are wrapper around different additionnal computations (`fix`, `compute`) which are being executed at the same time as the `Integrator`.

**Important**: A `Section` represents a scope for all the objects within it. The `Integrator`, `Group`, `Extension`, and `FileIO` objects assigned within the `Section` are declared at the start of the `Section` and but are also **removed** at the end of the `Section`. Consequently, if a following `Section` needs to use a `Group` previously declared, it will have to declare it again. This approach was chosen to enforce the clean deletion of every identifier during the execution of the Lammps script. Note that in the case of the `RecursiveSection`, the scope of the `Group`, `Extension`, and `FileIO` objects is visible to all the sub sections within the `RecursiveSection` and can thus be used by its sub sections.

Finally, the last category of objects is the `TemplateSection`. A `TemplateSection` is the base class to definie high level tasks which may be composed one or several `Section` objects. The example, the class `MinimizeTemplate` provide a high level object to define a minimization and specify a group of anchors without the need for the user to know how to setup anchors during a minimization. To create a new task, the developer need to extend the class `TemplateSection` and implement the methods `generate_sections()` if the task can be decomposed in sections, and override the function `add_all_commands()` if the `TemplateSection` does not follow organization of the `TemplateSection`. 

![Section Organization](data/images/Sections.svg)

### Unrolling the workflow into a Lammps script and data file

Once a `WorkflowBuilder` is fully configured, its role is to produce the Lammps script and data file implementing the workflow provided by the user.

#### Concept of Do and Undo

In Lammps, a lot of commands have a declaration and removal command which should be called to declare an action with an ID and stop the action associated with the ID. The typical commands are:
 - `fix`, `unfix`
 - `compute`, `uncompute`
 - `group ID style ...`, `group ID delete`

LammpsInputBuilder maintain this logic by requiring all its types of objects to provide a *do* and *undo* command whenever relavant. The only exceptions to this rule are the `Instruction` objects which do not have an *undo* counter part. For example, the command `reset_timestep` simply sets the `step` counter to a new value, therfor it doesn't need to be stopped or undone, it is a simple one time action. 

#### Unrolling the TypedMolecularSystem

The first step is to translate the `TypedMolecularSystem` object. The data file is generated internally by [ASE](https://wiki.fysik.dtu.dk/ase/). The initial Lammps input script is based on a preconfigured template with the necessary adjustements to account for the type of forcefield used.

Dev note: This is a sufficient approach for now because LIB only supports ReaxFF and Airebo potentiel which only requires the Atom section in the Lammps data file. Other forcefield might require a different approach or backend (ex: [moltemplate](https://www.moltemplate.org/)).

Examples of Lammps files produced for a benzene with a ReaxFF potential. 

Lammps data:
```
# Generated by LammpsInputBuilder
12 	 atoms 
2  atom types
0.0	104.96000000000001 xlo xhi
0.0	104.3 ylo yhi
0.0	100.0 zlo zhi

Masses

1 12.011 # C
2 1.008 # H

Atoms # full

     1   0   1   0.0      53.880000000000003      52.149999999999999                      50
     2   0   1   0.0                   53.18      53.359999999999999                      50
     3   0   1   0.0      51.780000000000001      53.359999999999999                      50
     4   0   1   0.0      51.079999999999998      52.149999999999999                      50
     5   0   1   0.0      51.780000000000001      50.939999999999998                      50
     6   0   1   0.0                   53.18      50.939999999999998                      50
     7   0   2   0.0      54.960000000000001      52.149999999999999                      50
     8   0   2   0.0      53.719999999999999      54.299999999999997                      50
     9   0   2   0.0      51.240000000000002      54.299999999999997                      50
    10   0   2   0.0                      50      52.149999999999999                      50
    11   0   2   0.0      51.240000000000002                      50                      50
    12   0   2   0.0      53.719999999999999                      50                      50
```

Lammps input:
```
# -*- mode: lammps -*-
units          real
atom_style     full
atom_modify    map hash
newton         on
boundary       p p p
read_data       model.data
pair_style     reaxff NULL mincap 1000
pair_coeff     * * ffield.reax.Fe_O_C_H.reax C H
fix            ReaxFFSpec all qeq/reaxff 1 0.0 10.0 1e-8 reaxff
neighbor       2.5 bin
neigh_modify   every 1 delay 0 check yes
compute reax   all pair reaxff
variable eb    equal c_reax[1]
variable ea    equal c_reax[2]
variable elp   equal c_reax[3]
variable emol  equal c_reax[4]
variable ev    equal c_reax[5]
variable epen  equal c_reax[6]
variable ecoa  equal c_reax[7]
variable ehb   equal c_reax[8]
variable et    equal c_reax[9]
variable eco   equal c_reax[10]
variable ew    equal c_reax[11]
variable ep    equal c_reax[12]
variable efi   equal c_reax[13]
variable eqeq  equal c_reax[14]
```

#### Unrolling the Extension, FileIO, and Group objects

All the `Extension`, `FileIO`, and `Group` objects implement the function `add_do_commands()` and `add_undo_commands()` command to declare and stop respectively their actions. These functions are responsible for converting from their respecting objects to Lammps commands. The separation of *do* and *undo* allows other objects to be able to manipulate the scope or lifetime of these objects as necessary. 

Dev note on `ThermoIO`: The *thermo* keyword in Lammps works differently than the other `FileIO` objects. In particular, a *thermo* is always active and part of the `log.lammps` file. Therefore the `ThermoIO` doesn't have a scope per say. Instead, declaring a new `ThermoIO` object will override the previous IO settings and replace them with the new object settings. See [here](https://docs.lammps.org/thermo_style.html) for more information about thermo in Lammps. 

Examples:
```
from lammpsinputbuilder.fileIO import ReaxBondFileIO
from lammpsinputbuilder.types import GlobalInformation

obj = ReaxBondFileIO(fileio_name="testFile", interval=10, group=AllGroup())
info = GlobalInformation() # Object automatically generated by the WorkflowBuilder
print(obj.add_do_commands(info))
print(obj.add_undo_commands())
```

Output:
```
fix testFile all reaxff/bonds 10 bonds.testFile.txt
unfix testFile
```

#### Unrolling the Instructions objects

Unlike the previous objects, the `Instruction` objects doesn't have a *undo* operation available to them. Consequently, they implement the function `write_instruction()` to convert the object to Lammps commands. Because of this, `Instruction` objects as well do not have a notion of scope. They simply perform their task one time and the script continues. 

Example:
```
from lammpsinputbuilder.instructions import SetTimestepInstruction
from lammpsinputbuilder.types import GlobalInformation
from lammpsinputbuilder.quantities import TimeQuantity, LammpsUnitSystem

instruction = SetTimestepInstruction(instruction_name="defaultSetTimestep", timestep=TimeQuantity(20, "fs"))
info_real = GlobalInformation()
info_real.set_unit_style(LammpsUnitSystem.REAL)
print(instruction.write_instruction(info_real))
```

Output:
```
timestep 20.0
```

#### Unrolling the Integrator objects

The `Integrator` objects are responsible for declaring the base process which is going to advance the step counter of the simulation. In most cases, that means in particular executing the Lammps `run` command in addition to the method to use for the time integration during that `run`. There are exceptions though such as the `minimize` command which technically doesn't use the `run` command but still involve some type of multistep process. 

The `Integrator` object implements up to three methods: `add_do_commands()`, `add_undo_commands()`, and `add_run_commands()`. The `add_do_commands()` and `add_undo_commands()` methods have the same as the other objects, i.e declare the necessary computation to perform and stop them respectively. The `add_run_commands()` is specific to the `Integrator` objects and is responsible for specifying how to trigger the computation. This is usually done by specify a `run` command. Note that an `Integrator` may only need to implement some of these methods.

Example:
```
from lammpsinputbuilder.integrator import NVEIntegrator
from lammpsinputbuilder.group import AllGroup
from lammpsinputbuilder.types import GlobalInformation

integrator = NVEIntegrator(integrator_name="myIntegrator", group=AllGroup(), nb_steps=1000)
print(integrator.add_do_commands(info))
print(integrator.add_run_commands())
print(integrator.add_undo_commands())
```

Output:
```
fix myIntegrator all nve
run 1000
unfix myIntegrator
```

#### Unrolling Section objects

A `Section` object represents a scope during which one or several computations or actions will be performed. Each object belonging to the `Section` object will be declared at the beginning of the `Section` and removed at the end of the `Section`.

A `Section` object is meant to be self-sufficient, as is it the object responsible for other objects. Consequently, a `Section` only needs to implement the method `add_all_commands()`. This way, unrolling a list of `Section` object simply requires to call to method `add_all_commands()` in a sequence on all the `Section` objects.

There are several types of `Section` objects which all follow a similar logic to convert its object into Lammps commands. The simplest object is the `IntegratorSection` which hosts
a `Integrator` object and optionnal `Group`, `Instruction`, `Extension`, and `FileIO` objects. The lifetime of these objects are tied to the lifetime of the `Section` object.
It does so by calling the methods `add_do_commands()` and `add_undo_commands()` in the right order. 

The `IntegratorSection` unrolls in the following order:
* Do list of Groups
* Do list of Instructions
* Do list of Extensions
* Do Integrator
* Do list of post Extensions
* Do list of FileIO
* Run Integrator
* Undo reverse list of FileIO
* Undo reverse list of post Extensions
* Undo Integrator
* Undo reverse list of Extensions
* Undo reverse list of Groups

This order ensures that the commands are declared in the right order, and removed in the right order as well. The LIFO approach to *undo* guarantees that commands which may depend on each other are stopped cleanly. For example, if we declare the command A, followed by B and that B depends on A to function, we will have to remove B first before removing A.

The `IntegratorSection` does include two spots to declare `Extensions`: before and after the `Integrator` with the methods `add_extension(Extension)` and `add_post_extension(Extension)` respectively. In the large majority of cases, the `Extension` objects should be declared as regular `Extension` with the `section.add_extension(ext)` method. However, some Lammps commands have to be declared after the declaration of the time integration method (ex: [bond/break](https://docs.lammps.org/fix_bond_break.html)). For these cases, users should use the method `section.add_post_extension(post_ext)`.

Other `Section` objects follow a very similar pattern with the difference mainly being that the center piece of the `Section` may be a different object than an `Integrator`. For instance, the `RecursiveSection` has a list of `Section` objects to execute in the middle. Several examples are provided below to see how different `Section` types can be used in practice. 

### Handling of Units 

Many parameters of Lammps commands represent a quantity with unit such as temperature, length, etc. In Lammps, the [unit system](https://docs.lammps.org/units.html) used is declared at the beginning of input script and is usually determined by which type of forcefield is used. 

This can be a challenge because commands parameters need to follow the unit system used. A major goal of LIB is to be able to make the definition of a workflow independant from the system definition unit. If the command's parameters are declared with only a simple value, a given workflow definition could only be used for potentials which are based on the same unit set.

To avoid this problem and make a workflow definition agnostic of a given unit set, LIB wraps numerical parameters into `Quantity` objects representing different physical properties. A `Quantity` object represents a type of physical property, a numerical value, and a unit associated with it. A `Quantity` type exists for each type of units declared in Lammps (temperature, length, force, etc). A `Quantity` object can be converted to a new unit on demand. This is done by using [Pint](https://pint.readthedocs.io/en/stable/) in the backend.

When converting the workflow into Lammps commands, the `WorkflowBuilder` knows which unit style is used, and can therefor require to convert all the `Quantity` objects to the right units when writting commands. This mechanism ensures that a user can define a workflow once, and change the Lammps unit set at will without having to update every physical quantities. 

Example:
```
from lammpsinputbuilder.quantities import TimeQuantity, LammpsUnitSystem

timestep=TimeQuantity(20, "fs")
timestep.get_magnitude() # print 20
timestep.get_units() # print "fs"

timestep.convert_to(LammpsUnitSystem.METAL) # print 0.02 , Lammps metal unit style is in ps
```

## Workflow examples

### Minimize, Warm Up, and NVE

In this example, we are going to model a single benzene molecule in vacuum. First, we load the molecular system and assign a force field onto it, e.g. ReaxFF. Next, we create a simple workflow composed of 3 stages: energy minimization, heating from 0K to 300K, relaxation at 300K.

#### Molecule model definition and potential assignement

The first step is to declare a model and assign a forcefield to it. In this example, we are going to use the benzene molecule with a reaxff potential file. This is done with the following code:

```
    modelData = Path(__file__).parent.parent / 'data' / 'models' / 'benzene.xyz'
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'ffield.reax.Fe_O_C_H.reax'

    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(modelData, forcefield)

    # Create the workflow. In this case, it's only the molecule
    workflow = WorkflowBuilder ()
    workflow.set_typed_molecular_system(typedMolecule)
```

The `ReaxTypedMolecularSystem` object represents the molecular system with its settings. Currently, we only need to setup the periodic condition style and the partial charges method. Additional settings may become available in the future. Once the `TypedMolecularSystem` object is created and initialized, it can be added to a `WorkflowBuilder` object. With this base, we can start to add `Section` objects to the workflow.

#### Minimization phase

In the first `Section`, we are going to minimize the model. This can be done by using a `IntegratorSection` with a `MinimizeIntegrator` object as follows:
```
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
```
For this example, we won't use any additionnal extensions or file ios. Once the section is fully declared, it can be added to the `WorkflowBuilder` object.

#### Warmup phase

Now that the model is minimized, we can warm up the molecular system in the second `Section`. To do so, we are going to use a `langevin` thermostat to raise the temperature of the system to 300K. A `langevin` thermostat must be used in conjonction to a process doing the time integration. In this case, we are going to use a `nve`. This can be done as follows:

```
    # Create a Langevin Section
    sectionWarmup = IntegratorSection(
        integrator=NVEIntegrator(
            integrator_name="warmup",
            group=AllGroup(),
            nb_steps=10000
        )
    )
    langevinWarmup = LangevinExtensioln(
        extension_name="langevin",
        group=AllGroup(), 
        start_temp=TemperatureQuantity(1, "K"),
        end_temp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    sectionWarmup.add_extension(langevinWarmup)
    workflow.add_section(sectionWarmup)
```
During this phase, we created a new `IntegratorSection` but this time with a `NVEIntegrator`. The `NVEIntegrator` will take care of declaring a `fix nve` and advancing the simulation. The langevin thermostat can be added via an `Extension` object with parameters following the [Lammps documentation](https://docs.lammps.org/fix_langevin.html). Note that the langevin extension has parameters representing temperature and time and relies on their respective `Quantity` objects. 

#### Relaxation phase

To complete this example, we are going to run an equilibration phase at 300K with the addition of trajectories. Running the equilibration phase is almost identical to the previous phase, except that the langevin thermostat will remain at constant temperature. During this run, we are going to add a trajectory for atom properties, bond properties, and explicit thermo fields. This can be achieved as follows:
```
    # Create a NVE Section
    sectionNVE = IntegratorSection(integrator=NVEIntegrator(
        integrator_name="equilibrium",
        group=AllGroup(),
        nb_steps=100000
    ))
    langevinWarmup = LangevinExtensioln(
        extension_name="langevin",
        group=AllGroup(), 
        start_temp=TemperatureQuantity(300, "K"),
        end_temp=TemperatureQuantity(300, "K"),
        damp=TimeQuantity(1, "ps"),
        seed=12345
    )
    pos = DumpTrajectoryFileIO(fileio_name="fulltrajectory", add_default_fields=True, interval=10, group=AllGroup())
    sectionNVE.add_fileio(pos)
    bonds = ReaxBondFileIO(fileio_name="bonds", interval=10, group=AllGroup())
    sectionNVE.add_fileio(bonds)
    thermo = ThermoFileIO(fileio_name="thermo", add_default_fields=True, interval=10)
    sectionNVE.add_fileio(thermo)

    workflow.add_section(sectionNVE)
```
Just like `Extension` objects, the `FileIO` objects are added to their respective section and will only be active during the duraction of that phase. Note that for the thermo io, we are using the `TypedMolecularSystem` object to obtain several variable names. This is because the pair command associated to the forcefield can produce dedicated values. This approach allows the `ThermoFileIO` to adapt to the type of forcefield used without having to modify it later on if the `TypedMolecularSystem` object changes.

Now that all the phases are declared and added to the workflow, the Lammps inputs can be generated as follow:
```
    # Generate the inputs
    job_folder = workflow.generate_inputs()

    logger.info(f"Inputs generated in the job folder: {job_folder}")

```
This code will produce all the necessary inputs in a job folder ready to be executed. The complete code of this example can be found at `examples/simpleNVE.py`.


### Scan of a surface with a tip

In this example, we are going to use a passivated slab and a molecular tooltip where the head of the tooltip has an open valence. The goal of this exemple is to move the tooltip above the slab, perform a single point energy calculation at each step, and for each step analyse the potential energy of the system as well as the list of bonds in the system. We are going to model our system using ReaxFF. As we move the tip above the surface, we will export the bonds that will form and break dynamically.

![Passivated slab and tooltip with open head](data/images/slabHeadDepassivated.png)

**IMPORTANT**: The code snippets provided are extracted from `examples/scanSlab.py` and may not be complete for the sake of space. Please refer to the complete example for a working example out of the box. To run the example, you can do as follow from the source folder:
```
cd examples
python3 scanSlab.py --lmpexec ~/dev/lammps/lammps-17Apr2024/build/install/bin/lmp --model headopen --zplane 1.5 --deltaxy 0.5 --loglevel INFO --min-bond-order 0.6
```
Please make sure to update the path to the lammps executable (`--lmpexec` option) to match the location of `lmp` to your machine.

The first step in this process is to determine the atom indices of the groups we are going to use. I used [Radahn](https://github.com/madreher/radahn) to visualize the model and do the selection. Other tools like [Ovito](https://www.ovito.org/) or [VMD](https://www.ks.uiuc.edu/Research/vmd/) may allow to do the same task. OVerall, we are defining 5 selections:
- The entire slab
- The entire tooltip
- The anchor of the slab (bottom layer of the slab)
- The anchor of the tooltip (top layer of the tooltip)
- The head, i.e the last atom at the bottom of the tooltip

![Group decomposition of the model](data/images/SlabGroups.svg)

With this being done, we can start to load the molecular model with LammpsInputGenerator. This is done as follows:

```
    # Load the model to get atom positions
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'Si_C_H.reax'
    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(xyzPath, forcefield)
    workflow = WorkflowBuilder ()
    workflow.set_typed_molecular_system(typedMolecule)
```

#### Phase 1: Minimization

The molecular system XYZ coordinates need to be adjusted to lower the initial energy prior to running any time-dependant simulation. We are first going to create a workflow only dedicated to the minimization process. One important aspect of this model is that it contains anchors and free atoms. Therefore, we put the atoms into specific groups to treat them independently. The force applied onto the anchors must be set to zero to prevent them from moving during the energy minimization step. LIB provides a convenient `Template` to implement this protocol. See also [setforce](https://docs.lammps.org/fix_setforce.html) command from Lammps. The minimization can then be done as follows:
```
    # Declare the arrays of selections (check examples/scanSlab.py for the list of indices)
    indiceAnchorTooltip = [...]
    indicesSlab = [...]
    indiceHead = [338]
    indicesTooltip = [...]

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

    # We are going to use the groupAnchors as well during the minimization, create a reference for it 
    # The reference is necessary to prevent the sectionMinimize to delete the group at the end of the section.
    refGroupAnchor = ReferenceGroup(group_name="refAnchor", reference=groupAnchors)

    sectionMinimization = MinimizeTemplate(section_name="MinimizeSection", style=MinimizeStyle.CG, etol = 0.01, ftol = 0.01, maxiter = 100, maxeval = 10000, useAnchors=True, anchorGroup=refGroupAnchor)
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

    # Get the final XYZ state
    finalXYZ = finalDump.get_associated_file_path()
```
Setting up the minimization is done in several phases:
- Define the different list of indices corresponding to our selections
- Create a `RecursiveSection` as we will want to run multiple `Section` objects
- Create the `Group` objects and assign them to the `RecursiveSection` object.
- Create the `MinimizeTemplate` object with the specification of the anchor group
- Create a second section which is going to run a single point energy calculation to save the state of the system after the minimization.

During this phase, we introduced two new objects: the `MinimizeTemplate` and the `ReferenceGroup` object. The `MinimizeTemplate` is a dedicated `Template` object designed to make easier the creation of a minimization process when anchors are involved. One problem with this setup though is that it does require a `Group` to specify the atoms part of the anchor. However, because the anchor group is given to the `MinimizeTemplate`, LIB has to consider that the `Group` is part of the `MinimizeTemplate` scope, and will therefor delete it at the end of `MinimizeTemplate`. This is not desirable in this case because that group was declared as part of the `RecursiveSection` and we would want its lifetime to be tied to the `RecursiveSection` and not the `MinimizeTemplate`. To address this problem, LIB offers the `ReferenceGroup`. This group object is like a pointer to another group without owning the referred group. This way, when the `ReferenceGroup` gets out of scope at the end of the `MinimizeTemplate`, it won't delete the group it refers to, i.e the anchor group in this case.

#### Phase 2: Scan

In this phase, we are going to displace the tooltip to various positions above the above the slab. The tooltip will follow a grid at a given height. To define the grid position, we first need to know the bounding box of the slab after minimization. To do so, we are going to create a new `TypedMolecularSystem` and load the model that we generated after the minimization. This can be done as follows:
```
    # Load the model to get atom positions
    xyzPath = previousJobFolder / finalXYZ
    forcefield = Path(__file__).parent.parent / 'data' / 'potentials' / 'Si_C_H.reax'
    typedMolecule = ReaxTypedMolecularSystem(
        bbox_style=BoundingBoxStyle.PERIODIC,
        electrostatic_method=ElectrostaticMethod.QEQ
    )
    typedMolecule.load_from_file(xyzPath, forcefield)
```
Once the model is loaded, we need to compute the bounding box of the slab specifically. To do so, we need the list of atom indices forming the slab that we have defined previously, and the current positions. Internally, the `TypedMolecularSystem` object stores a ASE [Atoms](https://wiki.fysik.dtu.dk/ase/ase/atoms.html) object which can be querried to access atom positions. This can be done as follows:
```
    # Get the positions and the list of atoms for the slab to compute its bounding box
    positions = typedMolecule.get_ase_model().get_positions()
    slabIndicesZeroBased = np.array(indicesSlab) - 1
    slabPositions = np.take(positions, slabIndicesZeroBased, axis=0)

    # Compute the bounding box oif the slab
    slabBoundingBox = np.min(slabPositions, axis=0), np.max(slabPositions, axis=0)
```
Note that the previous selection we used was 1-based because Lammps count indices from 1. We need to generate a new list of indices starting from 0 instead for ASE to get the right positions. 

Now that we have the bounding box of the slab, we need to get the current position of the head of the tooltip:
```
    # Get the position of the head 
    headInitialPosition = positions[indiceHead[0] - 1]
```

Now we have all the information needed to define the grid above the slab. The grid is defined by a 3 user settings: dx, dy, dz where dx and dy are the spacing we want on the grid between 2 data points, and dz is the desired different between the top height of the slab and the head of the tooltip.

The x,y coordinates can be generated as follow:
```
    desiredZDelta = 1.5
    desiredXDelta = 0.5
    desiredYDelta = 0.5
    logger.info(f"Generating trajectory with the following parameters: zplane={zplane}, xdelta={desiredXDelta}, ydelta={desiredYDelta}")
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
```
During the generation of the grid, we save the corresponding tooltip positions for the head as well as the 2D coordinate on the grid. This will be useful later on when we will want to analyse the files produced. Now that we have collected all the positions where we want to move the tooltip, we can create the desired workflow.
```
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
        moveForwardSection.add_instruction(instruction=DisplaceAtomsInstruction(instruction_name="moveforward", group=ReferenceGroup(group_name="tooltip", reference=groupTooltip), 
                                                                        dx=LengthQuantity(value=headTargetPosition[0] - headInitialPosition[0], units="lmp_real_length"),
                                                                        dy=LengthQuantity(value=headTargetPosition[1] - headInitialPosition[1], units="lmp_real_length"),
                                                                        dz=LengthQuantity(value=headTargetPosition[2] - headInitialPosition[2], units="lmp_real_length")))
        speSection = IntegratorSection(section_name="SPESection", integrator=RunZeroIntegrator())
        dumpIO = DumpTrajectoryFileIO(fileio_name=f"{headPixel[i][0]}_{headPixel[i][1]}", style=DumpStyle.CUSTOM, user_fields=["id", "type", "element", "x", "y", "z"], interval=1, group=AllGroup())
        trajectoryFiles.append(dumpIO.get_associated_file_path())
        bondIO = ReaxBondFileIO(fileio_name=f"{headPixel[i][0]}_{headPixel[i][1]}", group=AllGroup(), interval=1)
        bondFiles.append(bondIO.get_associated_file_path())
        thermoIO = ThermoFileIO(fileio_name=f"{headPixel[i][0]}_{headPixel[i][1]}", interval=1, user_fields=typedMolecule.get_default_thermo_variables())
        speSection.add_fileio(dumpIO)
        speSection.add_fileio(bondIO)
        speSection.add_fileio(thermoIO)
        moveBackwardSection = InstructionsSection(section_name="MoveBackwardSection")
        moveBackwardSection.add_instruction(instruction=DisplaceAtomsInstruction(instruction_name="movebackward", group=ReferenceGroup(group_name="tooltip", reference=groupTooltip), 
                                                                        dx=LengthQuantity(value=headInitialPosition[0] - headTargetPosition[0], units="lmp_real_length"),
                                                                        dy=LengthQuantity(value=headInitialPosition[1] - headTargetPosition[1], units="lmp_real_length"),
                                                                        dz=LengthQuantity(value=headInitialPosition[2] - headTargetPosition[2], units="lmp_real_length")))
        stepSection.add_section(moveForwardSection)
        stepSection.add_section(speSection)
        stepSection.add_section(moveBackwardSection)
        globalSection.add_section(stepSection)


    workflow.add_section(globalSection)

    # Generate the inputs
    job_folder = workflow.generate_inputs()
    logger.info(f"Scan inputs generated in the job folder: {job_folder}")
```
The important part of this workflow is within the for loop. For each coordinate, we create a `Section` which will displace the tooltip to the right position, perform a single point energy calculation to calculate the potential energy of the system as well as get the bond pairs from reax. Once this is done, we displace back the tooltip to its original position. 

Note that it would be possible to simply follow a path from a coordinate to the next without getting back to the original position. However, this approach would introduce small numerical drifts over time and the tooltip would not end up being exactly where we want it to be after a large number of displacements. Going back to the starting position each time avoid accumulating these small errors. 

Another important note is that at no point we perform a time integration step. In particular, the tooltip is *displaced* but not *moved* which are different in Lammps semantic. 

Once this is done, we can run the workflow. This workflow will produce two files per frame. In the script `examples/scanSlab.py`, we added a postprocessing step to concatenate all the files into a single trajectory file for simplicity and moved all the individual frame files into a subfolder.

This workflow produced the following trajectory:
![Trajectory of the scan, 1/10 frame](data/video/scan_traj_openhead.gif)

#### Phase 3: Analysis

This phase is outside the scope of `LammpsInputBuilder`, but is still provided in the interest of providing a complete experiment from input preparation to analysis.

The first analysis we are going to do is to generate an image of the potential energy to observe its variations depending on the position of the tooltip. For each tooltip position, we stored a 2D coordinate which will correspond to a pixel on an image.

We are going to rely on `matplotlib` to generate the corresponding image and `lammps_logfile` to read the potential energy from the log file.

The image can be generated as follows:
```
    # First, create an empty array
    data = np.zeros((headPixel[-1][0] + 1, headPixel[-1][1] + 1), dtype=np.float64)

    # Get the log file 
    logFile = job_folder / "log.lammps"
    log = lammps_logfile.File(logFile)

    # Loop over the frames
    for i in range(len(headPixel)):
        # Get the frame
        dataFrame = log.get(entry_name="PotEng", run_num=i)
        # Some frames can have ["warning"] as their first value, query for the last one to be safe
        data[headPixel[i][0], headPixel[i][1]] = dataFrame[-1]

    # Create a colormap with mathplotlib
    cmap = plt.get_cmap('inferno')
    plt.imshow(data, cmap=cmap, origin='lower')
    plt.colorbar()
    plt.savefig(job_folder / "potentialEnergyMap.png")
    plt.clf()
```
This will generate the following image:
![Potential Energy](data/images/potentialEnergyMap_headopen_xy0-5_z1-5.png)

This picture shows the total potential energy of the system as a function of the XY coordinates of the tooltip above the slab.

Another question we would like to answer is: does the bonds rearrange themselves when the tooltip is displaced? In particular, the head of a tooltip has an open valence and could potentially grab a hydrogen on the surface. 

To evaluate this, we are going to draw another image where the color is going to represent a given set of bond pairs. Consequently, different colors will means that some bonds have rearranged. This can be done as follows:
```
    # We create an image where each pixel corresponds to a bond configuration, i.e an set of bond pairs
    # Currently, we only consider bond pairs, regardless of the type. Should probably be refined in the next iteration

    colorMap = {}
    data = np.zeros((headPixel[-1][0] + 1, headPixel[-1][1] + 1), dtype=np.int32)

    frameFolder = job_folder / "frames"
    currentID = 0
    totalIgnoredBondPaired = 0
    logger.info("Start computing bond configurations with a minimum bond order of " + str(minbondOrder))

    for i in range(len(headPixel)):

        bondsFile = frameFolder / f"bonds.{headPixel[i][0]}_{headPixel[i][1]}.txt"
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
```

For each frame, we read the list of bonds produced by ReaxFF to determinate the available bond pairs. We filter out the bond pairs which have a bond order deemed too low to be meaningful. Once we have the full list of bond pairs, we sort the list of bonds and generate a unique ID identifying this specific list. Sorting the list of bonds is mandatory to ensure that two arrays with the same list of bonds but in a different order would become the same list and therfor end up with the same unique ID. When a new frame is read and an ID is gennerated, we check if we have already encountered this ID. If no, we assign a new color to the ID and store it. If yes, we assign the color associated to this ID to the current pixel. 

This will produce the following image:
![Map of bond individual configurations](data/images/bondConfigurationMap_headopen_xy0-5_z1-5.png)

With this picture, we see that the scan generates a total of 10 different bond lists. For most of the scan (dark blue), no new bonds are performed. However, the scan does show some spots on the surface where the tooltip is likely close enough to the surface to interact with its hydrogen atoms. With this image, the user can quickly go back to individual frames to see what happens in these spots of interest.

For a full working example of this workflow, please refer to the script `examples/scanSlab.py`.

## Dev Section

### Build and upload the package on the test repo

Source: https://packaging.python.org/en/latest/tutorials/packaging-projects/

Register an account for testpypi: https://test.pypi.org/account/register/
Register an account for pypi: https://pypi.org/account/register/
Create the file ~/.pypirc and add the token api after generating it in the testpypi and/or pypi account.

The file should look like this:
```
[testpypi]
  username = __token__
  password = <pwd>

[pypi]
  username = __token__
  password = <pwd>
```


Then you can build and upload the package: 

```
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload --repository pypi dist/*
```

The package is available at the address: https://test.pypi.org/project/lammpsinputbuilder/0.0.3/ and https://pypi.org/project/lammpsinputbuilder/0.0.3/

To install the package:
```
python3 -m venv test-lib
source test-lib/bin/activate
pip3 install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple lammpsinputbuilder==0.0.3
# OR
pip3 install -i https://pypi.org/simple/ lammpsinputbuilder==0.0.3
``` 

### Upload package by Github actions

The Github workflow needs to be declared in the test Pypi repo. This can be done here: https://test.pypi.org/manage/project/lammpsinputbuilder/settings/publishing/






