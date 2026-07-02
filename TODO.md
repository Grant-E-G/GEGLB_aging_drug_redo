# TODO

## Dataset Pulls

- [x] Keep raw data ignored by git but tracked locally through
  `data_sources/dataset_manifest.md`.
- [x] Pull and extract `all_drugbank_drugs.csv.zip` for local academic work. Do
  not commit the raw file.
- [0] Check CMap/CLUE size for `level5_beta_trt_cp_n720216x12328.gctx`:
  35,518,405,386 bytes (~33.1 GiB), so do not pull under the 10 GB rule. (We will pull this in the future.)
- [x] Pull `siginfo_beta.txt`: 465,242,319 bytes (~443.7 MiB).
- [ ] Do not pull `PPI_2022_distances.pkl` unless a size check confirms it is
  under 10 GB. It is an all-pairs shortest path artifact and should probably be
  regenerated or replaced by module-level BFS vectors.
- [ ] Pin exact OpenGenes download date if replacing the author-processed
  `Gene_hallmarks.csv` and `age-related-changes.tsv` with fresh OpenGenes data.
- [ ] Decide whether to use CMap BigQuery or a signature subset instead of the
  full 33.1 GiB GCTX file.
- [ ] Optional: pull CMap `instinfo_beta.txt` only if level 3/4 instance
  metadata becomes necessary. HEAD size check: 674,838,120 bytes (~643.6 MiB).

## Reproduction

- [ ] Confirm whether the proximity null randomizes drug targets only or both
  drug targets and hallmark modules.
- [ ] Implement a naive proximity oracle before vectorized optimization.
- [ ] Reproduce pAGE on the published result tables before changing the score.
- [ ] Record package versions from `BnayaGross/sharp-aging`.
- [ ] Compare local baseline counts with the paper and explain mismatches.
