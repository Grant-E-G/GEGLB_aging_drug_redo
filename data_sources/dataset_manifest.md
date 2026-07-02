# Dataset Manifest

Local pull date: 2026-07-02

## Upstream Repositories

| Source | URL | Commit | Notes |
|---|---|---:|---|
| Author data/scripts | https://github.com/BnayaGross/Longevity-module | `69ff9e6f8c455b25e9947649cffe28dd77f358ae` | Public repository with processed data, scripts, demo, and published result tables. |
| Author package | https://github.com/BnayaGross/sharp-aging | `a4b18789e10535a779582048f1c9fa94348719c4` | Small MIT-licensed Python package. Not vendored here. |
| Paper PDF | https://arxiv.org/pdf/2509.03330 | arXiv v1 | Downloaded locally to `sources/pdfs/2509.03330v1.pdf`. |

## Pulled Local Files

These files are present under `data/raw/longevity_module/` but ignored by git.

| File | Size | SHA-256 | Source note |
|---|---:|---|---|
| `Gene_hallmarks.csv` | 592,780 | `b6ca38fd9ea5f8c28a203a37680175a20d5f04e8e288cc17b1926130835b5dde` | OpenGenes-derived processed hallmark memberships from author repo. |
| `age-related-changes.tsv` | 1,036,411 | `445dec75eead80b2986d0525f54c11b873568d25f0757c1dbf43244f049feaaa` | OpenGenes-derived age-expression direction table from author repo. |
| `PPI_2022.csv` | 15,171,581 | `7f8134a3e55803ec136267c0571376910bcfa84403bef8f06f556e4b417ba19d` | Processed human interactome from author repo. |
| `PPI_STRING.csv.zip` | 11,744,284 | `003aa9cca0d05df114b774e2c3907389861345d41a36e047514c005066e311f2` | STRING validation network from author repo. |
| `CMap_data/geneinfo_beta.txt` | 1,141,389 | `e739d06bad42ff9285c00b778e65d8999425062a3375cc7e7cdab0e7154490b5` | CMap LINCS 2020 gene metadata copied from author repo. |
| `CMap_data/compoundinfo_beta.txt` | 4,631,014 | `a71fca6de41dcc46a5063858be7e04155f3c09832c8b3fb35814f03db8d9fdff` | CMap LINCS 2020 compound metadata copied from author repo. |
| `CMap_data/LINCS2020_Release_Metadata_Field_Definitions.xlsx` | 40,461 | `15ab6e651de14334e632d90e140ba3060f157d94681e4e8b8c0f7db353e7115e` | CMap metadata definitions copied from author repo. |
| `CMap_data/README.txt` | 2,200 | `d6e9bbb485950550999f0c882bf9a5640ccb3028896219a4c8bd1849649b41d1` | CMap release notes copied from author repo. |
| `results/*.csv` | 11,393,415 total | see below | Published proximity and pAGE result tables copied from author repo. |

Additional local source:

| File | Size | SHA-256 | Source note |
|---|---:|---|---|
| `sources/pdfs/2509.03330v1.pdf` | 2,150,445 | `57162eebf080b643796ff97e072bc91241486ea5307fb10c0869f21024917fda` | arXiv PDF. |

Result table checksums:

| File | SHA-256 |
|---|---|
| `results/drug_evidence_Altered intercellular communication.csv` | `038042398b0a8ac816d3ca7d4dc33c878c829c91026837f08136e6fcb5be7e56` |
| `results/drug_evidence_Cell senescence.csv` | `528e1d0d53ee504d6d075621355491d9f1870dc96c16b2df2d267c694b065622` |
| `results/drug_evidence_Changes in the extracellular matrix structure.csv` | `4b87ac7d3ec505ccd009d45eeeed719a18699ca8f88a9496746cce162f89b7dd` |
| `results/drug_evidence_Deregulated nutrient sensing.csv` | `0cb60406fe8e8a4c9e60a54387bbcd8e6302279754fe3438fb52812bc2d46a25` |
| `results/drug_evidence_Disabled macroautophagy.csv` | `0b671408eef93397523ed89362254aae5ad243aed0a193acd6ed58a1271a0cda` |
| `results/drug_evidence_Epigenetic alterations.csv` | `22cf751eb3fed65a77818cb7f37daf9621403fccefbce4b1b65824b049cb0baa` |
| `results/drug_evidence_Exhaustion of stem cells.csv` | `ca4f8f76550ee0e8809c5f30a4d8634f99210c03697c355f3ae569b3e06c3f56` |
| `results/drug_evidence_Genomic instability.csv` | `124f27e9ca6172345045f0a7a89fde6591d119270958db001ed2692b7e3b1737` |
| `results/drug_evidence_Loss of proteostasis.csv` | `b8009c21a94e2c35e019a1f57fb4786b3827f647c4b6414185627fc0e69ca9e7` |
| `results/drug_evidence_Mitochondrial dysfunction.csv` | `57e43e40093f6183db09a8ed26a257d069fb66b6f213c5b4689e661389a767b9` |
| `results/drug_evidence_Telomere attrition.csv` | `a00ed6bd0009e34f15471933dbb681374a883d32df6105ae26260eded1e87229` |
| `results/drug_evidence_proximity_hallmarks.csv` | `e86109ca5448a13cd8fffc653359ea4ebf1eba62d36906fc4ff0fb3403789b79` |

## Not Pulled

| Dataset | Reason |
|---|---|
| `all_drugbank_drugs.csv.zip` | Small in the author repo, but DrugBank-derived. License review is required before copying into this workspace or redistributing. |
| `level5_beta_trt_cp_n720216x12328.gctx` | Not hosted in GitHub. CLUE/CMap access terms apply, and the author README calls it very big. Do not pull if over 10 GB. |
| `siginfo_beta.txt` | Not hosted in GitHub. CLUE/CMap access terms apply, and the author README calls it very big. Check size/access before pulling. |
| `PPI_2022_distances.pkl` | Not hosted in GitHub. Author README says it is very big. Prefer regenerating or replacing with module-level BFS vectors. |
