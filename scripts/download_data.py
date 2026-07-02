"""Download small, license-compatible source files for the SHARP reproduction."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


MAX_BYTES = 10 * 1024**3
ROOT = Path(__file__).resolve().parents[1]
LONVER = "69ff9e6f8c455b25e9947649cffe28dd77f358ae"


def raw_url(path: str) -> str:
    quoted = "/".join(quote(part) for part in path.split("/"))
    return f"https://raw.githubusercontent.com/BnayaGross/Longevity-module/{LONVER}/{quoted}"


DOWNLOADS = [
    (
        "arxiv_pdf",
        "https://arxiv.org/pdf/2509.03330",
        "sources/pdfs/2509.03330v1.pdf",
    ),
    (
        "gene_hallmarks",
        raw_url("data/Gene_hallmarks.csv"),
        "data/raw/longevity_module/Gene_hallmarks.csv",
    ),
    (
        "age_related_changes",
        raw_url("data/age-related-changes.tsv"),
        "data/raw/longevity_module/age-related-changes.tsv",
    ),
    ("ppi_2022", raw_url("data/PPI_2022.csv"), "data/raw/longevity_module/PPI_2022.csv"),
    (
        "ppi_string",
        raw_url("data/PPI_STRING.csv.zip"),
        "data/raw/longevity_module/PPI_STRING.csv.zip",
    ),
    (
        "cmap_readme",
        raw_url("CMap_data/README.txt"),
        "data/raw/longevity_module/CMap_data/README.txt",
    ),
    (
        "cmap_geneinfo",
        raw_url("CMap_data/geneinfo_beta.txt"),
        "data/raw/longevity_module/CMap_data/geneinfo_beta.txt",
    ),
    (
        "cmap_compoundinfo",
        raw_url("CMap_data/compoundinfo_beta.txt"),
        "data/raw/longevity_module/CMap_data/compoundinfo_beta.txt",
    ),
    (
        "cmap_field_definitions",
        raw_url("CMap_data/LINCS2020 Release Metadata Field Definitions.xlsx"),
        "data/raw/longevity_module/CMap_data/LINCS2020_Release_Metadata_Field_Definitions.xlsx",
    ),
]

RESULT_FILES = [
    "drug_evidence_Cell senescence.csv",
    "drug_evidence_Epigenetic alterations.csv",
    "drug_evidence_proximity_hallmarks.csv",
    "drug_evidence_Altered intercellular communication.csv",
    "drug_evidence_Deregulated nutrient sensing.csv",
    "drug_evidence_Disabled macroautophagy.csv",
    "drug_evidence_Telomere attrition.csv",
    "drug_evidence_Loss of proteostasis.csv",
    "drug_evidence_Genomic instability.csv",
    "drug_evidence_Mitochondrial dysfunction.csv",
    "drug_evidence_Changes in the extracellular matrix structure.csv",
    "drug_evidence_Exhaustion of stem cells.csv",
]

SKIPPED = [
    (
        "all_drugbank_drugs.csv.zip",
        "DrugBank-derived file; requires license review before copying or redistribution.",
    ),
    (
        "level5_beta_trt_cp_n720216x12328.gctx",
        "CMap/CLUE matrix; check access terms and size. Do not pull if over 10 GB.",
    ),
    (
        "siginfo_beta.txt",
        "CMap/CLUE signature metadata; check access terms and size before pulling.",
    ),
    (
        "PPI_2022_distances.pkl",
        "Large generated all-pairs distance artifact; prefer regenerating or replacing.",
    ),
]


def request(url: str, method: str = "GET") -> Request:
    return Request(url, method=method, headers={"User-Agent": "geglb-aging-drug-redo"})


def remote_size(url: str) -> int | None:
    try:
        with urlopen(request(url, "HEAD"), timeout=30) as response:
            value = response.headers.get("Content-Length")
            return int(value) if value else None
    except (HTTPError, URLError, TimeoutError):
        return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_one(name: str, url: str, relative_path: str) -> tuple[str, Path, int, str]:
    destination = ROOT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    size = remote_size(url)
    if size is not None and size > MAX_BYTES:
        raise RuntimeError(f"{name} is {size} bytes, over the 10 GB cap")

    with urlopen(request(url), timeout=120) as response:
        data = response.read()

    if len(data) > MAX_BYTES:
        raise RuntimeError(f"{name} downloaded over the 10 GB cap")

    destination.write_bytes(data)
    return name, destination, len(data), sha256(destination)


def all_downloads() -> list[tuple[str, str, str]]:
    result_downloads = [
        (
            f"result_{index:02d}",
            raw_url(f"Proximity and pAGE results/{filename}"),
            f"data/raw/longevity_module/results/{filename}",
        )
        for index, filename in enumerate(RESULT_FILES, start=1)
    ]
    return DOWNLOADS + result_downloads


def main() -> int:
    for name, url, relative_path in all_downloads():
        pulled = download_one(name, url, relative_path)
        _, path, size, digest = pulled
        print(f"pulled {path.relative_to(ROOT)}\t{size}\t{digest}")

    for name, reason in SKIPPED:
        print(f"skipped {name}\t{reason}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
