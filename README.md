# LammpsInputBuilder

[![LIB CI/CD](https://github.com/madreher/lammpsinputbuilder/actions/workflows/ci.yml/badge.svg)](https://github.com/madreher/lammpsinputbuilder/actions/workflows/ci.yml)
[![Coverage badge](https://raw.githubusercontent.com/madreher/lammpsinputbuilder/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/madreher/lammpsinputbuilder/blob/python-coverage-comment-action-data/htmlcov/index.html)

## TLDR

LammpsInputBuilder (or LIB) is a Python library designed to generate Lammps inputs from a molecule file and a workflow high level definition.

The goal is to provide an API able to create a Lammps input and data scripts to declare a model followed by a sequence of operations. The current implementation supports ReaxFF and Rebo potentials for the model defintion, with the possibility to extend to other types of forcefields later on. 

Operations are organized in Sections, where each section is organized around typically but not necessary a time integration operations (minimize, nve, run 0, etc). Each Section can be extended to added addition computations (fix, compute, etc) running at the same time of the main time integration operation. 

With this organization, the main objectives of LammpsInputBuilder are as follows:
- Provide an easy way to generate base Lammps input scripts via a simple Python API
- Create a reusable library of common Sections types to easily chain common operations without having to copy Lammps code
- Make is possible for external tools to generate Lammps inputs via a JSON representation of a workflow (under construction)

## How does a Workflow work?

### Main Objects

A LammpsInputBuilder starts by declaring a `WorkflowBuilder` object. This object is responsible for hosting the workflow definition and converting it into a Lammps script.
The `WorkflowBuilder` is composed of two main parts: a `TypedMolecule`, and a list of `Section`.

<img src="data/images/WorkflowBuilder.svg" alt="WorkflowBuilder chart" height="400" />

A `TypedMolecule` represent a molecular model with a forcefield assigned to it. Currently, LIB supports ReaxFF and Airebo potentiels but other could be added in the future. With a `TypedMolecule`, the `WorkflowBuilder` can generate a Lammps data file as well as the beginning of the input script.

A `Section` generally represents a phase in a simulation workflow which could be reuse in another workflow. A `Section` can represent a minimization protocol, a NVE, a system warmup, etc. A `Section` can be recursive and be decomposed to another sequence of sub sections as well. A non recursive `Section` is often tied to a time integration process (minimize, nve, nvt), but certain `Section` can also be used as a way to modify the current state of the simulation, for instance to reset the timestep counter after a minimization or setup the velocity vectors of the atoms. 

A non recursive `Section` is usually built around an `Integrator` object. The `Integrator` object represents the process advancing the simulation. Current `Integrator` include the `MinimizeIntegrator`, `NVEIntegrator`, or `RunZeroIntegrator`, each of which are responsible to generate a `run` command or equivalent in their execution. In addition to the `Integrator`, a `Section` can host a list of `Group`, `Instruction`, `Extension`, and `FileIO` objects. A `Group` object represents a list of atoms selected based on different criteria. This object is a wrapper around the different Lammps offers to create atom selections. The `Instruction` object is a wrapper around commands which modify the current state of the simulation but without involving any time integration step. The `FileIO` objects are wrapper around the different methods that Lammps offer to write trajectory files during the time integration process. Finally, `Extension` objects are wrapper around different additionnal computations (`fix`, `compute`) which are being executed at the same time as the `Integrator`.

**Important**: A `Section` represents a scope for all the objects within it. The `Integrator`, `Group`, `Extension`, and `FileIO` objects assigned within the `Section` are declared at the start of the `Section` and but are also **removed** at the end of the `Section`. Consequently, if a following `Section` needs to use a `Group` previously declared, it will have to declare it again. This approach was chosen to enforce the clean deletion of every identifier during the execution of the Lammps script. Note that in the case of the `RecursiveSection`, the scope of the `Group`, `Extension`, and `FileIO` objects is visible to all the sub sections within the `RecursiveSection` and can thus be used by its sub sections.

![Section Organization](data/images/Sections.svg)

### Unrolling the workflow into a Lammps script and data file

Once a `WorkflowBuilder` is fully configured, its role is to produce and Lammps script and data file implementing the workflow provided by the user.

#### Concept of Do and Undo

In Lammps, a lot of commands have a declaration and removal command which should be called to declare an action with an ID and stop the action associated with the ID. The typical commands are:
 - `fix`, `unfix`
 - `compute`, `uncompute`
 - `group ID style ...`, `group ID delete`

LammpsInputBuilder maintain this logic by requiring all its type of objects to provide a *do* and *undo* command whenever relavant. The only exceptions to this rule are the `Instruction` objects which do not have an *undo* counter part. For example, the command `reset_timestep` simply sets the `step` counter to a new value, therfor it doesn't need to be stopped or undone, it is a simple one time action. 

#### Unrolling the TypedMolecule

The first step is to translate the `TypedMolecule` object. The data file is generated internally by ASE. The initial Lammps input script is based on a preconfigured template with the necessary adjustements to account for the type of potential used.

Dev note: This is a sufficient approach for now because LIB only supports ReaxFF and Airebo potentiel which only requires the Atom section in the Lammps data file. Other forcefield might require a different approach or backend.

Examples of Lammps files produced for a benzene with a reaxff potential. 

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

All the `Extension`, `FileIO`, and `Group` objects implement the function `addDoCommands()` and `addUndoCommands()` command to declare and stop respectively their actions. These funcions are responsible for converting from their respecting object to Lammps commands. The separation of *do* and *undo* allows other objects to be able to manipulate the scope or lifetime of these objects as necessary. 

Dev note on `ThermoIO`: The *thermo* keyword in Lammps works differently than the other `FileIO` objects. In particular, a *thermo* is always active and part of the `log.lammps` file. Therefor the `ThermoIO` doesn't have a scope per say. Instead, declaring a new `ThermoIO` object will override the previous IO settings and replace them with the new object settings. See [here](https://docs.lammps.org/thermo_style.html) for more information about thermo in Lammps. 

#### Unrolling the Instructions objects

Unlike the previous objects, the `Instruction` objects doesn't have a *undo* operation available to them. Consequently, they implement the function `writeInstruction()` to convert the object to Lammps commands. Because of this, `Instruction` objects as well do not have a notion of scope. They simply perform their task one time and the script will continue. 

#### Unrolling the Integrator objects

The `Integrator` objects are responsible for declaring the base process which is going to advance the step counter of the simulation. In most cases, that means in particular executing the Lammps `run` command in addition to the method to use for the time integration during that `run`. There are exceptions though such as the `minimize` command which technically doesn't use the `run` command but still involve some type of multistep process. 

The `Integrator` object implements up to three methods: `addDoCommands()`, `addUndoCommands()`, and `addRunCommands()`. The `addDoCommands()` and `addUndoCommands()` methods have the same as the other objects, i.e declare the necessary computation to perform and stop them respectively. The `addRunCommands()` is specific to the `Integrator` objects and is responsible for specifying how to trigger the computation. This is usually done by specify a `run` command. Note that an `Integrator` may only need to implement some of these methods.

#### Unrolling Section objects

A `Section` object represent a scope during which one or several computations or actions will be performed. Each object belonging to the `Section` object will be declared at the beginning of the `Section` and removed at the end of the `Section`.

A `Section` object is meant to be self-sufficient, as is it the object responsible for other objects. Consequently, a `Section` only need to implement the method `addAllCommands()`. This way, unrolling a list of `Section` object simply requires to call to method `addAllCommands()` in a sequence on all the `Section` objects.

There are several types of `Section` objects which all follow a similar logic to convert its object into Lammps commands. The simplest object is the `IntegratorSection` which hosts
a `Integrator` object and optionnal `Group`, `Instruction`, `Extension`, and `FileIO` objects. The lifetime of these objects are tied to the lifetime of the `Section` object.
It does so by calling the methods `addDoCommands()` and `addUndoCommands()` in the right order. 

The `IntegratorSection` unrolls in the following order:
* Do list of Groups
* Do list of Instructions
* Do list of Extensions
* Do Integrator
* Do list of FileIO
* Run Integrator
* Undo reverse list of FileIO
* Undo Integrator
* Undo reverse list of Extensions
* Undo reverse list of Groups

This order ensure that the commands are declared in the right order, and removed in the right order as well. The LIFO approach to *undo* guarantee that commands which may depend on each other are stopped cleanly.

Other `Section` objects follow a very similar pattern with the difference mainly being that the center piece of the `Section` may be a different object than an `Integrator`. For instance, the `RecursiveSection` has a list of `Section` objects to execute in the middle. Several examples are provided below to see how different `Section` types can be used in practice. 

### Handling of Units 

Many parameters of Lammps commands represent a quantity with unit such as temperature, length, etc. In Lammps, the unit system used is declared at the beginning of input script and is usually determined by which type of forcefield is used. 

This can be a challenge because commands parameters need to follow the unit system used. A major goal of LIB is to be able to make the definition of a workflow independant from the system definition unit. If the commands parameters are declared with only a simple value, a given workflow could only be used for potentials which are based on the same unit set.

To avoid this problem are make workflow definition agnostique of a given unit set, LIB wraps numerical parameters into `Quantity` objects representing different physical properties. A `Quantity` object represents a type of physical property, a numerical value, and a unit associated with it. A `Quantity` type exist for each type of units declared in Lammps (temperature, length, force, etc). A `Quantity` object can be converted to a new unit on demand. This is done by using [Pint](https://pint.readthedocs.io/en/stable/) in the backend.

When converting the workflow into Lammps commands, the `WorkflowBuilder` knows which unit style is used, and can therefor require to convert all the `Quantity` objects to the right units when writting commands. This mechanism ensures that a user can define a workflow ones, and change the potential at will without ever having to update its workflow because of improper units. 

## Workflow examples

### Minimize and NVE

TODO: Step by step description of the simpleNVE example.

### Scan of a surface with a tip

TODO: Step by step description of the scanSlab example.

