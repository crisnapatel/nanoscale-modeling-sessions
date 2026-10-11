# Terminal commands from Part 3

[Watch the session](https://youtu.be/0399MqYNvnw) · [Back to Part 3](README.md)

I used the terminal to pull the 33 Lennard-Jones entries out of `FTOH.data` and turn them into commands that `pack.lmp` could include. Run these from the `part-3` folder. The intermediate files are included so you can compare each stage with your own output.

## Find and extract the Pair Coeffs section

```bash
grep -n '^Pair Coeffs$' FTOH.data
# 52:Pair Coeffs

grep -A 5 '^Pair Coeffs$' FTOH.data
# Show the heading and five lines after it, just to inspect the layout.

grep -A 34 '^Pair Coeffs$' FTOH.data | tail -n +3 > coeffs/FTOH.pair_coeffs
wc -l coeffs/FTOH.pair_coeffs
# 33: one entry for each FTOH atom type.
```

`grep -A 34` keeps the blank line plus 33 coefficient lines after the heading. `tail -n +3` removes the heading and blank line. These numbers fit **this** LigParGen file; check the heading and atom-type count again if your file differs.

Here is a `sed` way to inspect exactly the same 33 lines. We used `grep` and `tail` in the recording; this is an extra check, not another required processing step.

```bash
sed -n '54,86p' FTOH.data
```

## Turn data-file rows into LAMMPS commands

The extracted rows have three fields: `type epsilon sigma`. First, I added `pair_coeff` in front:

```bash
awk '{print "pair_coeff", $1, $2, $3}' coeffs/FTOH.pair_coeffs > coeffs/FTOH.pair
```

That was useful for seeing the columns, but it was **not yet a valid input command**. In an input script, `pair_coeff` needs both atom-type arguments, `I J`. For these diagonal coefficients, `J` is the same as `I`, so I printed the type number twice:

```bash
awk '{print $1, $2, $2, $3, $4}' coeffs/FTOH.pair > coeffs/FTOH.pair-extended
sed -n '1,3p' coeffs/FTOH.pair-extended
# pair_coeff 1 1 0.066 3.5000000
# pair_coeff 2 2 0.066 3.5000000
# pair_coeff 3 3 0.066 3.5000000
```

`pack.lmp` includes only `coeffs/FTOH.pair-extended`. The other two files show how we got there. A `Pair Coeffs` section inside a LAMMPS data file uses one type number per row, while a `pair_coeff` command in an input script uses two. [LAMMPS documents this distinction here](https://docs.lammps.org/pair_coeff.html).

Check the result before using it:

```bash
wc -l coeffs/FTOH.pair-extended
# 33
awk '$1 != "pair_coeff" || $2 != $3 {print "Check line", NR ":", $0}' coeffs/FTOH.pair-extended
# No output means every row starts with pair_coeff and uses the same I and J type.
```

The final file defines the diagonal LJ values. `pair_modify mix geometric` in `pack.lmp` generates the unlike-type values from them; it does not check whether that mixing rule is appropriate for the original force field. [LAMMPS mixing-rule reference](https://docs.lammps.org/pair_modify.html).
