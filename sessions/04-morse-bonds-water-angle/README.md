# Session 4 - Morse Bonds and a Water-Like Molecule in LAMMPS

This session continues from the two-atom harmonic bond example. We first replace the harmonic bond with a Morse potential and then extend the model to a three-atom water-like molecule containing two bonds and one angle.

The examples are deliberately small. Their purpose is to make molecular topology, bond styles, angle styles, trajectory output, and common LAMMPS errors easier to understand. The parameters are illustrative and do not define a chemically accurate water model.

## Video

This session has not yet been published. The other sessions are available in the [Nanoscale Modeling playlist](https://www.youtube.com/playlist?list=PLxvbTrJqiiJu_a_j9wmM4NOX0Nvc-erVi).

## Files

- `morse_bond.data` defines two atoms connected by one bond.
- `morse_bond.lmp` applies a Morse bond potential and writes a trajectory.
- `water_bonds_angles.data` defines one oxygen-like atom, two hydrogen-like atoms, two bonds, and one angle.
- `water_bonds_angles.lmp` applies harmonic bond and angle potentials and writes a trajectory.

Generated logs and trajectories are not included. They can be recreated from these input files.

## Morse Bond Example

Run:

```bash
lmp -in morse_bond.lmp
```

This writes `morse_bond.lammpstrj`. The atoms begin `1.6 angstrom` apart, while the equilibrium bond length is `1.2 angstrom`, so the Morse bond pulls them together.

The bond coefficients follow the LAMMPS Morse form:

```text
bond_coeff bond_type D alpha r0
```

Here, `D = 20.0 kcal/mol`, `alpha = 2.0 1/angstrom`, and `r0 = 1.2 angstrom`.

## Water-Like Molecule Example

Run:

```bash
lmp -in water_bonds_angles.lmp
```

This writes `water_bonds_angles.lammpstrj`. The starting bond lengths match their equilibrium value, but the starting H-O-H angle is larger than the equilibrium angle. The motion therefore makes the angle potential easy to see in OVITO.

For bonded systems, open the `.data` file in OVITO first and then load the trajectory so that the molecular topology is available alongside the changing coordinates.

## Main LAMMPS Ideas

```text
atom_style molecular
read_data
bond_style morse
bond_style harmonic
angle_style harmonic
bond_coeff
angle_coeff
fix nve
dump custom
```

The next session moves from one water-like molecule to a periodic box of bulk SPC/E water.
