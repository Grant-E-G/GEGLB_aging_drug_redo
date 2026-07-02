# Data

Raw, interim, and processed data are local working artifacts and are ignored by
git by default.

Use:

```bash
python scripts/download_data.py
```

to recreate the initial raw pull. Tracked provenance and size notes live in
`data_sources/dataset_manifest.md`.
