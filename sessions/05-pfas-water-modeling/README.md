# Session 5. Preparing and packing PFAS molecules in LAMMPS

We split this session across two meetings. Start with Part 1 for the molecule files and template conversion, then continue with Part 2 for packing molecules and loading their masses and bonded coefficients.

| Part | What we did | Files | Video |
| --- | --- | --- | --- |
| 1 | Drew the molecule, used LigParGen, and converted data files to LAMMPS molecule templates | [Part 1 files](part-1/) | [Watch Part 1](https://youtu.be/bHsO5o7V8vA) |
| 2 | Inserted five FTOH-labelled molecules, checked overlaps, and loaded masses and bonded coefficients | [Part 2 files](part-2/) | [Watch Part 2](https://youtu.be/qzkvSmXXiFM) |

The discussion is mostly in English, with some Hindi.

We have not yet added water to the box or run molecular dynamics. The original SMILES export contains a disconnected fluorine fragment, so the 33-atom parameterised structure should be checked against the intended FTOH structure before using it for research. The LigParGen water file used in Part 1 is not an SPC/E model.
