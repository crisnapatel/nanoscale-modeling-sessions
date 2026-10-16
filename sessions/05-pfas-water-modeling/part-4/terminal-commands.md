# Terminal commands from Part 4

[Watch the meeting](https://youtu.be/DHhFY6wWZBI) · [Back to Part 4](README.md)

## Running LAMMPS with MPI

Around [05:14 in the video](https://youtu.be/DHhFY6wWZBI?t=314), we try different numbers of MPI processes:

```bash
lmp -in em.lmp
mpirun -np 2 lmp -in em.lmp
mpirun -np 4 lmp -in em.lmp
mpirun -np 8 lmp -in em.lmp
```

`mpirun` launches the processes. `-np 8` requests eight MPI ranks. `lmp` is the executable name on this machine, and `-in` tells LAMMPS which input file to read. Your installation may use a different executable name. `-i` is also accepted as an abbreviation of `-in`.

The log reports the MPI tasks, OpenMP threads, and loop time. The timings in the video are for this small system on one workstation. More ranks will not always make a calculation faster. Communication, output, and the amount of work per rank matter too. Setting `OMP_NUM_THREADS` alone does not turn ordinary pair styles into OpenMP-accelerated styles.

## Making the two branches

Around [26:32](https://youtu.be/DHhFY6wWZBI?t=1592), we create the folders and copy the input:

```bash
mkdir -p with_electrostatics without_electrostatics
cd with_electrostatics
cp ../em.lmp .
```

`..` means the parent directory. The final `.` means the current directory. After copying the input, we change the interaction settings for the charged branch. Copying alone does not make it a charged calculation.

Its `read_data ../polymer-water.data` path is relative to the directory where LAMMPS is launched. Run it from `with_electrostatics`, as shown in the README.

## Making the NVT input

Around [43:21](https://youtu.be/DHhFY6wWZBI?t=2601):

```bash
cp em.lmp nvt.lmp
```

Then we edit the copy. We read `em.data`, remove the minimisation commands, rename the dump/output files, initialise velocities, and add the timestep, `fix nvt`, and `run`. Do not run the copied file unchanged and assume it performs NVT.

## Useful checks while following along

These are quick checks for the reader, rather than extra commands we need to type during the video:

```bash
pwd
ls -lh
grep -n 'read_data' em.lmp nvt.lmp
grep -nE 'pair_style|kspace_style|special_bonds' em.lmp nvt.lmp
grep -A 7 'Minimization stats:' em.log
grep -E 'Loop time|MPI tasks|Total wall time|ERROR|WARNING' nvt.log
```

`pwd` is worth checking when a data file cannot be found or an edit seems to have no effect. The two inputs have the same name in different folders, so it is easy to edit one and run the other.

For the earlier `awk`, `grep`, `tail`, and `sed` coefficient-file exercises, see [Part 3's terminal commands](../part-3/terminal-commands.md).
