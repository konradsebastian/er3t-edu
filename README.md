# er3t-edu — EaR³T Education Repository

Teaching materials, student projects, and the summer school website for the
**Education and Research 3D Radiative Transfer Toolbox (EaR³T)**.

---

## What's Here

| Folder | Contents |
|---|---|
| `docs/` | GitHub Pages website (Science · Installation · Projects) |
| `notebooks/` | Jupyter notebook starters for student projects |
| `scripts/` | Verification scripts, helper utilities, YAML driver examples |
| `ROADMAP.md` | Development vision, task plan, and open questions |

## The EaR³T Package

The EaR³T Python package itself lives at: https://github.com/hong-chen/er3t

Install it via:
```bash
git clone https://github.com/hong-chen/er3t.git
cd er3t
conda env create -f er3t-env.yml
conda activate er3t
pip install -e .
```

## Website

The summer school / course website is served from `docs/` via GitHub Pages.

## License

Teaching materials in this repo: CC BY 4.0.
EaR³T package: GPL-3.0 (see upstream repo).
