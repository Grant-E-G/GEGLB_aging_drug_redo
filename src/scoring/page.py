"""pAGE-like ternary expression reversal scoring."""

from __future__ import annotations

from collections.abc import Iterable, Mapping


def ternary_direction(value: float, threshold: float = 0.0) -> int:
    if value > threshold:
        return 1
    if value < -threshold:
        return -1
    return 0


def page_score(
    age_directions: Mapping[str, int],
    drug_directions: Mapping[str, int],
    genes: Iterable[str] | None = None,
) -> int:
    selected_genes = genes if genes is not None else age_directions.keys()
    products = (
        age_directions.get(gene, 0) * drug_directions.get(gene, 0)
        for gene in selected_genes
    )
    return -sum(products)
