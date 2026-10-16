# Session 5, Part 4. From energy minimisation to NVT

[Watch Part 4 on YouTube](https://youtu.be/DHhFY6wWZBI) · [Session 5 overview](../) · [Previous part](../part-3/)

We pick up from the packed PFAS-water box, look at the forces during minimisation, add electrostatics and OPLS 1-4 scaling, and start an NVT run. NPT and MSD are the next steps. We discuss them in the video, but do not run them in this part.

## Files

| File | What it contains |
| --- | --- |
| `polymer-water.data` | The same packed structure used in Part 3, with five 33-atom FTOH molecules and 1,194 waters |
| `em.lmp` | The LJ-only minimisation from the first half of the meeting, including the per-atom force magnitude |
| `em.data`, `em.log` | Structure and log from that LJ-only minimisation |
| `with_electrostatics/em.lmp` | Charged minimisation with PPPM, geometric LJ mixing, and OPLS special-bond weights |
| `with_electrostatics/em.data` | Charged structure written during the meeting, ready for the NVT input |
| `with_electrostatics/nvt.lmp` | Velocity initialisation and a 10 ps NVT run at a 300 K target |
| `with_electrostatics/nvt.data`, `with_electrostatics/nvt.log` | End-of-run structure, velocities, and the meeting's NVT log |
| [Learning moments](learning-moments.md) | Errors, checks, and corrections to keep in mind while following the video |
| [Terminal commands](terminal-commands.md) | Commands for running the examples and checking their outputs |
| [Verification](verification.md) | Checks run before sharing these files, separate from the meeting logs |

The starting box has 3,747 atoms and sides of 40 Å. Its density is about 0.6183 g/cm³. Minimisation and NVT keep that volume fixed. Neither stage brings it to an ambient-pressure liquid density.

## Run the examples

Use a working copy of this folder if you want to keep the supplied outputs. LAMMPS overwrites output files with the same names.

For the LJ-only minimisation, run from this folder:

```bash
mpirun -np 8 lmp -in em.lmp -log em-new.log
```

For the charged version:

```bash
cd with_electrostatics
mpirun -np 8 lmp -in em.lmp -log em-new.log
mpirun -np 8 lmp -in nvt.lmp -log nvt-new.log
```

You can skip the charged minimisation and start from the included `with_electrostatics/em.data`. `nvt.lmp` reads that file, creates velocities once, uses a 1 fs timestep, and runs 10,000 steps. It writes `nvt.data`, including velocities for a later stage. This is the short run from the meeting, not a claim that equilibration is complete.

Both inputs dump every five steps, as shown in the video. The trajectories can be hundreds of megabytes, so they are not included here. To make smaller files while practising, increase the dump interval. Keep frequent output if you want to inspect the early minimisation closely.

For OVITO, open the generated `em.trj` or `nvt.trj` and colour particles by `v_atom_fnorm`. The variable is the magnitude of each atom's force, not the global force norm printed in the minimisation summary.

## What changed between the two stages

The early LJ-only example has no electrostatics and uses the default special-bond weights. The charged example adds both Coulomb interactions and OPLS 1-4 scaling:

```lammps
pair_style lj/cut/coul/long 10.0
kspace_style pppm 1.0e-4
special_bonds lj/coul 0.0 0.0 0.5
pair_modify mix geometric
```

These are successive stages of building the input, not a controlled comparison where only electrostatics changes. We created a `without_electrostatics` folder during the meeting but had not added inputs to it. There is no separate LJ-only NVT result in this part.

## Limits of this example

The water parameters came from LigParGen. They are not SPC/E, and the water angle parameter is 82.120°. We have not validated this model for liquid-water properties or PFAS diffusion. No NPT or MSD result is supplied here. Do not use this short NVT run to claim an equilibrated liquid or a diffusion coefficient.

The LJ-only log stops with `linesearch alpha is zero`, with a final maximum force component of about 0.606 kcal/mol/Å. That does not establish that the requested force tolerance was reached. See the learning notes before interpreting the minimised structure.

## Notes on the supplied files

The charged inputs, data files, and NVT log are copied from the meeting folder. The original `log.lammps` is named `nvt.log` here so it does not get confused with the earlier minimisation log. The charged minimisation log had already been replaced by the NVT run, so it is not included.

While switching folders, I edited the top-level `em.lmp` as well as the charged copy. The top-level file left on disk had the incompatible `lj/cut/coul/cut`/PPPM combination. The runnable top-level `em.lmp` here follows the LJ-only commands printed in the saved `em.log`. The error and its fix are described in the learning notes. The meeting files on Ubuntu have not been changed.

The packed data file is byte-for-byte the same as Part 3. The old molecule templates and coefficient-preparation files are in [Part 3](../part-3/), rather than duplicated here. Recordings, trajectories, subtitles, and the longer practice runs are not part of this folder.
