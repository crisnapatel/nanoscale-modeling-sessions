# Session 5, Part 1. Preparing molecule templates

[Watch Part 1 on YouTube](https://youtu.be/bHsO5o7V8vA) · [Session 5 overview](../)

We draw a molecule in Avogadro, export it, get LigParGen data files, and convert those files to LAMMPS molecule templates. The final `pack-part1.lmp` is the unfinished input from this meeting, reconstructed from the saved session snapshot.

| File | What it contains |
| --- | --- |
| `FTOH.xyz` | Structure exported from Avogadro |
| `FTOH.smi` | Original SMILES export, including the disconnected `.F` fragment discussed during debugging |
| `FTOH.data`, `water.data` | Single-molecule data files downloaded from LigParGen |
| `FTOH.mol`, `water.mol` | Molecule templates made during the lesson |
| `lammps_data_to_mol.py` | Converter used during the lesson |
| `pack-part1.lmp` | End-of-Part-1 checkpoint |

To check the conversion from this directory:

```bash
python3 lammps_data_to_mol.py water.data water-check.mol
python3 lammps_data_to_mol.py FTOH.data FTOH-check.mol
diff -u water.mol water-check.mol
diff -u FTOH.mol FTOH-check.mol
```

The converter copies coordinates, atom types, charges, and bonded topology. It centres the coordinates and reports the maximum number of interactions involving an atom and the special neighbours within three bonds. These are conservative structural counts to help choose storage sizes, not guaranteed minimum values for every LAMMPS configuration. Masses and force-field coefficients remain in the data files, not in the templates.

Run the checkpoint with `lmp -in pack-part1.lmp`. It writes `water.tmp`, an empty box. Loading a molecule template registers it but does not insert atoms. The arbitrary masses in this checkpoint were used to get past a missing-mass error during the lesson.

The LigParGen `water.data` file includes its own angle coefficient and is not the SPC/E model discussed earlier in the series. Also check the FTOH structure against the intended molecule before using these parameters for research.
