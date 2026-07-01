# EaR³T Education & Research — Project Roadmap
*K. Sebastian Schmidt · University of Colorado Boulder / LASP*
*Started: 2026-06-25 · Last updated: 2026-07-01 (session 12)*

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

**Status: DONE** — `er3t/` committed to repo as of 2026-07-01 (commit 946ef1e).

---

## Data Sources (DECIDED)

Two datasets hosted on Schmidt Lab Google Drive:

| Dataset | File | Google Drive ID | Size | Used by |
|---|---|---|---|---|
| er3t core data (REPTRAN, aux) | `er3t-data.tar.gz` (or similar) | `15YymaUt1i3ad45OZI4kXFDZZlxCNVuGU` | ~180 MB | all examples |
| LES cloud field | `les.nc` | `1cmrZDaCwoQNhaoPGhJ9OhSVEpDU9h-gg` | ~209 MB | examples 02–05 |

Download workflow:
- `er3t/install.sh` — downloads er3t core data + REPTRAN gas absorption database
- `er3t/examples/install-examples.sh` — downloads les.nc only
- MCARaTS, hparx, mcarats-examples tarballs are hosted directly in `er3t-edu/source/`

Note: REPTRAN is from the libRadtran *project* (Gasteiger et al. 2014) but is a standalone
data file, not the libRadtran RT solver. The libRadtran solver is NOT needed by any example.

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
- ✅ Clone URL updated to `konradsebastian/er3t-edu`
- ✅ pip install path updated to `cd er3t-edu/er3t`
- ✅ Directory structure diagram updated to show `er3t-edu/er3t/`
- ✅ All `$ERTDIR/er3t/` paths updated to `$ERTDIR/er3t-edu/er3t/`
- ✅ Core data download step present (install.sh downloads REPTRAN + core data)
- ✅ install-examples.sh downloads les.nc only (not redundant with install.sh)

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
- Embedded er3t teaching fork as er3t/ subdirectory in er3t-edu (commit 946ef1e)
- Updated install.html: clone URL → konradsebastian/er3t-edu, all paths → er3t-edu/er3t/
- Reverted install-examples.sh to les.nc only (install.sh handles core data + REPTRAN)
- Reset plot_only = False in 05_3d_cloud_radiance.py

---

## Pending Actions (in priority order)

### 1. ⚠️ URGENT: Verify er3t test scripts run cleanly [deadline July 5]

`er3t/tests/` contains four package unit tests that students should run right after
installation, BEFORE the pedagogical examples. We have not verified these run yet.

Scripts:
- `tests/00_test_util.py` — utilities; also contains `test_download_worldview()` (see Future Examples)
- `tests/01_test_atm.py` — atmosphere module
- `tests/02_test_abs.py` — absorption module (exercises REPTRAN — most important to verify)
- `tests/03_test_cld.py` — cloud module
- `tests/04_test_pha.py` — phase function module

Action needed:
1. Run all five scripts in the er3t conda environment, confirm clean pass
2. If any fail, fix them or note which to skip/defer
3. Add a "Verify installation" section to install.html pointing students to these tests
4. Note: REPTRAN is downloaded by install.sh and IS required by 02_test_abs.py.
   libRadtran (the RT solver) is NOT needed by any test or example — this is resolved.

### 2. ⚠️ URGENT: Student journey test [deadline July 5]
Clone a fresh copy to `test-install2/` and follow install.html start to finish.
```bash
cd ~/projects/er3t-edu   # or wherever test-install2 should live
git clone https://github.com/konradsebastian/er3t-edu.git test-install2
cd test-install2/er3t
conda env create -f er3t-env.yml
conda activate er3t
pip install -e .
bash install.sh
cd examples
bash install-examples.sh
cd ../tests
python 00_test_util.py
python 01_test_atm.py
python 02_test_abs.py
python 03_test_cld.py
python 04_test_pha.py
```

### 3. Add "Verify installation" section to install.html
Once tests are confirmed working, add a Step after the er3t install that directs students
to run the test scripts. This is what students do between installing and the July 11 session.

### 4. Public/private repo hygiene [post-summer-school]
Currently ROADMAP.md and any other internal files are in the public repo and visible to
students. Options (decide after summer school):
- Move internal docs to a separate private companion repo (cleanest)
- Move to a non-default branch
For now: not a blocker; students are unlikely to look, and content is not harmful.

---

## Future Examples (post-summer-school, needs student coordination)

### Example 06: NASA Worldview — Radiance Self-Consistency
Pull L2 satellite products for a user-chosen region/date from NASA Worldview, run er3t to
predict the radiance a satellite should observe given the retrieved cloud/aerosol state,
then compare with what the satellite actually measured. This is the "radiance
self-consistency" approach described in Chen et al. (2023).

Note: `er3t/tests/00_test_util.py` already contains `test_download_worldview()` which
may provide relevant infrastructure.

Action: coordinate with Schmidt Lab students.

### Example 07: Arctic Aircraft / Satellite Irradiance Comparison (tentative)
Use NASA research aircraft flights from 2024 Arctic campaign. Automatically find the closest
satellite overpass in time. Predict aircraft irradiance from satellite observations and
compare with actual aircraft measurements.

Action: coordinate with Schmidt Lab students.

---

## Summer School Timeline (DECIDED)

- **Summer school**: July 6–11, 2026 — https://c3sar.de/summer-school/
- **er3t day**: July 11 (1.5 hr slot)
- **Website go-live deadline**: July 5 ← only 4 days away as of 2026-07-01
- **Office hours**: July 6–10, students can ask installation questions
- **Student expectations by July 5**: Install er3t, run the test scripts (see below). Examples 01–05 are available to try; covered on July 11.

---

## Open Questions

- Should student projects be Jupyter notebooks or Python scripts?
- What compute resources do students have (laptops only, or Alpine cluster)?

---

## Session-End Checklist (to prevent memory loss)

At the end of every working session:
1. Update this ROADMAP with what was completed and any decisions made
2. Commit ROADMAP.md: `git add ROADMAP.md && git commit -m "Update roadmap" && git push`
3. Note any pending verbal decisions that haven't been executed yet

*Last updated: 2026-07-01 (session 12)*
