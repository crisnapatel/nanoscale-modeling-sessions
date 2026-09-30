# Session 5. Preparing and packing PFAS molecules in LAMMPS

We did Session 5 over two meetings. Part 1 covers the molecule files and the conversion to LAMMPS templates. In Part 2, we put five copies of the molecule in a box and add the masses and bonded coefficients.

| Part | What we did | Files | Video |
| --- | --- | --- | --- |
| 1 | Drew the molecule, used LigParGen, and converted data files to LAMMPS molecule templates | [Part 1 files](part-1/) | [Watch Part 1](https://youtu.be/bHsO5o7V8vA) |
| 2 | Inserted five FTOH-labelled molecules, checked overlaps, and loaded masses and bonded coefficients | [Part 2 files](part-2/) | [Watch Part 2](https://youtu.be/qzkvSmXXiFM) |

The discussion is mostly in English, with some Hindi.

We haven't added water to the box or run molecular dynamics yet. Also, the original SMILES export has a separate `.F` fragment. Please check that the 33-atom structure is the FTOH molecule you want before using these parameters for research. The water file from LigParGen is not an SPC/E model.
