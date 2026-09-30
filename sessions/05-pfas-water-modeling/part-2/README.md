# Session 5, Part 2. Packing FTOH-labelled molecules

[Watch Part 2 on YouTube](https://youtu.be/qzkvSmXXiFM) · [Session 5 overview](../)

We pick up from [Part 1](../part-1/). Here we put five copies of the molecule into the box, look at them in OVITO, and add the masses and bonded coefficients. I've included `FTOH.data` and `FTOH.mol` again so you can run this part from its own folder.

| File | What it contains |
| --- | --- |
| `pack.lmp` | Input at the end of Part 2 |
| `FTOH.data` | Original LigParGen data file used to extract masses and coefficients |
| `FTOH.mol` | Molecule template made in Part 1 and used for insertion |
| `mass/FTOH.mass` | Extracted mass commands |
| `coeffs/FTOH.*_coeffs` | Bond, angle, and dihedral coefficient commands |

From this folder, run `lmp -in pack.lmp`. Your LAMMPS build needs the interaction styles used in the input. The script puts five copies of the 33-atom molecule in the box, rejects placements where atoms are within 3 Å of each other, and writes `tmp.data`. You can open that file in OVITO with atom style `full`. If a molecule looks split across the box edge, unwrap the periodic images.

The first number in `create_box` means **atom types**, not atoms. In this LigParGen output, each atom happens to have its own type, so the number is 33. Five copies give us 165 atoms, but still only 33 atom types.

This is where we stopped. There is no water in the box yet, and we haven't added pair interactions or run MD. The original SMILES file has a separate `.F` fragment. Check that the 33-atom structure is the FTOH molecule you want before using it for research.
