#!/usr/bin/env python3
"""
parse_worldview.py — EaR³T scene configuration helper

Parses a NASA WorldView GeoTIFF snapshot (and optionally the browser URL)
to auto-generate an er3t scene YAML configuration file.

Usage:
    python parse_worldview.py --tif snapshot.tif [--url "<worldview_url>"] [--out scene.yml]

Example WorldView URL (copy from browser address bar after framing your scene):
    https://worldview.earthdata.nasa.gov/?v=-10,45,30,70&l=MODIS_Terra_CorrectedReflectance_TrueColor&t=2026-06-24

The GeoTIFF provides: bounding box, resolution, date (from filename).
The URL provides:      layer name → sensor/instrument identity.

If no URL is given, sensor is inferred from resolution (approximate).

Output is a YAML file that can be passed directly to er3t run scripts.
"""

import argparse
import os
import re
import sys
import yaml
from datetime import datetime, timezone

try:
    import rasterio
except ImportError:
    sys.exit("ERROR: rasterio is required. Install with: pip install rasterio")


# ── WorldView layer name → sensor/product mapping ─────────────────────────────

LAYER_MAP = {
    # MODIS
    'MODIS_Terra_CorrectedReflectance_TrueColor':     {'satellite': 'Terra',    'sensor': 'MODIS', 'collection': 'MYD03/MOD03', 'res_m': 500},
    'MODIS_Terra_CorrectedReflectance_Bands721':       {'satellite': 'Terra',    'sensor': 'MODIS', 'collection': 'MOD021KM',    'res_m': 1000},
    'MODIS_Aqua_CorrectedReflectance_TrueColor':      {'satellite': 'Aqua',     'sensor': 'MODIS', 'collection': 'MYD021KM',    'res_m': 500},
    'MODIS_Aqua_CorrectedReflectance_Bands721':        {'satellite': 'Aqua',     'sensor': 'MODIS', 'collection': 'MYD021KM',    'res_m': 1000},
    # VIIRS
    'VIIRS_SNPP_CorrectedReflectance_TrueColor':      {'satellite': 'Suomi-NPP','sensor': 'VIIRS', 'collection': 'VNP02MOD',    'res_m': 375},
    'VIIRS_NOAA20_CorrectedReflectance_TrueColor':    {'satellite': 'NOAA-20',  'sensor': 'VIIRS', 'collection': 'VJ102MOD',    'res_m': 375},
    'VIIRS_NOAA21_CorrectedReflectance_TrueColor':    {'satellite': 'NOAA-21',  'sensor': 'VIIRS', 'collection': 'VJ202MOD',    'res_m': 375},
    # Landsat
    'Landsat_8_OLI_TrueColor':                        {'satellite': 'Landsat-8','sensor': 'OLI',   'collection': 'LC08',         'res_m': 30},
    'Landsat_9_OLI_TrueColor':                        {'satellite': 'Landsat-9','sensor': 'OLI',   'collection': 'LC09',         'res_m': 30},
}

# Sensor guess from pixel resolution when no URL is provided
RES_SENSOR_GUESS = [
    (50,   {'satellite': 'Landsat',    'sensor': 'OLI',   'note': 'inferred from ~30m res'}),
    (300,  {'satellite': 'Suomi-NPP or NOAA-20', 'sensor': 'VIIRS', 'note': 'inferred from ~375m res'}),
    (600,  {'satellite': 'Terra or Aqua', 'sensor': 'MODIS', 'note': 'inferred from ~500m res'}),
    (1200, {'satellite': 'Terra or Aqua', 'sensor': 'MODIS', 'note': 'inferred from ~1km res'}),
    (9999, {'satellite': 'unknown',    'sensor': 'unknown', 'note': 'resolution too coarse to identify'}),
]


def parse_date_from_filename(fname):
    """Extract ISO date from WorldView snapshot filename."""
    m = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(fname))
    if m:
        return m.group(1)
    m = re.search(r'(\d{8})', os.path.basename(fname))
    if m:
        d = m.group(1)
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    return None


def parse_worldview_url(url):
    """
    Extract layer name, date, and viewport from a WorldView browser URL.

    Example URL:
      https://worldview.earthdata.nasa.gov/?v=-10,45,30,70&l=MODIS_Terra_CorrectedReflectance_TrueColor&t=2026-06-24
    """
    info = {}

    # Date from &t= parameter
    m = re.search(r'[?&]t=(\d{4}-\d{2}-\d{2})', url)
    if m:
        info['date'] = m.group(1)

    # Layer name from &l= parameter (first layer listed)
    m = re.search(r'[?&]l=([^&]+)', url)
    if m:
        layers_raw = m.group(1)
        # Layers can be comma-separated; take the first visible/base layer
        layers = [l.strip() for l in layers_raw.split(',') if l.strip()]
        # Prefer the first layer that's in our map; otherwise first layer
        info['layer_raw'] = layers
        for layer in layers:
            if layer in LAYER_MAP:
                info['layer'] = layer
                info.update(LAYER_MAP[layer])
                break
        if 'layer' not in info and layers:
            info['layer'] = layers[0]

    # Viewport from &v= parameter (lon_min,lat_min,lon_max,lat_max)
    m = re.search(r'[?&]v=([^&]+)', url)
    if m:
        try:
            parts = [float(x) for x in m.group(1).split(',')]
            if len(parts) == 4:
                info['viewport'] = {
                    'lon': [parts[0], parts[2]],
                    'lat': [parts[1], parts[3]],
                }
        except ValueError:
            pass

    return info


def guess_sensor_from_res(res_m):
    for threshold, sensor_info in RES_SENSOR_GUESS:
        if res_m < threshold:
            return sensor_info
    return RES_SENSOR_GUESS[-1][1]


def parse_geotiff(tif_path):
    """Extract spatial metadata from a WorldView GeoTIFF snapshot."""
    with rasterio.open(tif_path) as ds:
        b = ds.bounds
        res_deg = ds.res[0]
        res_m = res_deg * 111_000  # approximate, good enough for sensor ID

        return {
            'lon_min': round(b.left,  6),
            'lon_max': round(b.right, 6),
            'lat_min': round(b.bottom, 6),
            'lat_max': round(b.top,   6),
            'width_px':  ds.width,
            'height_px': ds.height,
            'bands':     ds.count,
            'crs':       str(ds.crs),
            'res_deg':   round(res_deg, 8),
            'res_m':     round(res_m, 0),
        }


def build_yaml(tif_path, url=None, out_path=None):

    # ── 1. Parse GeoTIFF ───────────────────────────────────────────────────
    geo = parse_geotiff(tif_path)

    # ── 2. Parse date from filename ────────────────────────────────────────
    date_from_fname = parse_date_from_filename(tif_path)

    # ── 3. Parse WorldView URL (optional) ─────────────────────────────────
    url_info = {}
    if url:
        url_info = parse_worldview_url(url)

    # ── 4. Resolve date (URL takes precedence over filename) ───────────────
    date = url_info.get('date') or date_from_fname or 'YYYY-MM-DD'

    # ── 5. Resolve sensor ─────────────────────────────────────────────────
    if 'sensor' in url_info:
        sensor_info = {k: url_info[k] for k in ('satellite', 'sensor') if k in url_info}
        sensor_note = f"identified from WorldView layer: {url_info.get('layer', '?')}"
        layer_name  = url_info.get('layer', None)
        collection  = url_info.get('collection', None)
    else:
        sensor_info = guess_sensor_from_res(geo['res_m'])
        sensor_note = sensor_info.pop('note', 'inferred from resolution')
        layer_name  = None
        collection  = None

    # ── 6. Bounding box: GeoTIFF is authoritative (user cropped the scene) ─
    lon = [geo['lon_min'], geo['lon_max']]
    lat = [geo['lat_min'], geo['lat_max']]

    # ── 7. Assemble config ─────────────────────────────────────────────────
    config = {
        'er3t': {
            'version': '1.0',
            'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'source_tif': os.path.basename(tif_path),
        },

        'paths': {
            'libradtran': '~/libradtran/v2.0.6',       # set to your libRadtran install
            'mcarats':    '~/mcarats/v0.10.4/src/mcarats',
            'data':       '~/er3t-data/',
            'output':     './output',
        },

        'scene': {
            'date': date,
            'domain': {
                'lon': lon,
                'lat': lat,
            },
            'sensor': {
                **sensor_info,
                **(({'layer': layer_name} if layer_name else {})),
                **(({'collection': collection} if collection else {})),
                'note': sensor_note,
            },
            'source': {
                'tif': os.path.basename(tif_path),
                'tif_res_m': int(geo['res_m']),
                'tif_size_px': [geo['width_px'], geo['height_px']],
                **(({'worldview_url': url} if url else {})),
                **(({'worldview_layer': layer_name} if layer_name else {})),
            },
        },

        'simulation': {
            'solver': 'mcarats',          # mcarats | lrt (libRadtran) | shdom
            'n_photon': 1e8,              # number of photons (MCARaTS)
            'wavelengths': {
                'mode': 'broadband',      # broadband | monochromatic | list
                # 'values': [650, 860]    # nm — uncomment for monochromatic/list
            },
            'output': {
                'radiance':   True,
                'irradiance': True,
                'format':     'hdf5',
            },
        },

        'atmosphere': {
            'profile':    'afglss',       # afglss | afglms | afglmw | afglt | afglsw
            'gas_abs':    'reptran',      # reptran | kato | fu
            'aerosol':    False,
        },

        'surface': {
            'albedo':     0.06,           # broadband shortwave albedo (ocean default)
            # 'albedo_file': null         # or path to a 2D albedo map
        },
    }

    # ── 8. Serialise ───────────────────────────────────────────────────────
    if out_path is None:
        base = os.path.splitext(os.path.basename(tif_path))[0]
        out_path = f"{base}_er3t.yml"

    with open(out_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return out_path, config


def main():
    parser = argparse.ArgumentParser(
        description='Parse a WorldView GeoTIFF (+ optional URL) into an EaR³T scene YAML.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('--tif', required=True, help='Path to WorldView GeoTIFF snapshot')
    parser.add_argument('--url', default=None,  help='WorldView browser URL (copy from address bar)')
    parser.add_argument('--out', default=None,  help='Output YAML path (default: <tif_basename>_er3t.yml)')
    parser.add_argument('--print', action='store_true', dest='print_yaml',
                        help='Also print the YAML to stdout')
    args = parser.parse_args()

    if not os.path.isfile(args.tif):
        sys.exit(f"ERROR: GeoTIFF not found: {args.tif}")

    out_path, config = build_yaml(args.tif, url=args.url, out_path=args.out)

    print(f"\n✓ Scene YAML written to: {out_path}")
    print(f"  Date     : {config['scene']['date']}")
    print(f"  Lon      : {config['scene']['domain']['lon']}")
    print(f"  Lat      : {config['scene']['domain']['lat']}")
    print(f"  Sensor   : {config['scene']['sensor'].get('satellite','?')} / {config['scene']['sensor'].get('sensor','?')}")
    print(f"  Solver   : {config['simulation']['solver']}")

    if args.print_yaml:
        print('\n--- YAML ---')
        with open(out_path) as f:
            print(f.read())

    print("\nNext step: review and edit the YAML (especially paths: section), then run:")
    print(f"  python scripts/run_er3t.py {out_path}\n")


if __name__ == '__main__':
    main()
