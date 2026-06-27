# STL geometry archive (multi-volume RAR)

GitHub blocks single files over 100 MB. The mesh (`.stl`) deliverables for this
tool total ~1.05 GB of **ASCII** STL, so they are shipped here as a single
multi-volume RAR archive (90 MB volumes) instead of loose files or Git LFS.

## Files
- `SHEX_STL_GEOMETRY.part01.rar`
- `SHEX_STL_GEOMETRY.part02.rar`

## How to extract
Download **both** parts into this folder, then extract `part01` — the rest are
pulled in automatically. Paths are stored relative to the repository root, so
the STLs land back in their original locations, e.g.:

```
export/full_tool/stl/SHEX-BP-UHEX-54_FULL_RUN-IN.stl
export/full_tool/stl/SHEX-BP-UHEX-54_FULL_SET.stl
export/REVISIONS/Rev-B_DCN-12_CURRENT/stl/full-tool/...
export/REVISIONS/Rev-A_DCN-01-11_PREVIOUS/stl/full-tool/...
export/release/stl/...
```

**WinRAR:**  right-click `part01.rar` → *Extract Here*.

**7-Zip:**  right-click `part01.rar` → *7-Zip → Extract Here*.

**CLI (from the repo root):**
```
"C:\Program Files\WinRAR\Rar.exe" x export\_stl_archive\SHEX_STL_GEOMETRY.part01.rar
# or
"C:\Program Files\7-Zip\7z.exe" x export\_stl_archive\SHEX_STL_GEOMETRY.part01.rar
```

## Or regenerate from source
The STLs are reproducible from the parametric CAD scripts (no archive needed):
```
python generate_full_tool.py     # complete run-in / set tool STL + STEP
python build_revisions.py         # per-revision archive (Rev A / Rev B)
```

> The loose `*.stl` files are intentionally git-ignored (see `.gitignore`); this
> archive is their tracked form.
