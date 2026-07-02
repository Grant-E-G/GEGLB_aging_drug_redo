# Research Plan

## 1. Core Question

Can we reproduce SHARP and then replace fragile parts of the pipeline with more
statistically defensible alternatives while preserving interpretability?

## 2. Baseline Thesis

The original SHARP pipeline should be treated as a clean baseline:

- network proximity identifies drugs whose targets are close to aging hallmark
  modules;
- pAGE asks whether drug-induced expression opposes age-associated expression;
- the combined score produces interpretable drug-hallmark hypotheses.

## 3. First Deliverable

A documented reproduction audit:

- exact upstream commits and source files;
- local data manifest with checksums;
- runnable Python loader/scoring scaffolds;
- clear list of blocked data pulls;
- first-pass comparison against the paper's headline counts.

## 4. Data Objects

- hallmark gene memberships from `Gene_hallmarks.csv`;
- age-related expression directions from `age-related-changes.tsv`;
- interactome edges from `PPI_2022.csv`;
- validation network from `PPI_STRING.csv.zip`;
- CMap metadata from `CMap_data/*`;
- published proximity/pAGE result tables from `results/*.csv`;
- later: full CMap Level 5 matrix or a documented subset.

## 5. Baseline Implementation

Implement in this order:

1. data loaders;
2. pAGE scorer;
3. proximity oracle;
4. optimized proximity implementation validated against the oracle;
5. reproduction summary tables.

## 6. Risks And Unknowns

- DrugBank-derived files require license review.
- CMap files may require account access and may exceed the 10 GB local pull cap.
- OpenGenes-derived processed files need a pinned upstream date if replaced with
  fresh downloads.
- Validation labels are small and may overlap with source literature used to
  build OpenGenes.

## 7. Near-Term Checks

- [ ] Run `python scripts/download_data.py` from a clean checkout.
- [ ] Run `pytest`.
- [ ] Count hallmark genes by confidence level.
- [ ] Count age-direction genes and inspect duplicate/conflicting directions.
- [ ] Confirm pAGE sign convention against the author notebook.
