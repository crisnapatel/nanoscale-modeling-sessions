# Session 5. PFAS-water modelling in LAMMPS

We are doing Session 5 over several meetings. Part 1 covers the molecule files and the conversion to LAMMPS templates. In Part 2, we put five copies of the molecule in a box and add the masses and bonded coefficients. In Part 3, we add water, set up the pair coefficients, and try energy minimisation. Part 4 checks the forces, adds electrostatics and OPLS 1-4 scaling, and starts NVT dynamics.

| Part | What we did | Files | Video |
| --- | --- | --- | --- |
| 1 | Drew the molecule, used LigParGen, and converted data files to LAMMPS molecule templates | [Part 1 files](part-1/) | [Watch Part 1](https://youtu.be/bHsO5o7V8vA) |
| 2 | Inserted five FTOH-labelled molecules, checked overlaps, and loaded masses and bonded coefficients | [Part 2 files](part-2/) | [Watch Part 2](https://youtu.be/qzkvSmXXiFM) |
| 3 | Added water to the box and ran a first energy minimisation | [Part 3 files](part-3/) | [Watch Part 3](https://youtu.be/0399MqYNvnw) |
| 4 | Inspected minimisation forces, added electrostatics and OPLS 1-4 scaling, and started NVT | [Part 4 files](part-4/) | [Watch Part 4](https://youtu.be/DHhFY6wWZBI) |

The discussion is mostly in English, with some Hindi.

We have reached a short charged NVT run. NPT equilibration and MSD analysis are still to follow in the meetings. The water file from LigParGen is not an SPC/E model. Part 3 and the beginning of Part 4 use LJ interactions without electrostatics; the later Part 4 inputs add Coulomb interactions and the OPLS special-bond weights. These are teaching examples, not a validated PFAS-water model. Check the molecular structure and parameters before using them for research.
