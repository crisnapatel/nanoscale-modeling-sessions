# Session 5, Part 1. Preparing molecule templates

[Watch Part 1 on YouTube](https://youtu.be/bHsO5o7V8vA) · [Session 5 overview](../)

In this part we draw the molecule in Avogadro, send it to LigParGen, and turn the LAMMPS data files into molecule templates. There wasn't a saved input file at the end of Part 1, so `pack-part1.lmp` contains the commands we had reached by then.

| File | What it contains |
| --- | --- |
| `FTOH.xyz` | Structure exported from Avogadro |
| `FTOH.smi` | Original SMILES export, including the disconnected `.F` fragment discussed during debugging |
| `FTOH.data`, `water.data` | Single-molecule data files downloaded from LigParGen |
| `FTOH.mol`, `water.mol` | Molecule templates made during the lesson |
| `lammps_data_to_mol.py` | Converter used during the lesson |
| `pack-part1.lmp` | The commands we had reached by the end of Part 1 |

To check the conversion from this directory:

```bash
python3 lammps_data_to_mol.py water.data water-check.mol
python3 lammps_data_to_mol.py FTOH.data FTOH-check.mol
diff -u water.mol water-check.mol
diff -u FTOH.mol FTOH-check.mol
```

The converter copies coordinates, atom types, charges, and bonded connections, including impropers if there are any. It centres the coordinates and prints the largest number of bonded interactions and special neighbours around an atom. These counts help us choose the extra storage in LAMMPS, but they aren't necessarily the smallest values that will work. The masses and coefficients stay in the data files. They aren't copied into the molecule templates.

Run `lmp -in pack-part1.lmp` from this folder. It writes `water.tmp`, but the box is still empty. The `molecule` command loads a template; it doesn't put any atoms in the box. We used placeholder masses here to get past the missing-mass error.

The LigParGen `water.data` file has its own angle coefficient. It is not the SPC/E water model we discussed earlier. The original `FTOH.smi` file also has a separate `.F` fragment, so check the FTOH structure before using these parameters for research.
