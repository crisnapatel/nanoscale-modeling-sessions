#!/usr/bin/env python3
"""Convert a LAMMPS molecular data file into a native molecule template.

The converter supports the common ``atom_style full``, ``molecular``, and
``charge`` layouts.  It copies coordinates, atom types, charges, and bonded
topology, remaps atom IDs to 1..N, unwraps coordinates when image flags and
box lengths are available, and centres the molecule around its centroid.

Force-field coefficients are intentionally not copied: a molecule template
describes one molecule's geometry and topology, while coefficients must
already exist in the LAMMPS system (for example from a preceding read_data).
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys


SECTION_NAMES = {
    "Masses",
    "Pair Coeffs",
    "PairIJ Coeffs",
    "Bond Coeffs",
    "Angle Coeffs",
    "Dihedral Coeffs",
    "Improper Coeffs",
    "Atom Type Labels",
    "Bond Type Labels",
    "Angle Type Labels",
    "Dihedral Type Labels",
    "Improper Type Labels",
    "Atoms",
    "Velocities",
    "Bonds",
    "Angles",
    "Dihedrals",
    "Impropers",
}

TOPOLOGY_WIDTH = {
    "Bonds": 2,
    "Angles": 3,
    "Dihedrals": 4,
    "Impropers": 4,
}


def clean(line: str) -> str:
    return line.split("#", 1)[0].strip()


def parse_file(path: Path) -> tuple[dict[str, list[list[str]]], dict[str, tuple[float, float]], str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    sections: dict[str, list[list[str]]] = {name: [] for name in SECTION_NAMES}
    bounds: dict[str, tuple[float, float]] = {}
    atom_style = ""
    current: str | None = None

    bound_re = re.compile(
        r"^\s*([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([xyz])lo\s+\3hi(?:\s|$)"
    )

    for raw in lines:
        match = bound_re.match(raw)
        if match:
            bounds[match.group(3)] = (float(match.group(1)), float(match.group(2)))

        section_key = clean(raw)
        if section_key in SECTION_NAMES:
            current = section_key
            if section_key == "Atoms" and "#" in raw:
                atom_style = raw.split("#", 1)[1].strip().split()[0].lower()
            continue

        content = clean(raw)
        if current and content:
            fields = content.split()
            if fields[0][0].isalpha():
                current = None
            else:
                sections[current].append(fields)

    if not sections["Atoms"]:
        raise ValueError("No Atoms section was found")
    return sections, bounds, atom_style


def parse_atoms(rows: list[list[str]], style: str, bounds: dict[str, tuple[float, float]]):
    atoms = {}
    for row in rows:
        if style == "full" or (not style and len(row) >= 7):
            atom_id, _mol_id, atom_type = map(int, row[:3])
            charge = float(row[3])
            xyz_start = 4
        elif style == "molecular":
            atom_id, _mol_id, atom_type = map(int, row[:3])
            charge = None
            xyz_start = 3
        elif style == "charge":
            atom_id, atom_type = map(int, row[:2])
            charge = float(row[2])
            xyz_start = 3
        else:
            raise ValueError(
                f"Unsupported or ambiguous atom style {style!r}; expected full, molecular, or charge"
            )

        x, y, z = map(float, row[xyz_start : xyz_start + 3])
        image = (0, 0, 0)
        if len(row) >= xyz_start + 6:
            image = tuple(map(int, row[xyz_start + 3 : xyz_start + 6]))

        coords = [x, y, z]
        for index, axis in enumerate("xyz"):
            if axis in bounds:
                lo, hi = bounds[axis]
                coords[index] += image[index] * (hi - lo)

        atoms[atom_id] = {
            "type": atom_type,
            "charge": charge,
            "coords": coords,
        }

    return atoms


def remap_topology(sections, id_map):
    topology = {}
    for section, width in TOPOLOGY_WIDTH.items():
        converted = []
        for row in sections[section]:
            old_id = int(row[0])
            interaction_type = int(row[1])
            old_atoms = list(map(int, row[2 : 2 + width]))
            converted.append((old_id, interaction_type, *(id_map[a] for a in old_atoms)))
        converted.sort()
        topology[section] = converted
    return topology


def topology_report(natoms: int, topology) -> str:
    lines = ["Topology analysis (conservative structural maxima):"]
    for section, width in TOPOLOGY_WIDTH.items():
        memberships = Counter()
        for row in topology[section]:
            memberships.update(row[2 : 2 + width])
        maximum = max(memberships.values(), default=0)
        lines.append(f"  {section.lower():11s}: {len(topology[section]):3d} total, {maximum:2d} involving one atom")

    graph = defaultdict(set)
    for row in topology["Bonds"]:
        atom1, atom2 = row[2:4]
        graph[atom1].add(atom2)
        graph[atom2].add(atom1)

    max_degree = max((len(graph[a]) for a in range(1, natoms + 1)), default=0)
    max_special = 0
    max_shells = (0, 0, 0)
    for start in range(1, natoms + 1):
        seen = {start}
        frontier = {start}
        shells = []
        special = set()
        for _distance in range(3):
            next_frontier = set()
            for atom in frontier:
                next_frontier.update(graph[atom])
            next_frontier.difference_update(seen)
            shells.append(len(next_frontier))
            special.update(next_frontier)
            seen.update(next_frontier)
            frontier = next_frontier
        if len(special) > max_special:
            max_special = len(special)
            max_shells = tuple(shells)

    lines.append(f"  maximum bond degree: {max_degree}")
    lines.append(
        "  maximum unique special neighbours within 1-2/1-3/1-4: "
        f"{max_special} (shells {max_shells[0]}/{max_shells[1]}/{max_shells[2]})"
    )
    #lines.append("These are transparent upper bounds, not necessarily LAMMPS's minimum internal storage values.")
    return "\n".join(lines)


def render_template(source: Path, atoms, topology) -> str:
    old_ids = sorted(atoms)
    id_map = {old_id: new_id for new_id, old_id in enumerate(old_ids, 1)}

    centred = {}
    centroid = [
        sum(atoms[old_id]["coords"][axis] for old_id in old_ids) / len(old_ids)
        for axis in range(3)
    ]
    for old_id in old_ids:
        centred[id_map[old_id]] = [
            atoms[old_id]["coords"][axis] - centroid[axis] for axis in range(3)
        ]

    out = [f"# Molecule template converted from {source.name}", ""]
    out.append(f"{len(old_ids)} atoms")
    for section in ("Bonds", "Angles", "Dihedrals", "Impropers"):
        if topology[section]:
            out.append(f"{len(topology[section])} {section.lower()}")

    out.extend(["", "Coords", ""])
    for atom_id in range(1, len(old_ids) + 1):
        x, y, z = centred[atom_id]
        out.append(f"{atom_id} {x:.8f} {y:.8f} {z:.8f}")

    out.extend(["", "Types", ""])
    for old_id in old_ids:
        out.append(f"{id_map[old_id]} {atoms[old_id]['type']}")

    if any(atoms[old_id]["charge"] is not None for old_id in old_ids):
        out.extend(["", "Charges", ""])
        for old_id in old_ids:
            charge = atoms[old_id]["charge"]
            out.append(f"{id_map[old_id]} {0.0 if charge is None else charge:.8f}")

    for section in ("Bonds", "Angles", "Dihedrals", "Impropers"):
        if not topology[section]:
            continue
        out.extend(["", section, ""])
        for new_interaction_id, row in enumerate(topology[section], 1):
            interaction_type = row[1]
            atom_ids = " ".join(str(value) for value in row[2:])
            out.append(f"{new_interaction_id} {interaction_type} {atom_ids}")

    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="LAMMPS data file")
    parser.add_argument("output", type=Path, help="native LAMMPS molecule-template file")
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    args = parser.parse_args()

    if args.output.exists() and not args.force:
        parser.error(f"output already exists: {args.output} (use --force to replace it)")

    sections, bounds, atom_style = parse_file(args.input)
    atoms = parse_atoms(sections["Atoms"], atom_style, bounds)
    old_ids = sorted(atoms)
    id_map = {old_id: new_id for new_id, old_id in enumerate(old_ids, 1)}
    topology = remap_topology(sections, id_map)

    args.output.write_text(render_template(args.input, atoms, topology), encoding="utf-8")
    print(f"Wrote {args.output} from {args.input}")
    print(topology_report(len(atoms), topology))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
