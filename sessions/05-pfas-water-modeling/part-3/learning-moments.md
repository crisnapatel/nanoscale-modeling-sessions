# Learning moments from Part 3

[Watch the session](https://youtu.be/0399MqYNvnw) · [Back to Part 3](README.md)

These are the errors and checks that moved us forward in this meeting. The final inputs are in this folder; the errors below describe earlier versions as we worked through them.

## Water needs its own type numbers

The FTOH template uses atom types 1–33, bond types 1–32, and angle types 1–61. The water template starts its numbering again at 1. If we insert it without offsets, its types collide with the existing ones. In `pack.lmp`, `molecule water_mol water.mol offset 33 32 61 0 0` shifts water atom types to 34–36, bond types to 33–34, and its angle type to 62. Water has no dihedrals or impropers here. The five offsets are for **atom, bond, angle, dihedral, and improper types**, in that order. They do not renumber separate coefficient files; those files must use the shifted IDs too. [LAMMPS `molecule` reference](https://docs.lammps.org/molecule.html).

## “All bond coeffs are not set”

We had inserted water and reserved 34 bond types, but had not supplied coefficients for water bond types 33 and 34. The problem surfaced when `write_data` initialized the system. We made `coeffs/water.bond_coeffs`, changed the types from the original water file's 1 and 2 to 33 and 34, and included it in `pack.lmp`. Copying the original `water.data` numbers unchanged would silently target FTOH bond types 1 and 2 instead.

## “All angle coeffs are not set”

After the bond fix, LAMMPS reached the next missing term: water's angle type 62. The original water data file calls it type 1, but the angle offset is 61. We set `angle_coeff 62 62.500 82.120` in `coeffs/water.angle_coeffs` and included that file.

## “Not all per-type masses are set. Type 34 is missing”

The new atom types 34–36 also needed masses. The molecule template gives topology and charges, not the `mass` commands for these new types. We added `mass 34 15.999`, `mass 35 1.008`, and `mass 36 1.008` in `mass/water.mass`.

## “Must define bond_style before Bond Coeffs”

The packed data file already contains coefficient sections. Our first `em.lmp` tried to read it before declaring the interaction styles, so LAMMPS could not interpret the bond coefficients. We put `bond_style harmonic`, `angle_style harmonic`, `dihedral_style opls`, and the other required styles before `read_data polymer-water.data`. The rule is to define a style before LAMMPS reads coefficients for it. [LAMMPS `read_data` reference](https://docs.lammps.org/read_data.html).

## Pair coefficients: a data-file row is not an input command

The LigParGen `Pair Coeffs` section has rows like `1 0.066 3.5000000`. Including those rows directly gave `Unknown command`; adding only `pair_coeff` gave `Incorrect args for pair coefficients`. An input command needs `pair_coeff I J epsilon sigma`, so the diagonal entry becomes `pair_coeff 1 1 0.066 3.5000000`. We used `grep`, `tail`, and `awk` to make `coeffs/FTOH.pair-extended`; see [the commands](terminal-commands.md). Only that final file is included by `pack.lmp`. [LAMMPS `pair_coeff` reference](https://docs.lammps.org/pair_coeff.html).

## Requested waters versus inserted waters

`create_atoms` requested 1,800 water molecules, but the `overlap 2.5` check left room for only 1,194 within the allowed insertion attempts. This was not a crash. We checked the atom count in `polymer-water.data`: five 33-atom FTOH-labelled molecules plus 1,194 three-atom waters give 3,747 atoms. Relaxing the overlap distance, increasing the box, or raising `maxtry` can change the outcome, but each changes how the starting configuration is prepared. [LAMMPS `create_atoms` reference](https://docs.lammps.org/create_atoms.html).

## A written `em.data` file does not mean minimisation converged

The CG run did lower the energy and wrote `em.data`, but [`em.log`](em.log) says `Stopping criterion = max iterations`. It reached the 1,000-iteration cap; it did not meet the requested energy or force tolerance. The final largest force component was about 3.57 kcal/mol/Å. Before using a minimised structure, check the **stopping criterion and residual forces** in the log, not just whether an output file exists. [LAMMPS `minimize` reference](https://docs.lammps.org/minimize.html).

## A physics check that produced no LAMMPS error

Both molecule templates have partial charges, but `pair_style lj/cut 10.0` calculates Lennard-Jones interactions only. The run has **no Coulombic interaction** and no long-range solver. `pair_modify mix geometric` fills in unlike-type LJ coefficients; it cannot add electrostatics. The packed and minimised files are useful for learning the workflow, not for interpreting PFAS–water behaviour. The water parameters also came from LigParGen rather than an SPC/E setup, and the original FTOH SMILES export has a separate `.F` fragment. [LAMMPS `lj/cut` reference](https://docs.lammps.org/pair_lj.html).
