# Rebuilding SHARP for Aging Drug Repurposing

This repo is a guided attempt to reproduce and improve the methodology from:

> Gross, Ehlert, Gladyshev, Loscalzo, and Barabási, "Network-driven discovery of repurposable drugs targeting hallmarks of aging," *Nature Aging*, 2026. Preprint: arXiv:2509.03330.

The paper introduces **SHARP** (Systematic Hallmark-based Aging Repurposing Pipeline), a network-medicine method for finding repurposable drugs that may target hallmarks of aging. It maps 2,358 longevity-associated genes onto the human interactome, shows that the genes for each hallmark form a connected subgraph (a "hallmark module"), scores the network proximity of 6,442 approved/experimental compounds to each module, and then applies a transcription-based directionality metric, **pAGE** (Pro-Age), that asks whether a drug's induced expression shifts reinforce or counteract known age-related expression changes. By convention, pAGE > 0 is pro-longevity and pAGE < 0 is age-accelerating.

The paper is useful and interpretable, but the methodology is intentionally simple. This project asks a sharper question:

> Can we reproduce the published pipeline and then build a better, more statistically defensible version without losing interpretability?

## Status

This is a planning README, not yet a working implementation.

Before starting serious coding, this plan should be reviewed by at least one third party with bioinformatics, network medicine, or computational biology experience.

## Why This Is Worth Doing

The paper is a good hypothesis generator, but it leaves obvious room for improvement.

The core limitations to address are:

- pAGE encodes expression direction as ternary (up / down / not-regulated) and sums it, discarding effect size and replicate uncertainty.
- Critically, pAGE is ternary in part *because its age-side input is categorical*. The age-related expression changes come from OpenGenes (`age-related-changes.tsv`), which are curated up/down annotations, not a quantitative differential-expression signature. So "make pAGE continuous" is really two separate problems (see Phase 3).
- The paper's validation leans on broad-coverage CMap perturbation data, which is dominated by a small number of cell lines; a per-drug context (tissue, cell type, dose, time) is largely collapsed.
- Aging is tissue-specific, cell-type-specific, dose-dependent, and time-dependent, yet the age signature is treated as one categorical vector.
- Shortest-path proximity in an undirected interactome is a weak proxy for causal effect.
- Validation emphasizes sensitivity on small positive sets more than precision at the top of the ranked list, and there is no clean negative set.

Meta-commentary: the goal is not to dunk on the paper. The goal is to treat it as a clean baseline. If the improved pipeline cannot beat a simple interpretable baseline, that is useful information.

## Access Check

The project appears feasible from public or academically accessible resources. Several rows below are now resolved in our favor because the authors ship processed data in `BnayaGross/Longevity-module`.

| Component | Access | Notes |
|---|---:|---|
| Original paper methods | Yes | The preprint Box 1 and Nature Fig. 4 / equation 3 describe pAGE clearly enough to reimplement. |
| Authors' study code/data | Yes | Data + scripts at `BnayaGross/Longevity-module`; Python package at `BnayaGross/sharp-aging`. Verify it runs first. |
| Processed interactome | Yes | `PPI_2022.csv` ships in the repo. STRING is used as a second validation network. **No 26-database rebuild needed for reproduction.** |
| OpenGenes aging genes | Yes | `Gene_hallmarks.csv` (module membership) and `age-related-changes.tsv` (pAGE direction) both derive from OpenGenes and ship in the repo. Pin the download date. |
| DrugBank target data | Conditional | `all_drugbank_drugs.csv` ships in the repo, but check DrugBank's license before **re-committing** any DrugBank-derived file under our own repo. |
| CMap/LINCS perturbation data | Yes, with effort | LINCS Level 5 signatures are large (hundreds of GB). Pin the release (GSE92742 / GSE70138). |
| Compute budget | **Constraint** | The published proximity script runs for *weeks* per confidence level. This reorders the whole timeline. See Phase 1 addendum. |
| Validation labels | Partial | Positive sets are small and biased; there is effectively no true negative set. Treat validation claims cautiously (see Phase 7). |

## Project Principles

- Reproduce first, improve second.
- Correctness before speed: every performance optimization must be validated against a slow reference (see Phase 1).
- Keep every data transformation auditable.
- Prefer boring baselines before fancy models.
- Separate "drug is near an aging module" from "drug pushes biology in a beneficial direction."
- Treat aging signatures as context-dependent, not universal truth.
- Do not overclaim clinical relevance from computational rankings.

Meta-commentary: this project can easily drift into a giant graph-ML swamp. Resist that. The first useful result is a clean reproduction plus one demonstrably better scoring model.

## Repo Roadmap

### Phase 0: Paper and Repository Audit

- [ ] Download the paper PDF, preprint, and supplementary information (preprint Box 1 / Nature Fig. 4 and equation 3 define pAGE).
- [ ] Clone or download the authors' repositories:
  - [ ] `BnayaGross/Longevity-module` (data + main scripts)
  - [ ] `BnayaGross/sharp-aging` (Python package)
- [ ] Record commit hashes, package versions, and file checksums.
- [ ] Pin external data versions, not just code: CMap/LINCS release (GSE92742 / GSE70138) and the OpenGenes download date. Both change over time.
- [ ] Identify whether the repos contain:
  - [ ] processed OpenGenes hallmark gene sets (`Gene_hallmarks.csv`)
  - [ ] processed human interactome (`PPI_2022.csv`)
  - [ ] age-related expression changes (`age-related-changes.tsv`)
  - [ ] DrugBank compound-target mappings (`all_drugbank_drugs.csv`)
  - [ ] CMap perturbation signatures (or the accession to fetch them)
  - [ ] validation drug lists
  - [ ] scripts for reproducing paper figures/tables
- [ ] Try to run the authors' pipeline as-is (expect the proximity step to be very slow).
- [ ] Confirm from the authors' code whether the proximity null randomizes the **drug target set only**, or **both the target set and the hallmark module**. This single fact sets the achievable speedup ceiling (see Phase 1).
- [ ] Log every missing file, dependency, manual step, and undocumented assumption.

Deliverable:

- [ ] `docs/repro_audit.md`

Success criterion:

- We know whether the published results are directly reproducible, partially reproducible, or only conceptually reproducible.

### Phase 1: Reimplement the Baseline

Implement a clean local version of the SHARP pipeline.

- [ ] Load hallmark gene sets from OpenGenes or the authors' processed files.
- [ ] Load the human interactome (`PPI_2022.csv`); keep STRING as a second network for the significance check.
- [ ] Map genes to a consistent identifier namespace.
- [ ] Compute largest-connected-component significance for each hallmark. Confirm from the paper/code whether this uses node permutation, edge permutation, or both; the Nature methods describe degree-matched random gene sets.
- [ ] Compute pairwise hallmark separation.
- [ ] Load drug-target mappings, then stratify hallmark modules by **OpenGenes confidence level [1–5]**. Reproduction counts only match if the OpenGenes confidence threshold matches.
- [ ] Compute drug-hallmark proximity using the Guney "closest" measure. Use the authors' NetMedPy subset as the reference implementation rather than reinventing the z-score.
- [ ] Generate degree-matched random controls.
- [ ] Reproduce proximity z-scores (significant proximity cutoff: z < −1.96).
- [ ] Load CMap/LINCS perturbation signatures.
- [ ] Implement pAGE exactly as described in preprint Box 1 / Nature Fig. 4 and equation 3 (ternary encoding, summed; pAGE > 0 = pro-longevity).
- [ ] Reproduce headline counts, per confidence level:
  - [ ] number of longevity-associated genes (target: 2,358 total)
  - [ ] number of hallmark-associated genes (target: 1,250)
  - [ ] number of age-direction genes used for pAGE (target: 2,025)
  - [ ] number of compounds screened (target: 6,442)
  - [ ] number of network-proximal drugs
  - [ ] number of proximal drugs with CMap data
  - [ ] number of positive-pAGE candidates
- [ ] Compare reproduced rankings against the paper.

Deliverables:

- [ ] `src/sharp_baseline/`
- [ ] `notebooks/01_reproduce_sharp.ipynb`
- [ ] `results/baseline_reproduction_summary.md`

Success criterion:

- We can explain any mismatch between our reproduction and the paper.

Meta-commentary: do not improve anything in this phase. Reproduction means copying even the parts we think are crude.

### Phase 1 addendum: Proximity performance (correctness-first)

The published proximity script runs for weeks per confidence level. This is algorithmic, not language-bound: the degree-preserving permutation null recomputes drug-independent work at Python speed. The first pass must reproduce the paper's z-scores exactly; speed is secondary to fidelity.

Why it's slow: the observed scores are ~400k evaluations (seconds). The cost is the ~10³ permutations per drug × hallmark × confidence level (~4×10⁸ evaluations), each doing a per-target inner loop at interpreter speed. The distances are already precomputed (`Create_PPI_2022_distances.ipynb` → `PPI_2022_distances.pkl`), so shortest-path recomputation is *not* the culprit — the null is.

**Correctness anchor (do this first):**

- [ ] Implement the naive per-drug proximity + permutation z-score as a reference oracle. Slow is fine; this is ground truth.
- [ ] Confirm (from Phase 0) whether the null randomizes the drug target set only, or both target set and hallmark module.

**Optimizations (each validated against the oracle to tolerance):**

- [ ] Replace min-over-module with a single multi-source BFS per module, seeded on all module nodes, yielding a per-node distance vector `c_S(v) = min_{s in S} d(v,s)`.
- [ ] Reduce a proximity evaluation to a numpy gather-and-mean over `c_S`: `d_c(T,S) = mean_{t in T} c_S(t)`. The inner loop stops touching the graph.
- [ ] Precompute the module-side null once per hallmark / OpenGenes-confidence-level / network combination (R BFS passes per combination → an R×N int8 distance matrix). Share that work across all drugs within the same combination — the module draws do not depend on the drug.
- [ ] Vectorize the drug-side null: degree-matched target draws as an index matrix, gather + row-mean.
- [ ] Require z-score agreement with the oracle on a held-out drug subset before running at full scale. Assert `abs(z_new - z_ref) < 1e-9` (not bit-exact: BFS tie-breaking and summation order can differ in the last ulp).

Expected result: weeks → hours. If the null is target-only, the BFS count collapses to roughly one observed module-distance vector per hallmark / confidence-level / network combination, and the remaining null is mostly numpy → potentially minutes.

**Deferred (not first pass):**

- [ ] Analytic null: closed-form mean/variance of `c_S` over degree bins to eliminate permutations entirely. Separate, validated experiment — check tail behavior at the z < −1.96 cutoff against the empirical null before trusting it, since the min-based `c_S` can be skewed for small modules.
- [ ] Language/library swap (`scipy.sparse.csgraph`, `igraph`, or Rust) **only** if profiling shows the BFS passes dominate after vectorization. A trigger, not a default — the hot path after vectorization is already C-backed numpy.

Deliverable:

- [ ] `docs/proximity_performance.md` (naive-vs-optimized runtime table + oracle-agreement check)

Blog beat: "The published pipeline takes weeks. The fix wasn't a faster language — it was noticing the permutation null recomputes work that doesn't depend on the drug."

### Phase 2: Build Better Baselines

Before introducing a new method, compare SHARP against simpler alternatives.

- [ ] Target-overlap baseline.
- [ ] Target-degree baseline.
- [ ] CMap reversal-only baseline.
- [ ] Proximity-only baseline.
- [ ] Random drug baseline matched by:
  - [ ] number of targets
  - [ ] target degree
  - [ ] CMap coverage
  - [ ] approval/experimental status
- [ ] Precision-at-k evaluation.
- [ ] Recall/sensitivity evaluation.
- [ ] Calibration plots if probabilistic scores are introduced.

Deliverable:

- [ ] `notebooks/02_baseline_comparisons.ipynb`

Success criterion:

- We know which part of SHARP contributes signal: network proximity, expression reversal, drug-target priors, or database bias.

### Phase 3: Replace pAGE With a Continuous Reversal Score

The first main methodological upgrade is to replace ternary pAGE with a continuous, effect-size-aware score.

Candidate score:

```text
score(drug, hallmark, context)
  = - sum_g w_g * beta_age(g, context) * beta_drug(g, drug, context)
```

where:

- `beta_age` is the estimated age-associated expression effect.
- `beta_drug` is the estimated drug-induced expression effect.
- `w_g` is a confidence, reliability, or hallmark-membership weight.
- `context` may include tissue, cell type, dose, time, or species.

Sign convention: this aligns with pAGE (higher = more reversal = more pro-longevity). If a gene rises with age (`beta_age > 0`) and the drug also raises it (`beta_drug > 0`), the product is positive and the leading minus makes the score negative (bad); reversal makes it positive (good). Preserve this direction so the baseline and continuous scores are directly comparable.

**Key realization — this is two problems, not one:**

- **Drug side (`beta_drug`): feasible now.** CMap/LINCS ships continuous moderated z-scores. This side can go continuous using data already in hand.
- **Age side (`beta_age`): blocked on Phase 5.** The age direction comes from OpenGenes categorical calls. There is no continuous effect size to recover without importing a quantitative aging DE resource (GTEx aging, Tabula Muris Senis, ARCHS4-derived signatures). That is a data-sourcing sub-project, and it *is* Phase 5.

So Phase 3 delivers the continuous drug side with the age side held categorical as an interim; Phase 5 supplies the continuous `beta_age` that completes the score. Treat Phase 3's age term as a placeholder with an explicit dependency on Phase 5.

Todo:

- [ ] Decide whether to use raw CMap z-scores, moderated effects, characteristic-direction scores, or another perturbation statistic for `beta_drug`.
- [ ] Preserve effect magnitude instead of reducing to up/down/unchanged.
- [ ] Preserve replicate uncertainty where available.
- [ ] Keep `beta_age` categorical for now; flag it as the Phase 5 hand-off.
- [ ] Evaluate whether results are robust to gene-level weighting choices.
- [ ] Compare against pAGE on the same candidate set.
- [ ] Identify drugs whose classification changes under the continuous model.

Deliverables:

- [ ] `src/scoring/continuous_reversal.py`
- [ ] `notebooks/03_continuous_reversal.ipynb`
- [ ] `results/pAGE_vs_continuous_reversal.md`

Success criterion:

- The continuous score either improves validation metrics or reveals that pAGE's simplicity is surprisingly hard to beat.

Meta-commentary: if the fancy score only produces prettier math and worse rankings, say so. The blog post gets stronger when it is honest.

### Phase 4: Model Dose, Time, and Cell Line

The paper chooses a CMap instance using highest dose and replicate quality. That is practical, but it discards structure.

Todo:

- [ ] Keep all available CMap instances instead of selecting one.
- [ ] Represent perturbations by dose.
- [ ] Represent perturbations by exposure time.
- [ ] Represent perturbations by cell line.
- [ ] Estimate per-drug variability across contexts.
- [ ] Flag drugs with unstable directionality.
- [ ] Identify drugs with beneficial signatures in one context and harmful signatures in another.

Possible modeling approaches:

- Mixed-effects model.
- Bayesian hierarchical model.
- Simple robust aggregation with sensitivity analysis.
- Leave-one-cell-line-out validation.

Deliverable:

- [ ] `notebooks/04_context_sensitivity.ipynb`

Success criterion:

- We can distinguish robust candidate drugs from context-fragile candidates.

### Phase 5: Add Tissue-Specific Aging Signatures

The second major methodological upgrade is to stop treating aging as one universal categorical vector. This phase also produces the continuous `beta_age` that Phase 3 needs — the two upgrades converge here.

Todo:

- [ ] Identify usable tissue-specific aging expression datasets (quantitative DE, not categorical).
- [ ] Start with a small, defensible set:
  - [ ] blood
  - [ ] brain or neural tissue
  - [ ] liver
  - [ ] muscle
  - [ ] fibroblast or skin
- [ ] Harmonize gene identifiers.
- [ ] Estimate continuous age effects per tissue (this is `beta_age`).
- [ ] Build tissue-specific hallmark vectors.
- [ ] Compute tissue-specific reversal scores using the Phase 3 continuous machinery.
- [ ] Compare tissue-specific rankings to the original all-tissue pAGE ranking.

Deliverables:

- [ ] `data_sources/tissue_aging_sources.md`
- [ ] `notebooks/05_tissue_specific_aging.ipynb`

Success criterion:

- We can show that some candidates are globally plausible but tissue-specific nonsense, or vice versa.

Meta-commentary: this is probably where the project becomes genuinely interesting. It is also where data harmonization can eat unlimited time. Start narrow.

### Phase 6: Improve the Network Model

Shortest-path proximity in an undirected interactome is interpretable but biologically blunt. This is also the natural home for any language/library performance work, if profiling in Phase 1 pointed here.

Possible upgrades:

- Network diffusion or random-walk proximity.
- Signed pathway-aware propagation.
- Tissue-filtered interactomes.
- Causal regulator activity models.
- Separate physical binding, signaling, kinase-substrate, and regulatory edges.

Todo:

- [ ] Reproduce shortest-path proximity first.
- [ ] Implement one alternative network score.
- [ ] Compare stability of candidate rankings.
- [ ] Test whether alternative network scores improve validation metrics.
- [ ] Avoid introducing graph neural networks until simpler graph methods are exhausted.

Deliverable:

- [ ] `notebooks/06_network_score_comparison.ipynb`

Success criterion:

- We know whether shortest-path proximity is a bottleneck or an adequate baseline.

### Phase 7: Validation and Stress Testing

Validation is the easiest place to fool ourselves.

Reproduction targets (name these explicitly): the Nature version validates against **11 ITP lifespan-extending drugs** and **17 drugs in clinical trials for longevity** (e.g., metformin, sirolimus). For the ITP set, 8 of 11 had CMap data and all 8 had positive pAGE plus statistically significant or marginal proximity, yielding **100% sensitivity among CMap-covered ITP positives**. For the clinical-trial set, 9 of 17 had CMap data and 8 of 9 met the same criterion, yielding **88.9% sensitivity among CMap-covered clinical candidates**. If using the preprint, record any different counting rule separately rather than mixing version-specific numbers.

Two problems the original under-weights:

- **Source-level circularity / leakage.** OpenGenes supplies *both* the longevity gene set (module construction) *and* the age-related direction (pAGE). Some validation drugs' longevity relevance traces to the same literature that populates OpenGenes. Defining labels "before looking at rankings" does not fix this — flag it explicitly and, where possible, quarantine label-source overlap.
- **No clean negative set.** There is essentially no defensible "does not affect longevity" set. AUPRC and precision@k are only as trustworthy as the negatives. Named fallback: use decoy / degree-matched permutation nulls instead of pretending we have true negatives.

Todo:

- [ ] Define positive labels before looking at final rankings.
- [ ] Treat negatives as an open problem; default to decoy/permutation nulls.
- [ ] Separate known longevity drugs from candidates used in data construction.
- [ ] Quarantine OpenGenes label-source overlap where possible.
- [ ] Evaluate:
  - [ ] precision at k
  - [ ] recall
  - [ ] AUROC, if meaningful
  - [ ] AUPRC, likely more meaningful
  - [ ] enrichment among top-ranked candidates
- [ ] Perform ablation studies:
  - [ ] no network
  - [ ] no expression reversal
  - [ ] no hallmark weighting
  - [ ] shuffled drug targets
  - [ ] shuffled age signatures
  - [ ] degree-preserving shuffled networks
- [ ] Check whether predictions are dominated by famous genes such as `TP53`, `AKT1`, `MTOR`, `SIRT1`, or `FOXO3`.

Deliverable:

- [ ] `results/validation_report.md`

Success criterion:

- We can state clearly what the improved method does and does not predict.

### Phase 8: Blog Post

The blog post should be written after the reproduction and at least one improvement experiment.

Possible title:

> Rebuilding a Nature Aging Drug-Repurposing Pipeline: What Happens When We Replace a Simple Aging-Reversal Score?

Proposed structure:

1. What the original paper (SHARP) tried to do.
2. Why the baseline is useful.
3. Where the methodology is weak.
4. What data are actually available.
5. Reproduction results — including the weeks-to-hours proximity story.
6. A better scoring model.
7. What changed in the drug rankings.
8. What still does not count as evidence.
9. What an experimental follow-up would need.

Todo:

- [ ] Keep the tone fair.
- [ ] Cite the original paper prominently.
- [ ] Do not imply that computational ranking proves longevity effects.
- [ ] Include code and reproducibility notes.
- [ ] Include the proximity performance beat (naive-vs-optimized runtime table + the "it wasn't the language, it was the null" framing).
- [ ] Include negative results if the improved method fails to help.

Meta-commentary: the best blog post is not "Nature paper bad." The better post is "this is a clean baseline, and here is what breaks or improves when we make the assumptions explicit."

## Suggested Repo Structure

```text
.
├── README.md
├── pyproject.toml
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── data_sources/
│   └── tissue_aging_sources.md
├── docs/
│   ├── repro_audit.md
│   └── proximity_performance.md
├── notebooks/
│   ├── 01_reproduce_sharp.ipynb
│   ├── 02_baseline_comparisons.ipynb
│   ├── 03_continuous_reversal.ipynb
│   ├── 04_context_sensitivity.ipynb
│   ├── 05_tissue_specific_aging.ipynb
│   └── 06_network_score_comparison.ipynb
├── results/
│   ├── baseline_reproduction_summary.md
│   ├── pAGE_vs_continuous_reversal.md
│   └── validation_report.md
├── scripts/
│   ├── download_data.py
│   ├── build_interactome.py
│   └── run_pipeline.py
├── src/
│   ├── sharp_baseline/
│   ├── scoring/
│   ├── networks/
│   ├── validation/
│   └── utils/
└── tests/
```

## Early Technical Decisions

Recommended defaults:

- Use Python.
- Use `uv` or `poetry` for environment management.
- Use `pandas`, `polars`, or both for data wrangling.
- Use `networkx` for initial graph work; for the ~12k module BFS passes use a C-backed traversal (`scipy.sparse.csgraph`, `igraph`, or `graph-tool`) if profiling calls for it.
- Use `scipy` and `statsmodels` for statistics.
- Use `sklearn` for validation metrics.
- Use `snakemake`, `pydra`, `make`, or plain scripts only once the workflow stabilizes.

On Rust (and language swaps generally): deferred by default. The proximity speedup is algorithmic — lifting `min` out of the drug loop and sharing the null — and after vectorization the hot path is already C-backed numpy. A language swap buys a constant factor on top of that and costs "reproduce first" simplicity. Revisit only if a profiler shows the BFS passes dominating (a Phase 6 concern).

Avoid at first:

- Graph neural networks.
- End-to-end deep learning.
- Overbuilt workflow systems.
- Premature language rewrites.
- Unreviewed automated biological interpretation.
- Claims about human intervention, supplement use, or clinical action.

## Third-Party Review Questions

Ask the reviewer:

- Is the reproduction plan sufficient?
- Are the proposed validation labels defensible, given the OpenGenes source-circularity issue?
- Is the decoy/permutation-null approach an acceptable substitute for a true negative set?
- Is the continuous reversal score statistically reasonable, and is the Phase 3/Phase 5 split the right way to stage it?
- What tissue-specific aging datasets (quantitative DE) should be prioritized for `beta_age`?
- Is there a better perturbation resource than CMap/LINCS for this purpose?
- Should the first methodological upgrade focus on expression scoring, network scoring, or validation?
- What claim would be too strong for a blog post?
- What result would actually be publishable or worth turning into a preprint?

## Definition of Done

Minimum useful project:

- [ ] SHARP baseline rerun or reimplemented.
- [ ] Proximity reproduced within tolerance of an oracle, and fast enough to iterate.
- [ ] Reproduction gaps documented.
- [ ] pAGE implemented and tested.
- [ ] Continuous reversal score (drug side) implemented.
- [ ] At least one validation comparison completed.
- [ ] Blog post drafted with honest limitations.

Strong project:

- [ ] Tissue-specific (continuous) aging signatures added, completing `beta_age`.
- [ ] Dose/time/cell-line sensitivity analyzed.
- [ ] Alternative network scoring benchmarked.
- [ ] Analytic proximity null validated against the empirical null in the tails.
- [ ] Top candidate changes explained mechanistically.
- [ ] Code and data processing are clean enough for external review.

## Non-Goals

- This project does not recommend drugs.
- This project does not claim clinical anti-aging effects.
- This project does not replace animal or cell validation.
- This project does not treat CMap reversal as proof of rejuvenation.
- This project does not assume that every age-associated expression change is harmful.

## Final Framing

This project is best understood as a methodological stress test:

> If we rebuild SHARP with better statistical handling of perturbation data, tissue context, and validation, do the same drugs still look good?

That is a concrete, bloggable, scientifically honest question.
