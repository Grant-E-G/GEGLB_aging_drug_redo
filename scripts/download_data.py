"""Download local source files for the SHARP reproduction.

The downloaded data lives under ignored paths. Files over 10 GB are reported and
not downloaded.
"""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


MAX_BYTES = 10 * 1024**3
ROOT = Path(__file__).resolve().parents[1]
LONVER = "69ff9e6f8c455b25e9947649cffe28dd77f358ae"
CMAP_ROOT = "https://s3.amazonaws.com/macchiato.clue.io/builds/LINCS2020"
GCTX_URL = f"{CMAP_ROOT}/level5/level5_beta_trt_cp_n720216x12328.gctx"
SIGINFO_URL = f"{CMAP_ROOT}/siginfo_beta.txt"


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
    (
        "cmap_siginfo",
        SIGINFO_URL,
        "data/raw/longevity_module/CMap_data/siginfo_beta.txt",
    ),
    (
        "drugbank_targets_zip",
        raw_url("data/all_drugbank_drugs.csv.zip"),
        "data/raw/longevity_module/all_drugbank_drugs.csv.zip",
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
        "level5_beta_trt_cp_n720216x12328.gctx",
        "CMap/CLUE matrix is 35,518,405,386 bytes, over the 10 GB cap.",
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
    partial = destination.with_suffix(destination.suffix + ".part")

    size = remote_size(url)
    if size is not None and size > MAX_BYTES:
        raise RuntimeError(f"{name} is {size} bytes, over the 10 GB cap")

    total = 0
    with urlopen(request(url), timeout=120) as response:
        with partial.open("wb") as handle:
            for block in iter(lambda: response.read(1024 * 1024), b""):
                total += len(block)
                if total > MAX_BYTES:
                    partial.unlink(missing_ok=True)
                    raise RuntimeError(f"{name} downloaded over the 10 GB cap")
                handle.write(block)

    partial.replace(destination)
    return name, destination, total, sha256(destination)


def extract_drugbank_targets() -> None:
    zip_path = ROOT / "data/raw/longevity_module/all_drugbank_drugs.csv.zip"
    if not zip_path.exists():
        return

    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if member.startswith("__MACOSX/") or member.endswith("/"):
                continue
            if Path(member).name != "all_drugbank_drugs.csv":
                continue
            destination = zip_path.parent / "all_drugbank_drugs.csv"
            destination.write_bytes(archive.read(member))


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

    extract_drugbank_targets()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
