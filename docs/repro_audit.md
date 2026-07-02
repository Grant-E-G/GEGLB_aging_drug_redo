# Reproduction Audit

Audit date: 2026-07-02

## Source Review

The project outline targets a reproduction of SHARP from:

- Gross, Ehlert, Gladyshev, Loscalzo, and Barabasi,
  "Network-driven discovery of repurposable drugs targeting hallmarks of aging,"
  arXiv:2509.03330.
- Author data/scripts repository:
  https://github.com/BnayaGross/Longevity-module
- Author Python package:
  https://github.com/BnayaGross/sharp-aging

The author repository README says it contains the processed PPI network,
OpenGenes-derived hallmark memberships, OpenGenes-derived age-related expression
changes, DrugBank-derived target mappings, CMap metadata, and published
proximity/pAGE result tables. It also says the all-pairs PPI distance pickle and
the full CMap Level 5 matrix are too large for GitHub.

## Local Pull

Pulled locally and ignored by git:

- arXiv PDF, 2.1 MB.
- OpenGenes-derived `Gene_hallmarks.csv`.
- OpenGenes-derived `age-related-changes.tsv`.
- `PPI_2022.csv`.
- `PPI_STRING.csv.zip`.
- CMap LINCS metadata files that are present in the author repo.
- Published proximity and pAGE result tables.

See `data_sources/dataset_manifest.md` for paths, sizes, checksums, and skipped
datasets.

## Immediate Findings

- The top-level README was still a generic theory template; it now reflects the
  SHARP reproduction project.
- The current repository did not have the project structure proposed in the
  outline; initial `data/`, `docs/`, `scripts/`, `src/`, `tests/`, `notebooks/`,
  and `results/` directories are now present.
- The full CMap expression matrix is not currently pulled because it would
  require either lifting the 10 GB pull cap or using a subset strategy. The GCTX
  is 35,518,405,386 bytes (~33.1 GiB).
- DrugBank-derived targets are now pulled locally for academic work but remain
  ignored by git.
- The most important unresolved methodological question is still the proximity
  null: whether the authors randomize only drug targets, or both drug targets and
  hallmark modules.

## First Local Counts

Using the initial stdlib loaders on the pulled raw files:

| Quantity | Count | Note |
|---|---:|---|
| Hallmark groups | 11 | Excludes the `other` OpenGenes group. |
| Hallmark gene assignments | 1,798 | Sum across hallmark groups, so duplicate genes across groups may count more than once. |
| Age-direction genes | 2,112 | Genes with at least one increased/decreased age-expression annotation. |
| `PPI_2022.csv` edges | 531,597 | Raw rows after requiring both HGNC endpoint fields. |

These are loader sanity checks, not final reproduction counts. The paper target
counts should be reproduced with the exact confidence-level and de-duplication
rules from the author code.

## Next Reproduction Steps

1. Inspect `Drug_proximity.py`, `NetworkMetrics.py`, and `pAGE.ipynb` from the
   author repository for the exact pAGE and proximity logic.
2. Reproduce headline counts from the local raw files:
   longevity genes, hallmark genes, age-direction genes, drugs, proximal drugs,
   and pAGE-positive candidates.
3. Implement the naive proximity oracle before any vectorized version.
4. Confirm pAGE sign convention against the paper and author notebook.
5. Document every mismatch against the paper in
   `results/baseline_reproduction_summary.md`.
