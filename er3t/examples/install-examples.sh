#!/usr/bin/env bash
# Download auxiliary data for er3t example scripts.
# Run from the er3t/examples/ directory.
#
# Data sources (Schmidt Lab Google Drive — not rate-limited by course traffic):
#   er3t core data tarball  — REPTRAN gas absorption database + auxiliary files
#   les.nc                  — LES cloud field used in examples 02–05
#
# Previous Google Drive IDs (Hong Chen's, archived):
#   les.nc core: 1Oov75VffmuQSljxjoOS6q6egmfT6CmkI

# ── Google Drive file IDs ─────────────────────────────────────────────────────
CORE_GDRIVE_ID="15YymaUt1i3ad45OZI4kXFDZZlxCNVuGU"
CORE_TARBALL="/tmp/er3t-data.tar.gz"
CORE_DEST=".."                    # unpacked relative to examples/ → goes into er3t/data/

LES_GDRIVE_ID="1cmrZDaCwoQNhaoPGhJ9OhSVEpDU9h-gg"
LES_DEST="data/00_er3t_mca/aux/les.nc"
# ─────────────────────────────────────────────────────────────────────────────

echo "╭────────────────────────────────────────────────╮"
echo "      EaR³T — Example Auxiliary Data Install      "
echo "╰────────────────────────────────────────────────╯"
echo

# Check for gdown
if ! command -v gdown &> /dev/null; then
    echo "[Error] 'gdown' is required to download from Google Drive."
    echo "  Install: pip install gdown"
    echo "  (It is included in the er3t conda environment.)"
    exit 1
fi

# ── Step 1: er3t core data (REPTRAN + auxiliary files) ───────────────────────
echo "<1> Downloading er3t core data (~180 MB) ..."
echo "  Source : Google Drive (Schmidt Lab, ID: $CORE_GDRIVE_ID)"
echo "  Target : er3t/data/"
echo

gdown "$CORE_GDRIVE_ID" --output "$CORE_TARBALL"

if [ ! -f "$CORE_TARBALL" ]; then
    echo "[Error] Core data download failed."
    exit 1
fi

echo "Extracting core data ..."
tar -xzf "$CORE_TARBALL" -C "$CORE_DEST"
rm -f "$CORE_TARBALL"
echo "Core data installed."
echo

# ── Step 2: LES cloud field ───────────────────────────────────────────────────
echo "<2> Downloading LES cloud field (les.nc, ~209 MB) ..."
echo "  Source : Google Drive (Schmidt Lab, ID: $LES_GDRIVE_ID)"
echo "  Target : $LES_DEST"
echo

mkdir -p "$(dirname "$LES_DEST")"
gdown "$LES_GDRIVE_ID" --output "$LES_DEST"

if [ ! -f "$LES_DEST" ]; then
    echo "[Error] LES download failed — '$LES_DEST' not found."
    exit 1
fi
echo "LES cloud field installed."
echo

echo "╭────────────────────────────────────────────────╮"
echo "  All example data installed. Ready to run.       "
echo "╰────────────────────────────────────────────────╯"
