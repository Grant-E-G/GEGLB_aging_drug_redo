"""Small data-loading helpers for author-processed SHARP files."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Iterable


def read_table(path: str | Path, delimiter: str | None = None) -> list[dict[str, str]]:
    table_path = Path(path)
    selected_delimiter = delimiter or ("\t" if table_path.suffix == ".tsv" else ",")
    with table_path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter=selected_delimiter))


def clean_gene(value: str | None) -> str:
    return (value or "").strip()


def parse_int(value: str | None, default: int = 0) -> int:
    try:
        return int(float((value or "").strip()))
    except ValueError:
        return default


def load_hallmark_genes(
    path: str | Path,
    min_confidence: int = 1,
    include_other: bool = False,
) -> dict[str, set[str]]:
    rows = read_table(path)
    grouped: dict[str, set[str]] = defaultdict(set)

    for row in rows:
        confidence = parse_int(row.get("confidence"))
        hallmark = (row.get("aging_mechanisms_group") or "").strip()
        gene = clean_gene(row.get("GeneId"))
        if not gene or confidence < min_confidence:
            continue
        if hallmark == "other" and not include_other:
            continue
        grouped[hallmark].add(gene)

    return dict(grouped)


def load_interactome_edges(path: str | Path) -> list[tuple[str, str]]:
    rows = read_table(path)
    edges = [
        (clean_gene(row.get("HGNC_Symbol.1")), clean_gene(row.get("HGNC_Symbol.2")))
        for row in rows
    ]
    return [(source, target) for source, target in edges if source and target]


def age_direction(change_type: str | None) -> int:
    normalized = (change_type or "").strip().lower()
    if "increased" in normalized:
        return 1
    if "decreased" in normalized:
        return -1
    return 0


def load_age_directions(path: str | Path) -> dict[str, set[int]]:
    rows = read_table(path, delimiter="\t")
    directions: dict[str, set[int]] = defaultdict(set)

    for row in rows:
        gene = clean_gene(row.get("HGNC"))
        direction = age_direction(row.get("change type"))
        if gene and direction:
            directions[gene].add(direction)

    return dict(directions)


def unique_genes(gene_sets: Iterable[Iterable[str]]) -> set[str]:
    return {gene for genes in gene_sets for gene in genes}
