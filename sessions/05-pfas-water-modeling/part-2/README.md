# Session 5, Part 2. Packing FTOH-labelled molecules

[Watch Part 2 on YouTube](https://youtu.be/qzkvSmXXiFM) · [Session 5 overview](../)

We continue from [Part 1](../part-1/), insert five molecule copies, inspect them in OVITO, and load masses and bonded coefficients from the LigParGen data. `FTOH.data` and `FTOH.mol` are repeated here so this input runs from its own directory.

| File | What it contains |
| --- | --- |
| `pack.lmp` | Input at the end of Part 2 |
| `FTOH.data` | Original LigParGen data file used to extract masses and coefficients |
| `FTOH.mol` | Molecule template made in Part 1 and used for insertion |
| `mass/FTOH.mass` | Extracted mass commands |
| `coeffs/FTOH.*_coeffs` | Bond, angle, and dihedral coefficient commands |

From this directory, run `lmp -in pack.lmp` with a LAMMPS build that has the interaction styles in the input. It creates five copies of the 33-atom template, checks for overlaps at a 3 Å distance, and writes `tmp.data`. Open that file in OVITO with atom style `full`. Unwrap periodic images if a molecule appears split across a box boundary.

The first number in `create_box` is the number of atom types, not the number of atoms to insert. Each atom in this LigParGen output happens to have its own type, so both numbers are 33. Five copies produce 165 atoms but still only 33 atom types.

This is where the meeting stopped. Water, pair interactions, electrostatics, equilibration, and molecular dynamics have not been added. The original SMILES export has a disconnected fluorine fragment, so verify that the 33-atom structure represents the intended FTOH molecule before using it for research.
