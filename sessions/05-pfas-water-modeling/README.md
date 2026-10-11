# Session 5. Preparing and packing PFAS molecules in LAMMPS

We did Session 5 over several meetings. Part 1 covers the molecule files and the conversion to LAMMPS templates. In Part 2, we put five copies of the molecule in a box and add the masses and bonded coefficients. In Part 3, we add water, set up the pair coefficients, and try energy minimisation.

| Part | What we did | Files | Video |
| --- | --- | --- | --- |
| 1 | Drew the molecule, used LigParGen, and converted data files to LAMMPS molecule templates | [Part 1 files](part-1/) | [Watch Part 1](https://youtu.be/bHsO5o7V8vA) |
| 2 | Inserted five FTOH-labelled molecules, checked overlaps, and loaded masses and bonded coefficients | [Part 2 files](part-2/) | [Watch Part 2](https://youtu.be/qzkvSmXXiFM) |
| 3 | Added water to the box and ran a first energy minimisation | [Part 3 files](part-3/) | [Watch Part 3](https://youtu.be/0399MqYNvnw) |

The discussion is mostly in English, with some Hindi.

We have added water, but have not run molecular dynamics yet. The original SMILES export has a separate `.F` fragment. Please check that the 33-atom structure is the FTOH molecule you want before using these parameters for research. The water file from LigParGen is not an SPC/E model. The Part 3 example uses Lennard-Jones interactions without electrostatics, so it is a teaching example, not a validated PFAS–water simulation.
