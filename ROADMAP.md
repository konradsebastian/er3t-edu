# EaR³T Education & Research — Project Roadmap
*K. Sebastian Schmidt · University of Colorado Boulder / LASP*
*Started: 2026-06-25 · Last updated: 2026-07-01 (session 13)*

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

**Hong Chen confirmed (2026-07-01)** that he is aware of and OK with the teaching fork.

**Upstream branch note**: The `master` branch of `hong-chen/er3t` is outdated. The current
development branch is `release/v0.2.0-alpha.1` — this is what the Libera L2 algorithm uses and
represents Hong's latest work. Our teaching fork was derived from the Libera version (equivalent
to `release/v0.2.0-alpha.1`), so we already have REPTRAN support and all current fixes.
If re-forking in the future, fork directly from `release/v0.2.0-alpha.1`.

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

## Example Scripts

All scripts live in `er3t-edu/er3t/examples/`. Summer school (July 11) covers examples 01–05.
Example 06 is written and available but not part of the summer school curriculum.

| Script | Status | Data needed | Summer school |
|---|---|---|---|
| `01_clear_sky_flux.py` | ✅ done | core data | ✅ yes |
| `02_3d_cloud_flux.py` | ✅ done | core + les.nc | ✅ yes |
| `03_cloud_aerosol_flux.py` | ✅ done | core + les.nc | ✅ yes |
| `04_cloud_aerosol_spectral.py` | ✅ done | core + les.nc | ✅ yes |
| `05_3d_cloud_radiance.py` | ✅ done | core + les.nc | ✅ yes |
| `05_3d_cloud_radiance_plot.py` | ✅ done | output of 05 | ✅ yes (standalone plot script) |
| `06_generated_cloud_radiance.py` | ✅ done | core only | ⏸ available, not in curriculum |
| `verify_install.py` | ✅ done | core + MCARaTS | ✅ yes (run right after install) |

**What example 06 does** (synthetic cloud generator, no real satellite data):
Uses `cld_gen_hem` to create user-controlled hemispheroidal cumulus clouds (configurable cloud
fraction, radii, altitude, width-to-height ratio), then simulates nadir radiance with MCARaTS.
Three output panels: 3D cloud-top height surface, COT map, simulated radiance. No external
data download or Earthdata credentials required — only er3t core data + MCARaTS.
Excluded from summer school curriculum but available for students who want to explore further.

**Note on abs_16g**: `abs_16g.h5` is NOT present in the teaching data package. The `abs_16g`
absorption module is therefore non-functional. This is flagged in `verify_install.py` as a
skipped check (not needed for examples 01–06). Action item: obtain `abs_16g.h5` if needed
for future examples (see Pending Actions).

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

### Session 13 (2026-07-01, continued)
- Updated roadmap with summer school timeline, test scripts, future examples
- Discovered existing tests/00–04 are developer unit tests, not student-facing
- Wrote `verify_install.py` — student-facing install verifier (7 checks + optional Worldview)
  - Checks: Python, imports, atm_atmmod, abs_16g (skip/expected), abs_rep/REPTRAN, pha_mie_wc, MCARaTS exe
  - `--worldview` flag tests Worldview RGB download (no credentials needed for RGB tiles)
- Security fix: removed two hard-coded credentials from upstream er3t code (Hong Chen's):
  - `daac.py`: Earthdata JWT token for user hoch4240 → now raises warning + reads EARTHDATA_TOKEN
  - `util.py`: SMTP password for mail.hongchen.cz → now reads from env vars
  - Hong Chen notified; **he confirmed (2026-07-01) no security risk on his end**:
    - Token: NASA revokes every 3 months, already expired — intentionally included for out-of-box use
    - SMTP password: created solely for er3t, uploaded knowingly — no rotation needed
- Clarified example numbering — two distinct things previously confused:
  - Example 06 (`06_generated_cloud_radiance.py`): ALREADY WRITTEN, synthetic cloud generator,
    no real satellite data, no Earthdata needed
  - Future Example 07: Worldview satellite comparison (NOT YET WRITTEN, needs Earthdata)
- **verify_install.py passed** on real er3t env; conda env confirmed → er3t-edu/er3t/
- Added Step 5 "Verify your installation" to install.html with expected output and hints

### Session 14 (2026-07-01, evening — email from Hong Chen)
- Received reply from Hong Chen re: upstream branch, security, and radiance self-consistency code
- **Upstream branch**: `master` is outdated; correct branch is `release/v0.2.0-alpha.1` (Libera flavor)
  Our teaching fork was derived from the Libera version, so we already have everything we need
- **Security concerns resolved**: Hong confirmed no risk from either credential
  (token: intentional, NASA rotates every 3 months, already expired; SMTP password: created for er3t only)
- **Radiance self-consistency code found**: `projects/02_modis_rad-sim.py` on `release/v0.2.0-alpha.1`
  — confirmed as the starting point for future Example 07
- Updated ROADMAP with all of the above

---

## Pending Actions (in priority order)

### ✅ ~~1. Run verify_install.py end-to-end~~ — DONE (2026-07-01)
All checks passed. Conda env confirmed pointing to `er3t-edu/er3t/er3t/__init__.py`.
abs_16g shows `—` (expected skip). MCARaTS, REPTRAN, Mie phase functions all ✓.

### 2. ⚠️ URGENT: Student journey test [deadline July 5]
Clone a fresh copy to `test-install2/` and follow install.html start to finish:
```bash
git clone https://github.com/konradsebastian/er3t-edu.git test-install2
cd test-install2/er3t
conda env create -f er3t-env.yml
conda activate er3t
pip install -e .
bash install.sh
cd examples
bash install-examples.sh
python verify_install.py
python 01_clear_sky_flux.py
```

### ✅ ~~3. Add verify_install.py step to install.html~~ — DONE (2026-07-01)
Added as Step 5 in install.html (between libRadtran Step 4 and examples Step 6).
Shows expected output, explains ✓/✗/— symbols, callout for MCARaTS env var fix.

### 4. Obtain abs_16g.h5 [post-summer-school]
`abs_16g.h5` is not in the current teaching data package. The abs_16g absorption module
is non-functional. Not needed for examples 01–06 but may be needed for future examples.
Action: ask Hong Chen where this file comes from / how to regenerate it.

### 5. Earthdata credentials — decide when students need them [before Example 07]
No credentials needed for examples 01–06 or verify_install.py (Worldview RGB is public).
Future Example 07 (Worldview satellite comparison) will require Earthdata credentials.
When that example is developed, add a prerequisite step to install.html:
  - Create Earthdata account at https://urs.earthdata.nasa.gov
  - Generate a token and add to shell rc: `export EARTHDATA_TOKEN="..."`

### 6. Public/private repo hygiene [post-summer-school]
ROADMAP.md and internal files are publicly visible in the repo. Options:
- Move to a separate private companion repo (cleanest)
- Move to a non-default branch
Not a blocker now; students are unlikely to look, content is not sensitive.

---

## Future Examples (post-summer-school, needs student coordination)

**Numbering note**: Example 06 (`06_generated_cloud_radiance.py`) already exists as a
synthetic cloud generator. The future satellite examples are numbered 07 and 08.

### Example 07: NASA Worldview — Radiance Self-Consistency (NOT YET WRITTEN)
Pull L2 satellite products for a user-chosen region/date from NASA Worldview, run er3t to
predict the radiance a satellite should observe given the retrieved cloud/aerosol state,
then compare with what the satellite actually measured. This is the "radiance
self-consistency" approach described in Chen et al. (2023).

Prerequisites for students: Earthdata account + token (see Pending Action #5).

**Existing code (confirmed by Hong Chen, 2026-07-01)**:
- Starting point: `projects/02_modis_rad-sim.py` on `hong-chen/er3t` branch `release/v0.2.0-alpha.1`
  - https://github.com/hong-chen/er3t/blob/release/v0.2.0-alpha.1/projects/02_modis_rad-sim.py
- `er3t/util/daac.py` contains `download_worldview_image()` and Earthdata download infrastructure
- `er3t/tests/00_test_util.py` has a `test_download_worldview()` prototype
- Vikas may have more advanced download/processing code — contact him

Action: coordinate with Schmidt Lab students; review `02_modis_rad-sim.py` as starting point.

### Example 08: Arctic Aircraft / Satellite Irradiance Comparison (tentative, NOT YET WRITTEN)
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

*Last updated: 2026-07-01 (session 14)*
