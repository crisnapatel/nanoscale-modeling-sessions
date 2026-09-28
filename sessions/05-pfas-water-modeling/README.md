# Session 5. Preparing and packing PFAS molecules in LAMMPS

This session is split into parts. We start with the molecules drawn in Avogadro, get parameters from LigParGen, and work through the LAMMPS input slowly enough to understand the errors along the way.

## Videos

- [Part 1 on YouTube](https://www.youtube.com/watch?v=bHsO5o7V8vA) covers drawing the molecule, SMILES, LigParGen, and converting data files into molecule templates.
- Part 2 covers inserting five FTOH-labelled molecules, assigning masses, checking overlaps in OVITO, and loading bonded coefficients. Its video link will be added after upload.

The discussion is mostly in English, with some Hindi.

## Files

| File | What it contains |
| --- | --- |
| `FTOH.xyz` | The structure exported from Avogadro during Part 1 |
| `FTOH.smi` | The original SMILES export, including the disconnected `.F` fragment discussed during debugging |
| `FTOH.data`, `water.data` | The single-molecule data files downloaded from LigParGen |
| `FTOH.mol`, `water.mol` | The molecule templates made in Part 1 |
| `lammps_data_to_mol.py` | The converter used in the lesson |
| `pack-part1.lmp` | The unfinished input at the end of Part 1, reconstructed from the saved session snapshot |
| `pack.lmp` | The input at the end of Part 2 |
| `mass/FTOH.mass` | Mass commands extracted from the LigParGen data file |
| `coeffs/FTOH.*_coeffs` | Bond, angle, and dihedral coefficient commands created in Part 2 |

The downloaded files and Part 2 input are kept as they were used in the lesson. Logs, temporary data files, and duplicate copies of the downloaded data file are omitted.

## Repeating the template conversion

From this session directory, use new output names to compare the results with the included templates.

```bash
python3 lammps_data_to_mol.py water.data water-check.mol
python3 lammps_data_to_mol.py FTOH.data FTOH-check.mol
diff -u water.mol water-check.mol
diff -u FTOH.mol FTOH-check.mol
```

The converter copies coordinates, atom types, charges, and bonded topology. It centres the coordinates and reports the maximum number of interactions involving an atom and the special neighbours within three bonds. Those structural counts help us choose storage sizes. They are conservative counts, rather than a guarantee of the minimum storage required by every LAMMPS configuration.

Masses and force-field coefficients stay in the data file. They are not copied into these molecule templates.

## Running the lesson inputs

Use a LAMMPS build with the molecular interaction styles used here.

```bash
lmp -in pack-part1.lmp
lmp -in pack.lmp
```

`pack-part1.lmp` writes `water.tmp`, an empty box. Loading a template registers the molecule but does not insert any atoms. The arbitrary masses in this checkpoint were used to get past the missing-mass error in the lesson.

`pack.lmp` inserts five copies of the 33-atom template, checks for atom overlaps using a 3 Å distance, loads masses and bonded coefficients, and writes `tmp.data`. Open that file in OVITO with atom style `full`. Unwrap the periodic images if a molecule appears split across a box boundary.

The first number in `create_box` is the number of **atom types**, not the number of atoms to insert. In this LigParGen output each atom happens to have its own type, so both numbers are 33. Inserting five copies produces 165 atoms while keeping 33 atom types.

## Where we stopped

Part 2 reaches a box containing the five molecules with masses and bonded coefficients. Water has not yet been inserted. Pair interactions, electrostatics, equilibration, and molecular dynamics still need to be added.

The files also preserve issues worth checking before continuing. The original SMILES export contains a disconnected fluorine fragment, and the 33-atom parameterised structure should be checked against the intended FTOH structure before using it for research. The `water.data` file is the LigParGen output used in this lesson, including its supplied angle coefficient. It is not the SPC/E water model discussed earlier in the series.

FTOH is a small PFAS molecule. The broader project concerns PFAS, water, and polymer or clay surfaces, but these lessons have not yet built a polyethylene or polypropylene chain.
