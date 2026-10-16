# Learning moments from Part 4

[Watch the meeting](https://youtu.be/DHhFY6wWZBI) · [Back to Part 4](README.md)

The inputs here are the versions to run. The broken commands below explain the mistakes we worked through. Error text was checked with LAMMPS 22 Jul 2025, Update 4. Source-file locations can differ between builds.

## Per-atom force magnitude is not the global force norm

[03:20](https://youtu.be/DHhFY6wWZBI?t=200)

The trajectory has `fx`, `fy`, and `fz`, but I want one value to colour each atom by. We add:

```lammps
variable atom_fnorm atom sqrt(fx^2+fy^2+fz^2)
dump em_trj all custom 5 em.trj id mol type x y z vx vy vz fx fy fz v_atom_fnorm
```

`atom` makes this a per-atom variable. `v_atom_fnorm` includes its values in the dump. In OVITO, we can then colour by that property. This is different from the global force two-norm in the minimisation summary, which combines force components across the whole system. The maximum single force component is also not the same as the maximum per-atom magnitude.

[LAMMPS variable reference](https://docs.lammps.org/variable.html)

## A minimisation can stop without reaching the requested tolerance

[10:05](https://youtu.be/DHhFY6wWZBI?t=605)

The first run stops at the iteration limit. We increase the limit from 1,000 to 10,000 and read the summary again. The saved LJ-only `em.log` reports:

```text
Stopping criterion = linesearch alpha is zero
Force two-norm initial, final = 4652.8913 1.8764638
Force max component initial, final = 148.08972 0.60598389
Iterations, force evaluations = 7874 15794
```

The forces have fallen substantially, but they are not at the requested `1.0e-8` tolerance. A zero line-search step means CG could not make further progress along its search direction at that point. It is not another way of saying the force tolerance was met. Writing `em.data`, lowering the energy, or obtaining a negative potential energy does not by itself prove convergence or physical stability.

[LAMMPS minimisation reference](https://docs.lammps.org/minimize.html)

## ERROR: Illegal thermo style step

[16:26](https://youtu.be/DHhFY6wWZBI?t=986)

We try to list quantities directly after `thermo_style`:

```lammps
thermo_style step pe ke ecoul evdwl density
```

LAMMPS interprets `step` as the name of a thermo style. For a list of output quantities, the style is `custom`:

```lammps
thermo 100
thermo_style custom step pe ke ecoul evdwl density
```

`thermo 100` sets the output interval. `thermo_style custom ...` chooses what is printed. The error text above was reproduced with this broken command because the meeting log was later overwritten.

[LAMMPS thermo_style reference](https://docs.lammps.org/thermo_style.html)

## Charges in a data file do not switch on electrostatics

[17:40](https://youtu.be/DHhFY6wWZBI?t=1060)

The packed file contains partial charges, but the early input uses `pair_style lj/cut 10.0`. That style calculates LJ interactions, not Coulomb forces. The zero `ecoul` output is a useful clue. We need an interaction style that actually uses the charges.

For the charged calculation we use:

```lammps
pair_style lj/cut/coul/long 10.0
kspace_style pppm 1.0e-4
```

The screened direct-space Coulomb term and PPPM work together. My explanation in the video is loose when I describe PPPM as simply handling the atoms beyond 10 Å. The reciprocal-space contribution is not restricted to a separate group of distant atoms. To inspect the Coulomb energy, print both `ecoul` and `elong`; `ecoul` alone is not the full electrostatic contribution.

```lammps
thermo_style custom step temp pe ke evdwl ecoul elong density
```

That last line is an optional improvement for checking the output, not a line added to the saved meeting inputs.

[LAMMPS LJ/Coulomb reference](https://docs.lammps.org/pair_lj_cut_coul.html)

## OPLS has rules for nonbonded neighbours within a molecule

[31:48](https://youtu.be/DHhFY6wWZBI?t=1908)

For a bonded chain A-B-C-D, A-B is a 1-2 pair, A-C a 1-3 pair, and A-D a 1-4 pair. These are distances along the bond graph, not atom-type numbers. We add:

```lammps
special_bonds lj/coul 0.0 0.0 0.5
pair_modify mix geometric
```

The OPLS convention excludes the 1-2 and 1-3 LJ/Coulomb contributions and halves the 1-4 terms. Other ordinary nonbonded pairs retain full weight, subject to the rest of the interaction setup. `dihedral_style opls` does not set those weights or the mixing rule for us.

When I say these interactions are already included in the bonded constants, take that as a rough explanation of a consistent parameterisation. The harmonic bond function does not literally contain the omitted LJ and Coulomb functions. We need the conventions used to parameterise the force field, rather than adding or removing terms independently.

The early LJ-only run and the later charged run differ in both electrostatics and these special-bond weights. Comparing them would not isolate the effect of charges alone.

[LAMMPS special_bonds reference](https://docs.lammps.org/special_bonds.html)

## ERROR: KSpace style is incompatible with Pair style

[41:34](https://youtu.be/DHhFY6wWZBI?t=2494)

The first attempt combines:

```lammps
pair_style lj/cut/coul/cut 10.0
kspace_style pppm 1.0e-4
```

The `coul/cut` style truncates Coulomb interactions. It is not the matching screened real-space part for PPPM. We change it to:

```lammps
pair_style lj/cut/coul/long 10.0
kspace_style pppm 1.0e-4
```

This pair-style/KSpace combination is the one used in the charged inputs. The exact error was reproduced from the incompatible combination left in the top-level file after the meeting.

[LAMMPS LJ/Coulomb styles](https://docs.lammps.org/pair_lj_cut_coul.html)

## Check the working directory and the file you edited

[40:44](https://youtu.be/DHhFY6wWZBI?t=2444)

There are two `em.lmp` files by this point. An edit in the parent folder does not change the copy in `with_electrostatics`. Also, a relative `read_data` path is interpreted from the working directory where LAMMPS is launched. Check `pwd`, the input filename, and its `read_data` line before changing more physics settings.

## Why does velocity creation take a temperature in kelvin?

[47:15](https://youtu.be/DHhFY6wWZBI?t=2835)

```lammps
velocity all create 300.0 84754 rot yes mom yes dist gaussian
```

The velocity is not measured in kelvin. LAMMPS draws velocities and scales them so that the kinetic temperature is 300 K. The integer is the random seed. `mom yes` and `rot yes` remove the system's net linear and angular momentum at initialisation. They do not freeze every molecule's translation or rotation.

Create velocities for the start of dynamics, then carry them forward rather than drawing a new set at every stage.

## NVT integrates motion as well as applying the thermostat

[48:23](https://youtu.be/DHhFY6wWZBI?t=2903)

```lammps
timestep 1
fix alok_nvt all nvt temp 300.0 300.0 100.0
run 10000
```

In `units real`, the timestep is in fs. This is a 10 ps run. `fix nvt` advances the dynamics with a Nose-Hoover thermostat, so we do not add a second `fix nve` on the same atoms. The damping argument is 100 fs here, not a command to reset the temperature every 100 steps. At this particular 1 fs timestep, 100 fs happens to equal 100 steps. If we change the timestep, that numerical coincidence no longer holds.

NVT keeps the volume fixed, so density stays at about 0.6183 g/cm³. That does not demonstrate equilibration. The meeting's thermo output does not include `temp`, `press`, or `elong`, so add those when checking temperature, pressure, and the complete Coulomb contribution in later practice.

[LAMMPS NVT/NPT reference](https://docs.lammps.org/fix_nh.html)
