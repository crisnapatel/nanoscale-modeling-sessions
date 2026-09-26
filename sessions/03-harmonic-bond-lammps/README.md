# Session 3 - Modeling a Harmonic Bond in LAMMPS

This session introduces bonded interactions through the smallest useful system: two atoms connected by one harmonic bond.

We first discuss what a force field means and compare the shape of harmonic and Morse bond potentials. We then build a molecular LAMMPS data file by hand, run the two-atom system in the NVE ensemble, and inspect its motion and forces in OVITO.

## Video

[Watch Session 3 on YouTube](https://www.youtube.com/watch?v=vEGduPf0NF8&list=PLxvbTrJqiiJu_a_j9wmM4NOX0Nvc-erVi), or open the [full Nanoscale Modeling playlist](https://www.youtube.com/playlist?list=PLxvbTrJqiiJu_a_j9wmM4NOX0Nvc-erVi).

## Files

- `two_atom_bond.data` contains the atoms, masses, simulation box, and bond connectivity.
- `harmonic_bond.lmp` reads the data file, assigns a harmonic bond model, runs the dynamics, and writes a trajectory.

Generated trajectory and log files are not included. They can be recreated by running the input.

## Run The Example

From this session directory:

```bash
lmp -in harmonic_bond.lmp
```

The run writes:

```text
harmonic_bond.lammpstrj
log.lammps
```

Open `harmonic_bond.lammpstrj` in OVITO. The atoms begin at a separation of `1.6 angstrom`, while the equilibrium bond length is `1.2 angstrom`. The stretched bond therefore pulls the atoms toward one another, converting potential energy into kinetic energy.

## Main LAMMPS Ideas

The data file describes the system:

```text
atoms and atom types
simulation box
masses
atom coordinates and molecule IDs
bond connectivity
```

The input file describes how that system evolves:

```text
atom_style molecular
read_data
bond_style harmonic
bond_coeff
fix nve
thermo_style
dump custom
run
```

This is a deliberately small model. Its purpose is to make the relationship between topology, potential energy, force, motion, and trajectory output easy to see.
