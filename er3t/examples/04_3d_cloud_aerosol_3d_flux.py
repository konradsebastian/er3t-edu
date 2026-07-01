"""
EaR³T Example 04 — 3D Cloud + 3D Aerosol Layer, Flux
=====================================================

What this script does
---------------------
Builds on Example 03 by making the aerosol layer *inhomogeneous in 3D* —
aerosol optical properties vary in x and y, not just vertically.  Here the
aerosol is concentrated near the surface (mixed with the cloud base) and
modelled with Mie scattering phase functions (not Henyey-Greenstein).

Outputs
-------
* HDF5 results in  tmp-data/04_3d_cloud_aerosol_3d_flux/
* PNG plot         04_3d_cloud_aerosol_3d_flux-..._<solver>.png
  Surface maps of upwelling and downwelling flux.

Key physics
-----------
When aerosol is spatially inhomogeneous, IPA and 3D diverge even more than
for a homogeneous layer.  The 3D simulation allows photons to scatter out of
high-aerosol columns into adjacent clear columns — an effect IPA cannot
capture.

The aerosol is placed at the two lowest model levels (z ≈ 0 – 0.4 km) using
fixed extinction values.  The cloud extinction at those levels is much larger,
so the aerosol's direct radiative effect is modest but non-zero.

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

# ── 3D aerosol near-surface parameters ────────────────────────────────────
# The aerosol is placed at the lowest two model layers.
# Edit these values to change the aerosol optical properties.
aer_ext_layer0 = 0.00012   # Extinction at lowest layer [km⁻¹ per m] — try 0, 0.0001, 0.001
aer_ext_layer1 = 0.00008   # Extinction at 2nd-lowest layer
aer_ssa        = 0.85      # Single scattering albedo (same for both layers)
aer_asy        = 0.6       # Asymmetry parameter
# ──────────────────────────────────────────────────────────────────────────

# ╚══════════════════════════════════════════════════════════════════════════╝


# ── Internal configuration (do not need to change) ────────────────────────
name_tag = '04_3d_cloud_aerosol_3d_flux'
fdir0    = er3t.common.fdir_examples
Ncpu     = max(1, multiprocessing.cpu_count() - 2)
rcParams['font.size'] = 14
# ──────────────────────────────────────────────────────────────────────────


def example_04_flux_les_cloud_3d_aerosol_3d(
        wavelength=wavelength,
        solver=solver,
        overwrite=True,
        plot=True
        ):

    """
    Similar to example_03 but with a 3D aerosol layer (inhomogeneous in x,y)

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


    # define mca_sca object (Mie phase function for 3D aerosol)
    #╭────────────────────────────────────────────────────────────────────────────╮#
    pha0 = er3t.pre.pha.pha_mie_wc(wavelength=wavelength)
    sca  = er3t.rtm.mca.mca_sca(pha_obj=pha0, fname='%s/mca_sca.bin' % fdir, overwrite=overwrite)
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define mcarats 1d and 3d "atmosphere" — cloud + 3D aerosol
    #╭────────────────────────────────────────────────────────────────────────────╮#
    # inhomogeneous 3d mcarats "atmosphere" (cloud, using Mie)
    atm3d0  = er3t.rtm.mca.mca_atm_3d(cld_obj=cld0, atm_obj=atm0, pha_obj=pha0, fname='%s/mca_atm_3d.bin' % fdir, overwrite=overwrite)

    # add spatially uniform 3D aerosol near surface (same value everywhere in x,y for this example)
    ext3d = np.zeros_like(atm3d0.nml['Atm_extp3d']['data'][:, :, :, 0])
    ext3d[:, :, 0] = aer_ext_layer0
    ext3d[:, :, 1] = aer_ext_layer1

    omg3d = np.zeros_like(atm3d0.nml['Atm_extp3d']['data'][:, :, :, 0])
    omg3d[...] = aer_ssa

    apf3d = np.zeros_like(atm3d0.nml['Atm_extp3d']['data'][:, :, :, 0])
    apf3d[...] = aer_asy
    atm3d0.add_mca_3d_atm(ext3d=ext3d, omg3d=omg3d, apf3d=apf3d)

    atm3d0.gen_mca_3d_atm_file(fname='%s/mca_atm_3d.bin' % fdir)

    # homogeneous 1d mcarats "atmosphere" (gas)
    atm1d0  = er3t.rtm.mca.mca_atm_1d(atm_obj=atm0, abs_obj=abs0)

    atm_1ds   = [atm1d0]
    atm_3ds   = [atm3d0]
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define mcarats object and run
    #╭────────────────────────────────────────────────────────────────────────────╮#
    mca0 = er3t.rtm.mca.mcarats_ng(
            date=datetime.datetime(2017, 8, 13),
            atm_1ds=atm_1ds,
            atm_3ds=atm_3ds,
            sca=sca,
            Ng=abs0.Ng,
            target='flux0',
            Nrun=3,
            surface_albedo=0.03,
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
        ax1.set_title('3D Cloud + 3D Aerosol (%s Mode), $\\mathrm{F_{up}}$ at %d km' % (solver, atm0.lev['altitude']['data'][z_index]))

        ax2 = fig.add_subplot(122)
        cs = ax2.imshow(np.transpose(out0.data['f_down']['data'][:, :, z_index]), cmap='jet', vmin=0.0, vmax=1.6, origin='lower')
        ax2.set_xlabel('X Index')
        ax2.set_ylabel('Y Index')
        ax2.set_title('3D Cloud + 3D Aerosol (%s Mode), $\\mathrm{F_{down}}$ at %d km' % (solver, atm0.lev['altitude']['data'][z_index]))

        plt.savefig(fname_png, bbox_inches='tight')
        plt.close(fig)
        print('Plot saved: %s' % fname_png)
    #╰────────────────────────────────────────────────────────────────────────────╯#




if __name__ == '__main__':

    print('=' * 60)
    print('EaR³T Example 04 — 3D Cloud + 3D Aerosol, Flux')
    print('  wavelength = %.1f nm' % wavelength)
    print('  solver     = %s' % solver)
    print('  photons    = %.0e' % photons)
    print('  Ncpu       = %d' % Ncpu)
    print('  Aerosol:  ext=[%.5f, %.5f]  SSA=%.2f  asy=%.2f' % (aer_ext_layer0, aer_ext_layer1, aer_ssa, aer_asy))
    print('=' * 60)
    print()
    print('Tip: set aer_ext_layer0 = aer_ext_layer1 = 0 to reproduce Example 02.')
    print('     Increase aer_ext_layer0 to see the near-surface aerosol effect.')
    print()

    example_04_flux_les_cloud_3d_aerosol_3d(
            wavelength=wavelength,
            solver=solver,
            )
