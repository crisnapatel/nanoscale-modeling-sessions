# Session 2 - Modeling Mindset and First Argon LAMMPS Run

In this session we first build a very small model ourselves: one particle whose position is randomly perturbed step by step. This gives a simple way to see the basic workflow behind a simulation:

```text
initial condition -> update rule -> trajectory -> visualization
```

After that, we move to LAMMPS and create a small Argon system using reduced Lennard-Jones units.

## Video

[Watch Session 2 on YouTube](https://www.youtube.com/watch?v=KTnfby1iwxw&list=PLxvbTrJqiiJu_a_j9wmM4NOX0Nvc-erVi), or open the [full Nanoscale Modeling playlist](https://www.youtube.com/playlist?list=PLxvbTrJqiiJu_a_j9wmM4NOX0Nvc-erVi).

## Files

- `brownian/one_particle_brownian_marimo.py`
  - Marimo notebook created during the session.
  - Prints one-particle XYZ-style frames to the notebook output.

- `lammps/01_create_argon_data.lmp`
  - Creates an FCC Argon system in LJ units.
  - Writes a LAMMPS data file named `Ar_1.data`.

- `lammps/02_run_argon_lj.lmp`
  - Creates the same Argon system.
  - Adds Lennard-Jones interactions, initial velocities, NVT dynamics, thermo output, and a dump trajectory.

Generated files are not included. Viewers can create the data file and trajectory by running the LAMMPS inputs themselves.

## Running The Brownian Example

From this session directory:

```bash
marimo edit brownian/one_particle_brownian_marimo.py
```

The notebook prints frames in a simple XYZ-style format:

```text
1
comment
I x y z
```

The important point here is the modeling idea: define the particle position, perturb it, and save the updated coordinates.

## Running The Argon Examples

Move into the LAMMPS directory:

```bash
cd lammps
```

Create the initial data file:

```bash
lmp -in 01_create_argon_data.lmp
```

This writes:

```text
Ar_1.data
```

You can open `Ar_1.data` in OVITO to inspect the simulation box and initial atom positions.

Run the Argon LJ dynamics:

```bash
lmp -in 02_run_argon_lj.lmp
```

This writes a trajectory:

```text
Ar.trj
```

Open `Ar.trj` in OVITO to see the atoms moving.

## Commands Introduced

LAMMPS commands used here:

```text
units
atom_style
dimension
boundary
lattice
region
create_box
create_atoms
mass
group
velocity
write_data
pair_style
pair_coeff
fix
thermo
dump
run
```

The next useful step is to slow down and read the interaction model carefully: what `lj/cut` means, what the three `pair_coeff` numbers mean, how forces are calculated, and how temperature and energy appear in the thermo output.
