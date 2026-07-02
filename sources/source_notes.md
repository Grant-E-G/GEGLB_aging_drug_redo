# Source Notes

## Gross et al., SHARP Aging Drug Repurposing

- Citation: Gross, B., Ehlert, J., Gladyshev, V. N., Loscalzo, J., and
  Barabasi, A. L. "Network-driven discovery of repurposable drugs targeting
  hallmarks of aging." arXiv:2509.03330.
- Location: https://arxiv.org/abs/2509.03330
- Local copy: `sources/pdfs/2509.03330v1.pdf` (ignored by git).
- Main result: introduces SHARP, combining hallmark-module network proximity
  with pAGE expression directionality to prioritize repurposable drugs.
- Relevant definitions: hallmark module, Guney closest proximity, pAGE.
- Notes: reproduce first, then evaluate continuous expression scoring and
  tissue/context-specific variants.

## BnayaGross/Longevity-module

- Citation: author data/scripts repository for the SHARP paper.
- Location: https://github.com/BnayaGross/Longevity-module
- Commit checked: `69ff9e6f8c455b25e9947649cffe28dd77f358ae`.
- Main result: ships processed inputs and published proximity/pAGE outputs.
- Relevant definitions: proximity scripts, LCC significance notebook, pAGE
  notebook, processed PPI/OpenGenes/CMap metadata files.
- Notes: full CMap matrix and `PPI_2022_distances.pkl` are not present in
  GitHub; DrugBank-derived target file needs license review.

## BnayaGross/sharp-aging

- Citation:
- Location: https://github.com/BnayaGross/sharp-aging
- Commit checked: `a4b18789e10535a779582048f1c9fa94348719c4`.
- Main result: small MIT-licensed Python package version of SHARP components.
- Relevant definitions: `sharp/core/proximity.py`, `sharp/expression/page.py`,
  `sharp/module/ranking.py`.
- Notes: use as a reference, not vendored into this repo yet.
