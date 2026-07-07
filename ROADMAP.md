# EaR³T Education & Research — Project Roadmap
*K. Sebastian Schmidt · University of Colorado Boulder / LASP*
*Started: 2026-06-25 · Last updated: 2026-07-07 (session 18)*

---

## Vision

Build a GitHub Pages website for teaching and summer school use centered on EaR³T (Education and Research 3D Radiative Transfer Toolbox), developed in the Schmidt lab at CU Boulder. The site serves as the home base for students to install the tool and work through examples that take them from the 1D view of the world to a 3D-aware one.

Two audiences:
- **Summer school participants** (immediate need: 1.5-hr slot + pre-school office hours)
- **Courses at CU Boulder** (future expansion)

Core pedagogical arc: *Why does 3D matter? → How do we model it? → Do it yourself.*

---

## Repository Strategy (UPDATED 2026-07-07)

### Two-repo architecture (confirmed live 2026-07-07)

| Repo | Purpose | Local path | Branch | Status |
|---|---|---|---|---|
| `konradsebastian/er3t-edu` | Website (docs/), roadmap | `~/projects/er3t-edu/` | `main` | ✅ active |
| `hong-chen/er3t` | All er3t code + teaching examples | `~/projects/er3t-edu/er3t-dev/` | `dev_er3t_edu` | ✅ live |

**Correction (2026-07-07)**: An earlier draft of this section — and this document only,
not the website — referred to the teaching branch as `teaching/summer-school-2026`. That
rename never actually happened. Verified 2026-07-07 via `git ls-remote --heads` against the
real `hong-chen/er3t` remote: the only teaching branch present is `dev_er3t_edu`, and its
tip commit matches exactly what we've been pushing. `install.html` (nav link, Step 1 clone
command, Resources section) has consistently pointed to `dev_er3t_edu` the whole time, so
no website fix was needed — only this file was out of date.

**Rationale**: Hong Chen (er3t upstream maintainer) prefers a dedicated teaching branch
on his own repo over a fork under a different GitHub account. This avoids divergence and
keeps the code lineage clear.

**Teaching branch** (`dev_er3t_edu` on `hong-chen/er3t`):
- Based on `release/v0.2.0-alpha.1` (Hong's current Libera flavor — NOT master, which is outdated)
- Contains examples 01–07, `tests/`, `verify_install.py`, `install-examples.sh`
- **Student journey test**: ✅ passed (smoke-tested via `test-install2` clone, 2026-07-06/07)

**Development working directory**: `~/projects/er3t-edu/er3t-dev/`
- Local clone of `hong-chen/er3t` (`dev_er3t_edu` branch); new code is committed here directly and pushed
- Website content lives in the separate `~/projects/er3t-edu/` repo (`konradsebastian/er3t-edu`, `main` branch) — kept out of the code repo entirely, not a subdirectory of it

**Smoke-test clone**: `~/projects/er3t-edu/test-install2/`
- Fresh clone used to reproduce and verify student-reported bugs (fresh conda env, fresh checkout) before landing a fix in `er3t-dev`

**Students install with**:
```bash
cd $ERTDIR
git clone -b dev_er3t_edu https://github.com/hong-chen/er3t.git er3t
cd er3t
conda env create -f er3t-env.yml
conda activate er3t
```

**Upstream branch note**: The `master` branch of `hong-chen/er3t` is outdated. Always use
`release/v0.2.0-alpha.1` as the base. Our teaching branch was built on this branch.

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
- MCARaTS, hparx, mcarats-examples tarballs are hosted directly in `dev_er3t_edu/source/`

Note: REPTRAN is from the libRadtran *project* (Gasteiger et al. 2014) but is a standalone
data file, not the libRadtran RT solver. The libRadtran solver is NOT needed by any example.

---

## Example Scripts

All scripts live in `er3t-dev/examples/`. Summer school (July 11) covers examples 01–05.
Examples 06–07 are written, committed, and documented on the site, but optional/advanced —
not part of the core summer school slot.

| Script | Status | Data needed | Summer school |
|---|---|---|---|
| `01_clear_sky_flux.py` | ✅ done | core data | ✅ yes |
| `02_3d_cloud_flux.py` | ✅ done | core + les.nc | ✅ yes |
| `03_cloud_aerosol_flux.py` | ✅ done | core + les.nc | ✅ yes |
| `04_cloud_aerosol_spectral.py` | ✅ done | core + les.nc | ✅ yes |
| `05_3d_cloud_radiance.py` | ✅ done | core + les.nc | ✅ yes |
| `05_3d_cloud_radiance_plot.py` | ✅ done | output of 05 | ✅ yes (standalone plot script) |
| `06_modis_data_download.py` | ✅ done — committed + pushed 2026-07-07 | EARTHDATA_TOKEN + download | ⏸ optional / advanced |
| `07_modis_radiance.py` | ✅ done — committed + pushed 2026-07-07 | `modis_scene_input.h5` from 06 | ⏸ optional / advanced |
| `verify_install.py` | ✅ done | core + MCARaTS | ✅ yes (run right after install) |

**What example 06 does**: Downloads real MODIS data (MYD02QKM/MOD02QKM, MYD03/MOD03,
MYD06_L2/MOD06_L2, MCD43A1, MCD43A3) plus a Worldview RGB for a student-chosen date/extent/
satellite, grids everything to 250 m, and saves `modis_scene_input.h5` for use by example 07.
Requires an `EARTHDATA_TOKEN`.

**What example 07 does**: Runs a 3D MCARaTS radiance simulation from example 06's output and
compares it against the MODIS-measured radiance for the same scene — reproducing Appendix 2 of
Chen et al. (2023). Produces a 4-panel figure (MODIS measured, EaR³T simulated, density scatter,
MC noise map).

Both documented in `docs/examples.html` and referenced from `install.html` and `science.html`
("seven examples" language updated site-wide 2026-07-07).

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
(repo: `konradsebastian/er3t-edu`, separate from the `hong-chen/er3t` code repo)

Current state:
- ✅ Full installation walkthrough (conda env, MCARaTS compile, er3t install)
- ✅ Examples 01–07 described with expected outputs and what to look for (06/07 added 2026-07-07)
- ✅ Clone URL points to `hong-chen/er3t` branch `dev_er3t_edu` — confirmed consistent with
  where code is actually pushed (verified via `git ls-remote` 2026-07-07)
- ✅ All path references updated: `$ERTDIR/er3t/` throughout
- ✅ Core data download step present (install.sh downloads REPTRAN + core data)
- ✅ install-examples.sh downloads les.nc only (not redundant with install.sh)
- ✅ Step 5/6 verify_install.py + examples walkthrough section with expected output
- ✅ No placeholder callouts remaining

---

## Completed Work (chronological)

### Sessions 1–2 (2026-06-25)
- Analysed EaR³T papers, extracted application summary
- Created ROADMAP, project folder, website skeleton
- Decided on single-repo strategy (er3t inside dev_er3t_edu)

### Sessions 3–5
- Walked through full installation from scratch
- Fixed `abs_rep` issue in er3t package
- Verified 00_er3t_mca.py runs end-to-end
- Created er3t core data tarball, uploaded to Google Drive (ID: `15YymaUt1i3ad45OZI4kXFDZZlxCNVuGU`)
- Uploaded les.nc to Google Drive (ID: `1cmrZDaCwoQNhaoPGhJ9OhSVEpDU9h-gg`)
- MCARaTS/hparx/mcarats-examples tarballs hosted in dev_er3t_edu/source/

### Sessions 6–10 (2026-06-26 to 2026-07-01)
- Wrote examples 01–05 from scratch (student control blocks, km axes, km coordinates)
- Example 03: 3 output figures (map/profile/xsection), (x0,y0) output location with star marker
- Example 04: spectral loop, 2×4 layout (IPA row / 3D row), ±1σ fill_between, x cross-section column
- Example 05: both solvers in one run, 3 output figures, plot_only mode, Coakley two-stream r(τ) with scipy fit
- Example 05_plot: standalone plotting script with no er3t dependency
- Updated install.html for examples 01–05, removed example 06, "five examples" throughout
- Pushed website update to konradsebastian/dev_er3t_edu
- Embedded er3t teaching fork as er3t/ subdirectory in dev_er3t_edu (commit 946ef1e)
- Updated install.html: clone URL → konradsebastian/dev_er3t_edu, all paths → dev_er3t_edu/er3t/
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
- **verify_install.py passed** on real er3t env; conda env confirmed → dev_er3t_edu/er3t/
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

### Sessions 15–16 (2026-07-02 — repo restructuring + teaching branch prep)

**Repo restructuring:**
- Hong Chen confirmed preference for a **teaching branch on his repo** over a fork under konradsebastian
- Deactivated `er3t/` subdirectory in dev_er3t_edu:
  - `git rm --cached -r er3t/` (files kept on disk for local testing)
  - Added `er3t/` and `teaching-branch-setup/*.patch` to `.gitignore`
  - Committed and pushed to konradsebastian/dev_er3t_edu

**Teaching branch preparation** (`dev_er3t_edu`):
- Cloned `hong-chen/er3t` at `release/v0.2.0-alpha.1` locally at `/tmp/hong-chen-er3t`
- Applied two commits on top of the release branch:
  1. **Security commit** (`a34e082`): surgical fix to remove hardcoded credentials only
     - `er3t/util/daac.py` line 68: JWT token → `EARTHDATA_TOKEN` env var + warning message
     - `er3t/util/util.py` lines 159-160: SMTP credentials → `ER3T_SENDER_EMAIL` / `ER3T_SENDER_PASSWORD` env vars
     - Deliberately did NOT apply other diffs (pysolar removal, etc.) to keep Hong's code clean
  2. **Teaching examples commit** (`4110f5a`): added full examples suite
     - `examples/01_clear_sky_flux.py` through `06_generated_cloud_radiance.py`
     - `examples/verify_install.py`
     - `examples/install-examples.sh`
- Generated patch files: `0001-security-*.patch` and `0002-teaching-*.patch`
- Created `push_teaching_branch.sh` (in `teaching-branch-setup/`):
  re-clones hong-chen/er3t from scratch, applies both patches, pushes the branch
- **Push attempt**: Failed with 403 — konradsebastian does not have push access to hong-chen/er3t
- **Email sent to Hong Chen (2026-07-02)**: requesting collaborator access to hong-chen/er3t
  (to push `dev_er3t_edu` branch)

**install.html updated:**
- Step 1 clone URL changed from `konradsebastian/dev_er3t_edu` → `hong-chen/er3t -b dev_er3t_edu`
- All path references updated: `$ERTDIR/dev_er3t_edu/er3t` → `$ERTDIR/er3t` throughout
- Footer GitHub link updated
- Placeholder callout added to Step 1: "URL update in progress — pending collaborator access"

**Analysis of 02_modis_rad-sim.py (future Example 07):**
- Full analysis of Hong Chen's 1775-line MODIS radiance simulation script
- Key finding: `sys.exit()` at line 1448 inside `cal_mca_rad()` causes simulation to always abort — must be removed
- Teaching adaptation plan finalized (see Future Examples section below)
- Development flagged for post-summer-school (not needed for Jul 11)

### Sessions 17–18 (2026-07-06/07 — summer school bug triage + example 06/07 docs)

**Student bug triage:**
- Student report: `tests/00_test_util.py` broken — `download_worldview_rgb` renamed to
  `download_worldview_image` upstream. Fixed in `er3t-dev`, mirrored + verified in the
  `test-install2` smoke-test clone before landing, then committed and pushed to
  `hong-chen/er3t` (`dev_er3t_edu`) as commit `91970df`.
- Student report: `tests/03_test_cld.py` MODIS download failure — traced to an Earthdata
  token/auth issue (635-byte "successful" download was actually an auth error page);
  student resolved on their own.
- Same commit also picked up several pre-existing uncommitted fixes: numpy 2.0 dtype
  deprecations (`np.int_`/`np.float_` → `np.int64`/`np.float64`), `os.system()` →
  `subprocess.run(shlex.split(...))` in `mca_run.py`, and curl/wget retry/timeout increases
  in `daac.py`.

**Website docs:**
- Discovered examples 06 (`06_modis_data_download.py`) and 07 (`07_modis_radiance.py`) had
  been committed to `er3t-dev` but never documented on the website.
- Added full write-ups of both to `docs/examples.html`; updated "five examples" → "seven
  examples" language in `install.html`, `science.html`, `index.html`. Committed to
  `konradsebastian/er3t-edu` as `b8a30c0`.

**Roadmap correction:**
- Verified via `git ls-remote --heads` against `hong-chen/er3t` that the teaching branch is,
  and has only ever been, `dev_er3t_edu` — not `teaching/summer-school-2026` as an earlier
  draft of this document claimed. `install.html` was already correct throughout; only this
  file needed fixing. See Repository Strategy section above for the corrected record.

---

## Pending Actions (in priority order)

### ✅ ~~1. Run verify_install.py end-to-end~~ — DONE (2026-07-01)
All checks passed. Conda env confirmed pointing to `dev_er3t_edu/er3t/er3t/__init__.py`.
abs_16g shows `—` (expected skip). MCARaTS, REPTRAN, Mie phase functions all ✓.

### ✅ ~~2. Add verify_install.py step to install.html~~ — DONE (2026-07-01)
Added as Step 5 in install.html.

### ✅ ~~3. Push teaching branch to hong-chen/er3t~~ — DONE (2026-07-03)
Branch `dev_er3t_edu` pushed and live (note: an earlier version of this roadmap incorrectly
called this branch `teaching/summer-school-2026` — corrected 2026-07-07, see Repository
Strategy above). Placeholder callout removed from install.html.

### ✅ ~~4. Full student journey test~~ — DONE (2026-07-03, re-verified 2026-07-06/07)
Cloned from `dev_er3t_edu` into the `test-install2` smoke-test clone, followed install.html
end-to-end, ran `verify_install.py` + example scripts. All passed, including a re-test after
the `download_worldview_rgb` → `download_worldview_image` fix (see Session 17).

### ✅ ~~5. Remove placeholder callout from install.html~~ — DONE (2026-07-03)

### ~~6. Obtain abs_16g.h5~~ — NOT NEEDED
Confirmed 2026-07-03: Example 07 (MODIS radiance sim) uses `abs_rep`, not `abs_16g`.
`abs_16g.h5` is not required for any planned teaching example.

### ✅ ~~7. Earthdata credentials — document for students~~ — DONE (2026-07-03)
Prerequisite instructions added to install.html (Earthdata account, token generation,
`export EARTHDATA_TOKEN`). No credentials needed for examples 01–06 or verify_install.py.

### 8. Public/private repo hygiene [post-summer-school]
ROADMAP.md and internal files are publicly visible in the repo. Options:
- Move to a separate private companion repo (cleanest)
- Move to a non-default branch
Not a blocker now; students are unlikely to look, content is not sensitive.

---

## Future Examples (post-summer-school, needs student coordination)

**Numbering note**: Examples 06 (`06_modis_data_download.py`) and 07 (`07_modis_radiance.py`)
are now both written, committed, and documented on the website (2026-07-07) — see Example
Scripts table above. They superseded the earlier synthetic-cloud-generator draft of 06.

### Example 07: MODIS Radiance Self-Consistency — ✅ DONE (2026-07-07)

Reproduces Appendix 2 of Chen et al. (2023) — a validation that er3t can simulate the radiance
a satellite actually measured, given the retrieved cloud state. Final output: 4-panel figure
(MODIS measured, EaR³T simulated, density scatter, MC noise map).

Prerequisites for students: Earthdata account + NASA LAADS token (see Pending Action #7).

**Starting point was**: `projects/02_modis_rad-sim.py` on `hong-chen/er3t` branch
`release/v0.2.0-alpha.1` (1775 lines, analyzed 2026-07-02) — adapted down into the current
`06_modis_data_download.py` (pre-processing) + `07_modis_radiance.py` (simulation + comparison) pair.

**Website documentation**: Added to `docs/examples.html`, with cross-references from
`install.html` and `science.html` (2026-07-07).

**Coordination**: Vikas may have more advanced download/processing code — contact him if
students want to go further than examples 06/07.

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

*Last updated: 2026-07-07 (session 18)*
