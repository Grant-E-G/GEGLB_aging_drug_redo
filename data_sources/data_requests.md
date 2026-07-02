# Data Requests And Storage Plan

All raw data should stay out of git. The repository tracks local data by
manifest, checksums, source URLs, and download scripts.

Local raw data currently lives under `data/raw/` and is ignored by `.gitignore`.

## Current Local Footprint

| Group | Local path | Approximate size | Status |
|---|---|---:|---|
| Author processed SHARP inputs | `data/raw/longevity_module/` | 537 MiB | Pulled locally, ignored by git. |
| Paper PDF | `sources/pdfs/2509.03330v1.pdf` | 2.1 MiB | Pulled locally, ignored by git. |

The working filesystem had about 115 GiB free when checked on 2026-07-02.

## Required For First Reproduction

| Dataset | Size | Status | Notes |
|---|---:|---|---|
| `Gene_hallmarks.csv` | 592,780 bytes | Pulled | OpenGenes-derived hallmark mapping from author repo. |
| `age-related-changes.tsv` | 1,036,411 bytes | Pulled | OpenGenes-derived categorical age-expression annotations. |
| `PPI_2022.csv` | 15,171,581 bytes | Pulled | Main interactome. |
| `PPI_STRING.csv.zip` | 11,744,284 bytes | Pulled | STRING validation network. |
| `all_drugbank_drugs.csv.zip` | 5,955,750 bytes | Pulled | DrugBank-derived author file; local academic use only, do not commit. |
| `all_drugbank_drugs.csv` | 44,642,727 bytes | Pulled/extracted | Local extraction for author script compatibility. |
| `siginfo_beta.txt` | 465,242,319 bytes | Pulled | Required by the author pAGE notebook. |
| `geneinfo_beta.txt` | 1,141,389 bytes | Pulled | Required for CMap gene mapping. |
| `compoundinfo_beta.txt` | 4,631,014 bytes | Pulled | Required for CMap compound mapping. |
| Published proximity/pAGE CSVs | 11,393,415 bytes total | Pulled | Useful for comparison before recomputing everything. |

## Too Large Under Current Rule

| Dataset | Remote size | Decision | Source |
|---|---:|---|---|
| `level5_beta_trt_cp_n720216x12328.gctx` | 35,518,405,386 bytes (~33.1 GiB) | Do not pull under the 10 GB cap. | `https://s3.amazonaws.com/macchiato.clue.io/builds/LINCS2020/level5/level5_beta_trt_cp_n720216x12328.gctx` |

The GCTX file is needed to recompute pAGE directly from CMap expression values.
Until disk policy changes, use the author result tables for audit work and plan
either a subset extraction, CMap BigQuery query, or a one-time local pull outside
the repository if enough disk is available.

## Optional Or Deferred

| Dataset | Size/status | Decision |
|---|---|---|
| `instinfo_beta.txt` | 674,838,120 bytes (~643.6 MiB), remote HEAD checked | Not needed for Level 5 pAGE reproduction yet; pull only if level 3/4 instance metadata becomes useful. |
| `PPI_2022_distances.pkl` | Unknown; generated and omitted by authors as very large | Do not pull. Prefer module-level BFS vectors or regenerate only with an explicit storage estimate. |
| Fresh OpenGenes download | Unknown current size | Deferred. Current reproduction should use author-processed OpenGenes files first. |
| Tissue-specific aging expression datasets | Unknown | Phase 5. Add one dataset at a time after size/license checks. |

## Suggested Next Data Work

1. Decide whether the 33.1 GiB CMap GCTX can live outside git under
   `data/raw/longevity_module/CMap_data/`.
2. If not, write a CMap subset plan keyed by drugs with DrugBank targets and
   signatures present in `siginfo_beta.txt`.
3. Estimate the storage cost of `PPI_2022_distances.pkl` before generating it.
   A dense all-pairs distance matrix over the interactome is probably wasteful
   for this project.
4. Keep all downloaded/generated data ignored; update
   `data_sources/dataset_manifest.md` after every pull.
