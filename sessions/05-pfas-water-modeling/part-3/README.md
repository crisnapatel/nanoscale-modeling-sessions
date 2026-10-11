# Session 5, Part 3. Adding water and trying energy minimisation

[Session 5 overview](../) · Video to follow

We started with the five FTOH-labelled molecules from [Part 2](../part-2/), added water molecules to the same periodic box, and then ran a first energy minimisation. These are the files we used in the meeting. The input and output data files are included so you can inspect the packed and minimised structures without rerunning everything.

| File | What it is |
| --- | --- |
| `pack.lmp` | Packs the FTOH-labelled molecules and water into a 40 Å box |
| `FTOH.mol`, `water.mol` | Molecule templates used by `pack.lmp` |
| `mass/`, `coeffs/` | Masses and bonded/Lennard-Jones coefficients loaded by `pack.lmp` |
| `polymer-water.data` | Packed structure used as the starting point for minimisation |
| `em.lmp` | Reads `polymer-water.data` and runs conjugate-gradient minimisation |
| `em.data` | Structure written by the minimisation run shown in the meeting |

From this folder, run `lmp -in pack.lmp`. That writes `tmp.data`; in the meeting I copied it to `polymer-water.data` before running `lmp -in em.lmp`. The included `polymer-water.data` is that starting structure. `em.lmp` writes `em.data` and an `em.trj` dump. The dump is large and is not included here.

The script requests 1,800 waters, but the overlap check only placed 1,194. Together with five 33-atom FTOH-labelled molecules, the packed data file has 3,747 atoms. The minimisation reduced the energy, but it stopped at the 1,000-iteration limit rather than meeting the requested tolerances; `em.data` should not be treated as a fully converged geometry.

This is a working-through-the-inputs example, not a production model. Although the molecule templates contain partial charges, `pair_style lj/cut` does not use them; there are no Coulomb or long-range electrostatic interactions in this run. The LigParGen water file is not SPC/E, and the original FTOH SMILES export has a separate `.F` fragment. Check the molecule identity and force-field choices before drawing any physical conclusions.
