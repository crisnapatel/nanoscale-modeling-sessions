# Checks before sharing the Part 4 files

Checked on 16 October 2026 with LAMMPS 22 Jul 2025, Update 4, on the Ubuntu workstation.

| Input or check | Result |
| --- | --- |
| Top-level LJ-only `em.lmp` | Minimisation finished without a LAMMPS error |
| `with_electrostatics/em.lmp` | Charged minimisation finished without a LAMMPS error |
| `with_electrostatics/nvt.lmp` | All 10,000 steps finished without a LAMMPS error |
| `lj/cut/coul/cut` with PPPM | Reproduced `ERROR: KSpace style is incompatible with Pair style` |
| `thermo_style step pe ke ecoul evdwl density` | Reproduced `ERROR: Illegal thermo style step` |
| Packed `polymer-water.data` | SHA-256 matches the Part 3 file exactly |

The successful runs used eight MPI ranks and one OpenMP thread per rank. Tests ran in a separate working folder. Only the dump commands were removed from the test copies to avoid writing large trajectories. The timestep, force-field settings, minimisation limits, velocity seed, thermostat, and NVT run length were unchanged. The supplied meeting outputs were not replaced with these test outputs, and the original Ubuntu meeting folder was not modified.

These are checks that the inputs run. They do not establish force convergence, equilibration, timestep convergence, or the physical accuracy of the water model. The [learning notes](learning-moments.md) explain those limitations.
