# GEGLB Aging Drug Reproduction

This repository is for reproducing and stress-testing SHARP, the network
medicine pipeline from Gross, Ehlert, Gladyshev, Loscalzo, and Barabasi,
"Network-driven discovery of repurposable drugs targeting hallmarks of aging."

The working question is:

> If we rebuild SHARP with explicit provenance, better statistical handling of
> perturbation data, tissue context, and validation, do the same drugs still look
> good?

## Coding Guidelines

- Write project code in Python.
- Prefer mostly functional modules: small pure functions, explicit inputs and
  outputs, and minimal shared state.
- Avoid heavy object construction unless profiling or API clarity justifies it.
- Keep code concentrated in a few coherent modules; do not fragment logic across
  many tiny files.
- Make data transformations auditable: every script should have clear source
  paths, output paths, and deterministic behavior.
- Treat correctness as the baseline. Optimize only after validating against a
  slow, clear reference implementation.
- Use standard library tools where sufficient; add dependencies only when they
  remove real complexity or are needed for performance/statistics.
- Format with `black` when available. The environment may not have it installed,
  so formatting should not be the only verification step.
- Keep clinical language conservative. This repo prioritizes computational
  hypotheses, not drug recommendations.

## Current Status

The original project outline is in `notes/Project_outline.md`. The repository
now has an initial Python scaffold, data/source manifests, and local ignored raw
data pulled from the public author repository where feasible.

Local raw data is intentionally ignored by git. Recreate it with:

```bash
python scripts/download_data.py
```

## Repository Layout

- `notes/`: project outline, research plan, reading notes, and logs.
- `docs/`: reproduction audit and method notes.
- `data/`: ignored local raw/interim/processed data plus tracked data docs.
- `data_sources/`: tracked manifests and data-source TODOs.
- `sources/`: bibliographic/source notes and ignored local PDFs.
- `scripts/`: reproducible command-line utilities.
- `src/`: Python implementation modules.
- `tests/`: focused tests for local scoring and parsing logic.
- `notebooks/`: eventual exploratory and reproduction notebooks.
- `results/`: tracked result summaries, not raw generated bulk output.
- `latex/`: manuscript or long-form writeup material.

## Pulled Sources And Data

Pulled locally but ignored by git:

- `sources/pdfs/2509.03330v1.pdf`, arXiv paper PDF.
- `data/raw/longevity_module/Gene_hallmarks.csv`.
- `data/raw/longevity_module/age-related-changes.tsv`.
- `data/raw/longevity_module/PPI_2022.csv`.
- `data/raw/longevity_module/PPI_STRING.csv.zip`.
- `data/raw/longevity_module/CMap_data/geneinfo_beta.txt`.
- `data/raw/longevity_module/CMap_data/compoundinfo_beta.txt`.
- `data/raw/longevity_module/CMap_data/siginfo_beta.txt`.
- `data/raw/longevity_module/CMap_data/LINCS2020_Release_Metadata_Field_Definitions.xlsx`.
- `data/raw/longevity_module/all_drugbank_drugs.csv.zip`.
- `data/raw/longevity_module/all_drugbank_drugs.csv`.
- `data/raw/longevity_module/results/*.csv`, published proximity and pAGE result
  tables from the author repository.

Not pulled yet:

- CMap Level 5 compound matrix. The public S3 HEAD reports 35,518,405,386 bytes
  (~33.1 GiB), so it is over the 10 GB pull cap.
- `PPI_2022_distances.pkl`, generated artifact described by the authors as too
  large for GitHub.

See `data_sources/dataset_manifest.md` and `TODO.md` for details.

## First Workflow

1. Recreate the raw data pull with `python scripts/download_data.py`.
2. Run `pytest` for the small local test suite.
3. Build the reproduction audit in `docs/repro_audit.md`.
4. Implement the naive SHARP baseline before optimizing proximity.
5. Validate any optimized proximity score against the naive oracle.

## Upstream References

- Paper/preprint: https://arxiv.org/abs/2509.03330
- Author data/scripts: https://github.com/BnayaGross/Longevity-module
- Author package: https://github.com/BnayaGross/sharp-aging
- OpenGenes downloads: https://open-genes.com/download
- CLUE/CMap data dashboard: https://clue.io/releases/data-dashboard
