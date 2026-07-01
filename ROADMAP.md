# EaR³T Education & Research — Project Roadmap
*K. Sebastian Schmidt · University of Colorado Boulder / LASP*
*Started: 2026-06-25 · Last updated: 2026-07-01*

---

## Vision

Build a GitHub Pages website for teaching and summer school use centered on EaR³T (Education and Research 3D Radiative Transfer Toolbox), developed in the Schmidt lab at CU Boulder. The site serves as the home base for students to install the tool and work through examples that take them from the 1D view of the world to a 3D-aware one.

Two audiences:
- **Summer school participants** (immediate need: 1.5-hr slot + pre-school office hours)
- **Courses at CU Boulder** (future expansion)

Core pedagogical arc: *Why does 3D matter? → How do we model it? → Do it yourself.*

---

## Repository Strategy (DECIDED)

**Single repo: `konradsebastian/er3t-edu`** hosts everything:
- `docs/`        — GitHub Pages website
- `source/`      — MCARaTS, hparx, mcarats-examples tarballs (mirrored here to avoid external link rot)
- `er3t/`        — Teaching fork of Hong Chen's er3t package (our modified version)
- `ROADMAP.md`   — This file

The original `hong-chen/er3t` remains the upstream research codebase. Our `er3t/` subdirectory is explicitly a **teaching fork** — simplified examples, student-facing control blocks, pedagogical annotations. It is NOT intended to be merged back upstream.

Students install with:
```bash
git clone https://github.com/konradsebastian/er3t-edu.git
cd er3t-edu/er3t
pip install -e .
```

**Status: PENDING** — `er3t/` subdirectory not yet committed to the repo.
Currently lives at `~/projects/er3t-edu/test-install/er3t/` (local only).
Action needed: copy into `er3t-edu/er3t/`, commit, push.

---

## Data Sources (DECIDED)

Two datasets hosted on Schmidt Lab Google Drive:

| Dataset | File | Google Drive ID | Size | Used by |
|---|---|---|---|---|
| er3t core data (REPTRAN, aux) | `er3t-data.tar.gz` (or similar) | `15YymaUt1i3ad45OZI4kXFDZZlxCNVuGU` | ~180 MB | all examples |
| LES cloud field | `les.nc` | `1cmrZDaCwoQNhaoPGhJ9OhSVEpDU9h-gg` | ~209 MB | examples 02–05 |

Both downloaded via `install-examples.sh` using `gdown`.
MCARaTS, hparx, mcarats-examples tarballs are hosted directly in `er3t-edu/source/`.

---

## Example Scripts (DECIDED: 01–05 only for summer school)

All scripts live in `er3t-edu/er3t/examples/`. Example 06 exists locally but is excluded from the summer school package.

| Script | Status | Description |
|---|---|---|
| `01_clear_sky_flux.py` | ✅ done | Clear-sky flux profile, Monte Carlo noise demo |
| `02_3d_cloud_flux.py` | ✅ done | LES cloud flux, 3D vs IPA comparison |
| `03_cloud_aerosol_flux.py` | ✅ done | Cloud + aerosol, 3 output figs (map/profile/xsection), km axes, (x0,y0) star |
| `04_cloud_aerosol_spectral.py` | ✅ done | Spectral flux, 2×4 layout, ±1σ bands, x cross-section column |
| `05_3d_cloud_radiance.py` | ✅ done | 3D radiance, 3 output figs, plot_only mode, Coakley r(τ) with fit |
| `05_3d_cloud_radiance_plot.py` | ✅ done | Standalone plot-only script (no er3t import), for student modification |
| `06_generated_cloud_radiance.py` | ⏸ excluded | Exists locally; not part of summer school package |

Key fixes applied to er3t package:
- `abs_rep` fix: corrected spectral bin handling that caused shape mismatch in flux outputs
- All examples use `target='flux'` (not `target='flux0'`) to get full 21-level output

---

## Website (docs/install.html)

Hosted at: https://konradsebastian.github.io/er3t-edu/install.html

Current state:
- ✅ Full installation walkthrough (conda env, MCARaTS compile, er3t install)
- ✅ Examples 01–05 described with expected outputs and what to look for
- ✅ Example 06 removed
- ❌ Clone URL still points to `hong-chen/er3t` → needs to change to `konradsebastian/er3t-edu`
- ❌ Core data download step missing from install instructions
- ❌ install-examples.sh step needs updating to reflect both datasets

---

## Completed Work (chronological)

### Sessions 1–2 (2026-06-25)
- Analysed EaR³T papers, extracted application summary
- Created ROADMAP, project folder, website skeleton
- Decided on single-repo strategy (er3t inside er3t-edu)

### Sessions 3–5
- Walked through full installation from scratch
- Fixed `abs_rep` issue in er3t package
- Verified 00_er3t_mca.py runs end-to-end
- Created er3t core data tarball, uploaded to Google Drive (ID: `15YymaUt1i3ad45OZI4kXFDZZlxCNVuGU`)
- Uploaded les.nc to Google Drive (ID: `1cmrZDaCwoQNhaoPGhJ9OhSVEpDU9h-gg`)
- MCARaTS/hparx/mcarats-examples tarballs hosted in er3t-edu/source/

### Sessions 6–10 (2026-06-26 to 2026-07-01)
- Wrote examples 01–05 from scratch (student control blocks, km axes, km coordinates)
- Example 03: 3 output figures (map/profile/xsection), (x0,y0) output location with star marker
- Example 04: spectral loop, 2×4 layout (IPA row / 3D row), ±1σ fill_between, x cross-section column
- Example 05: both solvers in one run, 3 output figures, plot_only mode, Coakley two-stream r(τ) with scipy fit
- Example 05_plot: standalone plotting script with no er3t dependency
- Updated install.html for examples 01–05, removed example 06, "five examples" throughout
- Pushed website update to konradsebastian/er3t-edu

---

## Pending Actions (in priority order)

### 1. Embed er3t into er3t-edu repo [BLOCKING everything else]
```bash
# From your terminal:
cp -r ~/projects/er3t-edu/test-install/er3t ~/projects/er3t-edu/er3t
cd ~/projects/er3t-edu
echo "er3t/tmp-data/" >> .gitignore
echo "er3t/**/__pycache__/" >> .gitignore
echo "er3t/**/*.pyc" >> .gitignore
git add er3t/
git add .gitignore
git commit -m "Add er3t teaching fork as er3t/ subdirectory"
git push origin main
```

### 2. Update install.html clone URL
Change `git clone https://github.com/hong-chen/er3t.git` →
```bash
git clone https://github.com/konradsebastian/er3t-edu.git
cd er3t-edu/er3t && pip install -e .
```
(I will prepare this edit once step 1 is done.)

### 3. Wire core data download into install-examples.sh
Already done in the script — needs push after step 1.

### 4. Test full student install journey
Clone fresh copy of er3t-edu, follow install.html exactly, run example 01.

---

## Open Questions

- Summer school date / how much lead time for pre-installation office hours?
- Should student projects be Jupyter notebooks or Python scripts?
- What compute resources do students have (laptops only, or Alpine cluster)?
- libRadtran installation — needed for which examples? (flagged as tomorrow's task in earlier session)

---

## Session-End Checklist (to prevent memory loss)

At the end of every working session:
1. Update this ROADMAP with what was completed and any decisions made
2. Commit ROADMAP.md: `git add ROADMAP.md && git commit -m "Update roadmap" && git push`
3. Note any pending verbal decisions that haven't been executed yet

*Last updated: 2026-07-01*
