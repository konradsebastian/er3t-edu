"""
EaR³T Example 03 — 3D Cloud + 1D Aerosol Layer, Flux
======================================================

What this script does
---------------------
Builds on Example 02 by adding a horizontally homogeneous aerosol layer
above the LES cloud field.  The aerosol is treated as 1D (same optical
properties everywhere in x, y) while the cloud remains fully 3D.

Outputs
-------
* HDF5 results in  tmp-data/03_3d_cloud_aerosol_1d_flux/
* PNG plot         03_3d_cloud_aerosol_1d_flux-..._<solver>.png
  Surface maps of upwelling and downwelling flux.

Key physics
-----------
Adding aerosol above the cloud:
  - Absorbs and scatters photons before they reach the cloud.
  - Reduces downwelling at the surface.
  - Increases upwelling at the aerosol level (backscatter).
Compare with Example 02 to isolate the aerosol effect.

Aerosol parameters you can tune (in the student control block):
  aod   — aerosol optical depth (total column; controls how thick the layer is)
  ssa   — single scattering albedo (1.0 = purely scattering, 0.0 = purely absorbing)
  asy   — asymmetry parameter (0 = isotropic, 1 = all forward, typical dust ~0.7)
  z_bot, z_top — bottom and top altitudes of the layer in km

Requires
--------
  data/00_er3t_mca/aux/les.nc  (~209 MB, downloaded via install-examples.sh)

Student controls — edit the block below
-----------------------------------------
"""

import os
import sys
import h5py
import time
import numpy as np
import datetime
import multiprocessing
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams

import er3t


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                     STUDENT CONTROL BLOCK                              ║
# ╠══════════════════════════════════════════════════════════════════════════╣

wavelength = 650.0      # Wavelength in nm.  Try: 400, 500, 650, 860

photons    = 1e6        # Monte Carlo photons per spectral bin.
                        #   1e6  → fast, low noise   |  1e8  → production quality

solver     = '3D'       # '3D' (full horizontal transport) or 'IPA' (column-by-column)

# ── Aerosol layer parameters ──────────────────────────────────────────────
aod   = 0.4             # Aerosol optical depth.  Try: 0.0 (no aerosol), 0.2, 0.4, 1.0
ssa   = 0.9             # Single scattering albedo.  0.9 = mostly scattering (clean)
                        # Try: 0.7 (absorbing, like black carbon / urban smoke)
asy   = 0.6             # Asymmetry parameter (Henyey-Greenstein).
z_bot = 5.0             # Layer bottom altitude [km]
z_top = 8.0             # Layer top altitude [km]
# ──────────────────────────────────────────────────────────────────────────

# ╚══════════════════════════════════════════════════════════════════════════╝


# ── Internal configuration (do not need to change) ────────────────────────
name_tag = '03_3d_cloud_aerosol_1d_flux'
fdir0    = er3t.common.fdir_examples
Ncpu     = max(1, multiprocessing.cpu_count() - 2)
rcParams['font.size'] = 14
# ──────────────────────────────────────────────────────────────────────────


def example_03_flux_les_cloud_3d_aerosol_1d(
        wavelength=wavelength,
        solver=solver,
        overwrite=True,
        plot=True
        ):

    """
    Similar to example_02 but adding an aerosol layer above LES clouds

    To run this test, we will need data/00_er3t_mca/aux/les.nc
    """

    _metadata   = {'Computer': os.uname()[1], 'Script': os.path.abspath(__file__), 'Function':sys._getframe().f_code.co_name, 'Date':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    fdir='%s/tmp-data/%s/%s' % (fdir0, name_tag, _metadata['Function'])

    if not os.path.exists(fdir):
        os.makedirs(fdir)

    # define an atmosphere object
    #╭────────────────────────────────────────────────────────────────────────────╮#
    levels    = np.linspace(0.0, 20.0, 21)
    fname_atm = '%s/atm.pk' % fdir
    atm0      = er3t.pre.atm.atm_atmmod(levels=levels, fname=fname_atm, overwrite=overwrite)
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define an absorption object
    #╭────────────────────────────────────────────────────────────────────────────╮#
    fname_abs = '%s/abs.pk' % fdir
    abs0      = er3t.pre.abs.abs_rep(wavelength=wavelength, fname=fname_abs, atm_obj=atm0, target='medium', overwrite=overwrite)
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define a cloud object from LES output
    #╭────────────────────────────────────────────────────────────────────────────╮#
    fname_nc  = '%s/data/00_er3t_mca/aux/les.nc' % (er3t.common.fdir_examples)
    fname_les = '%s/les.pk' % fdir
    cld0      = er3t.pre.cld.cld_les(fname_nc=fname_nc, fname=fname_les, coarsen=[1, 1, 25], overwrite=overwrite)
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define mcarats 1d and 3d "atmosphere" — cloud + aerosol
    #╭────────────────────────────────────────────────────────────────────────────╮#
    # inhomogeneous 3d mcarats "atmosphere" (cloud)
    atm3d0  = er3t.rtm.mca.mca_atm_3d(cld_obj=cld0, atm_obj=atm0, fname='%s/mca_atm_3d.bin' % fdir)

    # homogeneous 1d mcarats "atmosphere" (gas)
    atm1d0  = er3t.rtm.mca.mca_atm_1d(atm_obj=atm0, abs_obj=abs0)

    # add homogeneous 1d aerosol layer on top of the 1d atmosphere
    aer_ext = aod / (z_top - z_bot) / 1000.0   # convert AOD to extinction [km⁻¹]
    atm1d0.add_mca_1d_atm(ext1d=aer_ext, omg1d=ssa, apf1d=asy, z_bottom=z_bot, z_top=z_top)

    atm_1ds   = [atm1d0]
    atm_3ds   = [atm3d0]
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define mcarats object and run
    #╭────────────────────────────────────────────────────────────────────────────╮#
    mca0 = er3t.rtm.mca.mcarats_ng(
            date=datetime.datetime(2017, 8, 13),
            atm_1ds=atm_1ds,
            atm_3ds=atm_3ds,
            Ng=abs0.Ng,
            Nrun=3,
            solar_zenith_angle=30.0,
            solar_azimuth_angle=45.0,
            fdir='%s/%4.4d/flux_%s' % (fdir, wavelength, solver.lower()),
            photons=photons,
            weights=abs0.coef['weight']['data'],
            solver=solver,
            Ncpu=Ncpu,
            mp_mode='py',
            overwrite=overwrite
            )
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # collect output
    #╭────────────────────────────────────────────────────────────────────────────╮#
    fname_h5 = '%s/mca-out-flux-%s_%s.h5' % (fdir, solver.lower(), _metadata['Function'])
    out0 = er3t.rtm.mca.mca_out_ng(fname=fname_h5, mca_obj=mca0, abs_obj=abs0, mode='mean', squeeze=True, verbose=True, overwrite=overwrite)
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # plot
    #╭────────────────────────────────────────────────────────────────────────────╮#
    if plot:
        z_index = 0
        fname_png = '%s-%s_%s.png' % (name_tag, _metadata['Function'], solver.lower())

        fig = plt.figure(figsize=(12, 6))

        ax1 = fig.add_subplot(121)
        cs = ax1.imshow(np.transpose(out0.data['f_up']['data'][:, :, z_index]), cmap='jet', vmin=0.0, vmax=1.6, origin='lower')
        ax1.set_xlabel('X Index')
        ax1.set_ylabel('Y Index')
        ax1.set_title('3D Cloud + 1D Aerosol (%s Mode), $\\mathrm{F_{up}}$ at %d km' % (solver, atm0.lev['altitude']['data'][z_index]))

        ax2 = fig.add_subplot(122)
        cs = ax2.imshow(np.transpose(out0.data['f_down']['data'][:, :, z_index]), cmap='jet', vmin=0.0, vmax=1.6, origin='lower')
        ax2.set_xlabel('X Index')
        ax2.set_ylabel('Y Index')
        ax2.set_title('3D Cloud + 1D Aerosol (%s Mode), $\\mathrm{F_{down}}$ at %d km' % (solver, atm0.lev['altitude']['data'][z_index]))

        plt.savefig(fname_png, bbox_inches='tight')
        plt.close(fig)
        print('Plot saved: %s' % fname_png)
    #╰────────────────────────────────────────────────────────────────────────────╯#




if __name__ == '__main__':

    print('=' * 60)
    print('EaR³T Example 03 — 3D Cloud + 1D Aerosol, Flux')
    print('  wavelength = %.1f nm' % wavelength)
    print('  solver     = %s' % solver)
    print('  photons    = %.0e' % photons)
    print('  Ncpu       = %d' % Ncpu)
    print('  Aerosol:  AOD=%.2f  SSA=%.2f  asy=%.2f  z=[%.1f–%.1f km]' % (aod, ssa, asy, z_bot, z_top))
    print('=' * 60)
    print()
    print('Tip: set aod=0.0 to reproduce Example 02 exactly.')
    print('     Compare SSA=0.9 (scattering) vs SSA=0.7 (absorbing) aerosol.')
    print()

    example_03_flux_les_cloud_3d_aerosol_1d(
            wavelength=wavelength,
            solver=solver,
            )
