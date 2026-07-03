# EaR³T Education & Research — Project Roadmap
*K. Sebastian Schmidt · University of Colorado Boulder / LASP*
*Started: 2026-06-25 · Last updated: 2026-07-02 (session 16)*

---

## Vision

Build a GitHub Pages website for teaching and summer school use centered on EaR³T (Education and Research 3D Radiative Transfer Toolbox), developed in the Schmidt lab at CU Boulder. The site serves as the home base for students to install the tool and work through examples that take them from the 1D view of the world to a 3D-aware one.

Two audiences:
- **Summer school participants** (immediate need: 1.5-hr slot + pre-school office hours)
- **Courses at CU Boulder** (future expansion)

Core pedagogical arc: *Why does 3D matter? → How do we model it? → Do it yourself.*

---

## Repository Strategy (UPDATED 2026-07-02)

### Two-repo architecture (transitioning)

| Repo | Purpose | Status |
|---|---|---|
| `konradsebastian/dev_er3t_edu` | Website, data, roadmap | ✅ active |
| `hong-chen/er3t` branch `dev_er3t_edu` | All er3t code + teaching examples | ⏳ pending push |

**Rationale**: Hong Chen (er3t upstream maintainer) prefers a dedicated teaching branch
on his own repo over a fork under a different GitHub account. This avoids divergence and
keeps the code lineage clear. We agreed on this after initial communication (2026-07-02).

**`er3t/` subdirectory in dev_er3t_edu**: Deactivated as of 2026-07-02.
- Removed from git tracking via `git rm --cached er3t/` (files kept on disk for local testing)
- Added `er3t/` to `.gitignore`
- install.html updated with placeholder notice — does NOT point to the deactivated er3t/

**Teaching branch** (`dev_er3t_edu`):
- Based on `release/v0.2.0-alpha.1` (Hong's current Libera flavor — NOT master, which is outdated)
- Two commits prepared as patches in `teaching-branch-setup/`:
  1. Security fix: remove hardcoded credentials (daac.py + util.py)
  2. Teaching examples: add 01–06, verify_install.py, install-examples.sh
- Push script ready: `teaching-branch-setup/push_teaching_branch.sh`
- **Blocked on**: collaborator access from Hong Chen (email sent 2026-07-02)

**Students will install with** (once teaching branch is live):
```bash
git clone -b dev_er3t_edu https://github.com/hong-chen/er3t.git
cd er3t
pip install -e .
```

**Upstream branch note**: The `master` branch of `hong-chen/er3t` is outdated. Always use
`release/v0.2.0-alpha.1` as the base. Our teaching patches were built on this branch.

**Fallback** (if Hong Chen does not grant access in time): create a formal fork at
`konradsebastian/er3t` and redirect the push script to that remote. The patches apply cleanly
either way. Long-term, we still want option B (branch on hong-chen/er3t).

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

All scripts live in `dev_er3t_edu/er3t/examples/`. Summer school (July 11) covers examples 01–05.
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

Hosted at: https://konradsebastian.github.io/dev_er3t_edu/install.html

Current state:
- ✅ Full installation walkthrough (conda env, MCARaTS compile, er3t install)
- ✅ Examples 01–05 described with expected outputs and what to look for
- ✅ Example 06 not in summer school curriculum (available for self-study)
- ✅ Clone URL updated to `hong-chen/er3t` teaching branch (updated 2026-07-02)
- ✅ All path references updated: `$ERTDIR/er3t/` throughout (no more `dev_er3t_edu/er3t/`)
- ✅ Core data download step present (install.sh downloads REPTRAN + core data)
- ✅ install-examples.sh downloads les.nc only (not redundant with install.sh)
- ✅ Step 5 verify_install.py section with expected output
- ⚠️ Placeholder callout box in Step 1: "Repository URL update in progress — pending Hong Chen push access"

**Action required after Hong Chen grants access**:
Remove placeholder callout box from Step 1. The clone URL and path instructions are already
correct — only the callout text needs to come out.

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

---

## Pending Actions (in priority order)

### ✅ ~~1. Run verify_install.py end-to-end~~ — DONE (2026-07-01)
All checks passed. Conda env confirmed pointing to `dev_er3t_edu/er3t/er3t/__init__.py`.
abs_16g shows `—` (expected skip). MCARaTS, REPTRAN, Mie phase functions all ✓.

### ✅ ~~2. Add verify_install.py step to install.html~~ — DONE (2026-07-01)
Added as Step 5 in install.html.

### 3. ⚠️ Wait for Hong Chen response [deadline: ASAP — Jul 5 hard stop]
Email sent 2026-07-02 requesting collaborator access to hong-chen/er3t.
Two options depending on reply:

**Option B (preferred): Hong Chen grants collaborator access**
```bash
cd ~/projects/dev_er3t_edu/teaching-branch-setup
bash push_teaching_branch.sh   # clones, applies patches, pushes
```
Then: remove placeholder callout from install.html Step 1, commit + push dev_er3t_edu.

**Option A (fallback if no reply by ~Jul 4)**: Create formal fork
```bash
# fork hong-chen/er3t on GitHub under konradsebastian account
# then edit push_teaching_branch.sh: change git push origin → git push fork
bash push_teaching_branch.sh
```
install.html clone URL would become `konradsebastian/er3t` (update accordingly).
Long-term intention remains Option B.

### 4. ⚠️ URGENT: Full student journey test [deadline July 5]
**Prerequisite**: teaching branch must be live (see item 3 above).
Clone fresh from final code location and follow install.html start to finish:
```bash
git clone -b dev_er3t_edu https://github.com/hong-chen/er3t.git test-install2
# (or konradsebastian/er3t if using fallback fork)
cd test-install2
conda env create -f er3t-env.yml
conda activate er3t
pip install -e .
bash install.sh
cd examples
bash install-examples.sh
python verify_install.py
python 01_clear_sky_flux.py
```
Note any issues → fix and push before Jul 5.

**Local testing (interim, while waiting for Hong Chen)**:
✅ Examples 01–05 confirmed passing locally against `release/v0.2.0-alpha.1` (2026-07-02).
Can test from local clone at `/tmp/hong-chen-er3t`.

### 5. Remove placeholder callout from install.html [after teaching branch is live]
After push succeeds (Option B or A), remove the "URL update in progress" callout box
from Step 1 of docs/install.html. The clone URL and path instructions are already correct.

### 6. Obtain abs_16g.h5 [post-summer-school]
`abs_16g.h5` is not in the current teaching data package. The abs_16g absorption module
is non-functional. Not needed for examples 01–06 but needed for Example 07 (MODIS sim).
Action: ask Hong Chen where this file comes from / how to regenerate it.

### 7. Earthdata credentials — document for students [before Example 07]
No credentials needed for examples 01–06 or verify_install.py.
Example 07 (MODIS radiance simulation) requires a NASA Earthdata token.
When Example 07 is developed, add a prerequisite step to install.html:
  - Create Earthdata account at https://urs.earthdata.nasa.gov
  - Generate token at https://ladsweb.modaps.eosdis.nasa.gov/
  - Add to shell rc: `export EARTHDATA_TOKEN="<your-token-here>"`

### 8. Public/private repo hygiene [post-summer-school]
ROADMAP.md and internal files are publicly visible in the repo. Options:
- Move to a separate private companion repo (cleanest)
- Move to a non-default branch
Not a blocker now; students are unlikely to look, content is not sensitive.

---

## Future Examples (post-summer-school, needs student coordination)

**Numbering note**: Example 06 (`06_generated_cloud_radiance.py`) already exists as a
synthetic cloud generator. The future satellite examples are numbered 07 and 08.

### Example 07: MODIS Radiance Self-Consistency (NOT YET WRITTEN — flagged for post-summer-school)

Reproduces Appendix 2 of Chen et al. — a validation that er3t can simulate the radiance
a satellite actually measured, given the retrieved cloud state. Final output: 2D maps of
observed vs. simulated MODIS Band 1 reflectance + scatter plot.

Prerequisites for students: Earthdata account + NASA LAADS token (see Pending Action #7).

**Starting point**: `projects/02_modis_rad-sim.py` on `hong-chen/er3t` branch `release/v0.2.0-alpha.1`
(1775 lines, fully analyzed 2026-07-02)
https://github.com/hong-chen/er3t/blob/release/v0.2.0-alpha.1/projects/02_modis_rad-sim.py

**Simplifications required to produce `07_modis_radiance.py`**:
1. Remove `sys.exit()` at line 1448 inside `cal_mca_rad()` — this bug causes simulation to abort
2. Skip IPA COT retrieval pipeline (~300 lines) — use MODIS L2 COT directly instead
3. Skip parallax correction pipeline (~80 lines) — acceptable for teaching purposes
4. Swap `abs_rep` → `abs_16g` for gas absorption (requires `abs_16g.h5` — see Pending Action #6)
5. Reduce photon count: 1e8 → 5e5–1e6 (runtime from hours to minutes)
6. Pre-supply `pre-data.h5` (intermediate processed data) to skip downloads for students
   — students may optionally generate it themselves with `EARTHDATA_TOKEN` set
7. Reference Appendix 2 figure from Chen et al. on website so students can cross-check output

**Website documentation**: Add example 07 to install.html examples section once script is ready.
Point to the Appendix 2 figure in the paper for cross-check.

**Coordination**: Vikas may have more advanced download/processing code — contact him.

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

*Last updated: 2026-07-02 (session 16)*
