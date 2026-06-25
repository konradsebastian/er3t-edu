# EaR³T Education & Research — Project Roadmap
*K. Sebastian Schmidt · University of Colorado Boulder / LASP*
*Started: 2026-06-25*

---

## Vision

Build a GitHub Pages website for teaching and summer school use centered on EaR³T (Education and Research 3D Radiative Transfer Toolbox), developed in the Schmidt lab at CU Boulder over the past ~10 years. The site serves as the home base for students to understand the scientific motivation, install the tool, and work through projects that take them from the 1D view of the world to a 3D-aware one.

The website will serve two audiences:
- **Summer school participants** (immediate need: 1.5-hr slot + pre-school office hours)
- **Courses at CU Boulder** (future expansion: ATOC courses on radiative transfer and remote sensing)

The core pedagogical arc: *Why does 3D matter? → How do we model it? → Do it yourself.*

---

## EaR³T: What It Is and Why It Matters

### What EaR³T does

EaR³T is a modularized Python package that automates end-to-end 3D radiative transfer (RT) calculations. It:
- Downloads and pre-processes satellite data (MODIS, VIIRS, OCO-2, AHI, Worldview, LAADS DAAC, GES DISC)
- Sets up atmospheric optical properties (gases via correlated-k / REPTRAN, clouds via Mie theory, surface via Cox-Munk / LSRT)
- Runs RT simulations through pluggable solvers: **MCARaTS** (3D Monte Carlo), **libRadtran** (1D, benchmark), **SHDOM** (planned)
- Outputs radiance and irradiance fields in HDF5 format for analysis and closure studies

It is benchmarked against libRadtran, which is itself one of the most widely used 1D RT packages in atmospheric science.

GitHub: https://github.com/hong-chen/er3t  
Docs: https://er3t.readthedocs.io  
DOI: https://doi.org/10.5194/amt-16-1971-2023

### The core science problem

Conventional satellite cloud retrievals use 1D (independent pixel approximation, IPA) radiative transfer — treating each pixel as a horizontally infinite, homogeneous column. Nature is not 1D. In real, spatially inhomogeneous cloud fields, photons scatter horizontally between columns (net horizontal photon transport), creating 3D-RT effects that bias retrieved cloud properties and derived irradiances.

**EaR³T's approach**: Use 3D-RT to simulate what the satellite *should* have observed given the retrieved cloud field (radiance self-consistency / closure). Inconsistency between simulated and measured radiances reveals and quantifies the 3D bias.

---

## Applications Summary (from peer-reviewed papers)

### Core paper
**Chen et al. (2023)** — *The Education and Research 3D Radiative Transfer Toolbox (EaR³T)* — AMT 16, 1971–2000. DOI: 10.5194/amt-16-1971-2023

Four application blueprints:
1. **OCO-2 radiance closure** — 3D-RT simulation of OCO-2 radiances from MODIS cloud products; demonstrates 3D-induced radiance inconsistency over inhomogeneous cloud scenes (SW Colorado).
2. **MODIS radiance closure** — Self-consistency test of MODIS L2 cloud products using 3D-RT; shows IPA COT low bias due to horizontal photon transport.
3. **CAMP²Ex irradiance closure** — Geostationary AHI cloud products → simulated irradiance along *all* CAMP²Ex aircraft flight legs → comparison with SP-NS airborne measurements. Finds 10% low bias in satellite-derived cloud transmittance attributable to coarse GEO resolution + 3D effects.
4. **CNN cloud retrieval + radiance closure** — Applies a CNN (trained on LES-derived 3D-RT synthetic data) to high-resolution CAMP²Ex camera imagery; CNN-based COT retrievals yield better 3D radiance consistency than IPA, demonstrating bias mitigation.

### Application papers

**Nataraja et al. (2022)** — *Segmentation-based multi-pixel COT retrieval using CNN* — AMT 15, 5181. DOI: 10.5194/amt-15-5181-2022  
→ **Application type: ML synthetic data generation**  
EaR³T + MCARaTS generates 3D-RT radiance fields from LES cloud scenes to train a U-Net CNN that corrects IPA bias in COT retrievals. Demonstrates that accounting for spatial context via CNN substantially outperforms IPA across all cloud morphologies (stratocumulus through cumulus).

**Yu-Wen Chen et al. (2024, preprint)** — *Mitigation of OCO-2 CO2 biases near clouds using EaR3T* — EGUsphere 2024-1936 (in review at AMT)  
→ **Application type: Trace-gas retrieval bias correction**  
EaR3T-OCO extension uses MCARaTS to compute 3D-RT spectral perturbations on OCO-2 radiances from nearby clouds. Linear approximation (slope + intercept per band) gives ~100× speedup. Physics-based pre-correction of OCO-2 spectra reduces XCO2 biases from >2 ppm (footprint) to <0.7 ppm (regional), constituting the first physics-based 3D-RT correction for OCO-2/3.

**Gristey et al. (2020)** — GRL DOI: 10.1029/2020GL090152  
→ **Application type: Surface irradiance from satellite imagery** (full abstract not retrieved — JS-rendered page; to be confirmed)

**Chen et al. (2022)** — JGR-Atmos DOI: 10.1029/2022JD036822  
→ **Application type: EaR³T toolbox / radiance simulator** (full abstract not retrieved — JS-rendered page; to be confirmed)

### Application taxonomy (for intro talk)

| Theme | Representative paper | Key message |
|---|---|---|
| Radiance closure / 3D bias quantification | Chen et al. 2023 (App. 1, 2) | 1D retrievals are inconsistent with 3D reality; closure reveals the gap |
| Irradiance closure / campaign-scale validation | Chen et al. 2023 (App. 3) | EaR³T enables systematic (not case-study) closure across entire field campaigns |
| ML synthetic data generation | Nataraja et al. 2022; Chen et al. 2023 (App. 4, 5) | 3D-RT is the engine behind next-gen ML cloud retrievals |
| Trace-gas retrieval bias mitigation | Yu-Wen Chen et al. 2024 | 3D cloud effects contaminate CO₂ retrievals; 3D-RT corrections are tractable |
| Surface irradiance from imagery | Gristey et al. 2020 | (to be confirmed) |

---

## Website Structure

### Section 1: Science Introduction and Context
- What is radiative transfer? (1D baseline: libradtran)
- Why does 3D matter? (IPA bias, horizontal photon transport, cloud inhomogeneity)
- The EaR³T approach: from imagery to 3D-RT to closure
- Applications overview (linked to papers, summary figures)
- **Slides**: 1.5-hr summer school talk (to be uploaded as PDF/HTML)
- **References**: all papers

### Section 2: Installation Guide
- System requirements and dependencies
- **EaR³T** (Python package, GitHub)
- **MCARaTS** (Fortran, 3D Monte Carlo solver) — with compiled binaries if feasible
- **SHDOM** (Fortran, deterministic 3D solver) — optional
- **libRadtran** (1D benchmark solver)
- **Data packages**: REPTRAN, ic_yang2013, optprop (for libRadtran), etc.
- **Conda environment** setup (`er3t-env.yml`)
- **Verification script**: `check_installation.py` — runs a minimal end-to-end test confirming all solvers work
- CU Research Computing / SLURM setup (for students on Alpine)

### Section 3: Projects / Homework

#### Project A: Polar satellite data → surface irradiance (Arctic case)
Use MODIS/VIIRS imagery over NW Greenland (Pituffik/Thule area) from a specific overpass to predict downwelling shortwave irradiance at the surface. Compare against surface radiometer observations (e.g., GEOS network or ARCSIX ground station). Quantify 1D vs. 3D difference.

#### Project B: Geostationary/polar imagery → aircraft irradiance along flight track
Use AHI or MODIS cloud products to simulate irradiance along an aircraft flight track (e.g., CAMP²Ex or ARCSIX). Compare with SP-NS or pyranometer measurements. Identify segments where 3D bias is largest and explain why.

#### Project C: Radiance closure (WorldView + MODIS)
Use a configurable cloud scene from NASA WorldView as starting point. Run 1D IPA retrieval → get COT field → run 3D-RT → compare simulated radiance to original measurement. Identify inconsistency. Then: estimate what bias in surface irradiance the COT bias causes. Advanced variant: apply CNN retrieval and compare closure metrics.

#### Project D: Sub-pixel inhomogeneity (spectral)
Simulate a partially cloud-filled pixel (cloud under-filling an imager resolution element). Show what a 1D retrieval returns (effective OT, no skill on cloud fraction). Then explore whether spectral information (multi-channel reflectance) can help disentangle sub-pixel cloud fraction from optical thickness. Ranges from simple (homogeneous stratus → stratocumulus → cumulus) to research-grade.

#### Project E (research-track): Spectral information content for vertical cloud structure
Based on Buggee et al. (passive shortwave cloud vertical structure retrievals): simulate 3D LES cloud scenes → 1D synthetic reflectance spectra → check whether 3D perturbations reduce spectral information content. Compare across cloud scene types (stratus, Sc, Cu).

---

## GitHub / Repository Strategy

**Options:**
1. **Fork `hong-chen/er3t`** into `kss-schmidt/er3t` (or the Schmidt lab GitHub org), add a `summer-school` branch with teaching materials, verification scripts, and simplified examples.
2. **Separate repo** `kss-schmidt/eart-edu` housing only the website + student-facing materials, linking back to the main `er3t` repo for the package itself.
3. **GitHub Pages site** hosted on a dedicated repo (e.g., `eart3d.github.io` or `kss-schmidt.github.io/eart-edu`).

**Recommendation**: Option 2 + 3 combined. Keep the EaR³T package repo clean (and defer to Hong Chen's upstream); create a separate teaching repo that provides the website, student notebooks, verification scripts, and project starter code. This avoids merge complexity with the research codebase.

**Actions needed:**
- [ ] Decide on GitHub org / username for hosting
- [ ] Create `eart-edu` repo (or equivalent name)
- [ ] Enable GitHub Pages on that repo
- [ ] Set up `er3t-env.yml` verified against current EaR³T version
- [ ] Walk through full installation chain to verify and document any bugs

---

## Multi-Day Work Plan (1-hour increments)

### Session 1 — 2026-06-25 (today, ~1h15m)
- [x] Analyze EaR³T papers and extract application summary ✅
- [x] Create `ert.edu` project folder and this ROADMAP ✅
- [ ] Set up website skeleton (HTML/CSS, three sections, navigation)
- [ ] Draft Section 1 science intro text (hook + 1D/3D motivation)

### Session 2 — next available slot
- [ ] Walk through EaR³T installation from scratch (fresh conda env)
- [ ] Document any issues / version conflicts encountered
- [ ] Test MCARaTS compile (on local machine or Alpine)
- [ ] Draft Section 2 installation guide (based on tested steps)

### Session 3
- [ ] Walk through libRadtran installation and verify er3t linkage
- [ ] Run `examples/00_er3t_mca.py` and `00_er3t_lrt.py` end-to-end
- [ ] Write verification script (`check_installation.py`)
- [ ] Populate Section 2 with tested instructions

### Session 4
- [ ] Run `examples/03_spns_flux-sim.py` (CAMP²Ex irradiance closure)
- [ ] Adapt into Project B student notebook (simplified, guided)
- [ ] Identify data dependencies; check what is auto-downloaded vs. needs pre-staging

### Session 5
- [ ] Run `examples/01_oco2_rad-sim.py` or `02_modis_rad-sim.py`
- [ ] Draft Project C (radiance closure / WorldView) notebook skeleton
- [ ] Identify Arctic / Pituffik data availability for Project A

### Session 6
- [ ] Draft Project A (Arctic surface irradiance) notebook
- [ ] Draft Project D (sub-pixel inhomogeneity) outline
- [ ] Begin Section 3 project page on website

### Session 7
- [ ] Polish website: science intro, figures, paper links
- [ ] Upload / link summer school slides (PDF)
- [ ] Final review of installation instructions
- [ ] Test student journey end-to-end (install → verify → run one project)

### Session 8
- [ ] Buffer: fix bugs found in Session 7
- [ ] Set up GitHub repo and GitHub Pages deployment
- [ ] Share website URL with summer school organizers

---

## Open Questions / Decisions Needed

- Which GitHub account/org hosts the teaching repo?
- Which data sources are available for the Arctic (Pituffik) project? (ARCSIX observations?)
- Is SHDOM needed for any of the student projects, or is MCARaTS sufficient?
- What is the summer school date / how much lead time for pre-installation office hours?
- Should student projects be Jupyter notebooks or standalone Python scripts? (Notebooks preferred for teaching.)
- What compute resources do students have? (Laptops + Alpine? Just laptops?)

---

*Last updated: 2026-06-25*
