# TODO

## Dataset Pulls

- [ ] Review DrugBank redistribution terms before pulling or committing
  `all_drugbank_drugs.csv.zip`. The file is small in the author repository
  (~5.7 MB), but the source is license-restricted.
- [ ] Check CMap/CLUE access terms and actual size for
  `level5_beta_trt_cp_n720216x12328.gctx`. The author README calls it very big;
  do not pull it if it is over 10 GB. Prefer a documented subset strategy if the
  full matrix is too large.
- [ ] Check whether `siginfo_beta.txt` can be downloaded without an account and
  whether it is under 10 GB. The author README says this file is very big and
  should be downloaded from CMap.
- [ ] Do not pull `PPI_2022_distances.pkl` unless a size check confirms it is
  under 10 GB. It is an all-pairs shortest path artifact and should probably be
  regenerated or replaced by module-level BFS vectors.
- [ ] Pin exact OpenGenes download date if replacing the author-processed
  `Gene_hallmarks.csv` and `age-related-changes.tsv` with fresh OpenGenes data.

## Reproduction

- [ ] Confirm whether the proximity null randomizes drug targets only or both
  drug targets and hallmark modules.
- [ ] Implement a naive proximity oracle before vectorized optimization.
- [ ] Reproduce pAGE on the published result tables before changing the score.
- [ ] Record package versions from `BnayaGross/sharp-aging`.
- [ ] Compare local baseline counts with the paper and explain mismatches.
