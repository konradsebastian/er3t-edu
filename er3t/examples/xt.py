"""
EaR³T Example 05 — 3D Cloud Radiance (Satellite View, LES Field)
=================================================================

What this script does
---------------------
Simulates what a satellite *would observe* looking down through an
inhomogeneous LES cloud field: nadir top-of-atmosphere radiance at 705 km
altitude.  Uses a Mie scattering phase function (more accurate than
Henyey-Greenstein for cloud droplets).

Outputs
-------
* HDF5 results in  tmp-data/05_3d_cloud_radiance/
* PNG plot         05_3d_cloud_radiance-..._<solver>.png
  Grayscale image of simulated nadir reflectance (radiance / F₀).

Key physics / "aha" moments
----------------------------
This is the most directly comparable to satellite imagery.
  - IPA: thick-cloud pixels look brighter, thin-cloud darker.
    Cloud edges appear sharp because there is no lateral photon transport.
  - 3D: bright halos appear next to cloud edges (photons scatter sideways
    into the open sky from the cloud interior — "cloud shadow brightening").
    Optically thick cloud tops can appear slightly darker than in IPA
    (photon escape from the side of the column).
These 3D effects cause systematic biases in 1D (IPA) satellite cloud
optical thickness retrievals — the core motivation for EaR³T.

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

wavelength = 650.0      # Wavelength in nm.  Try: 400, 500, 650, 860, 1640
                        # Shorter wavelengths have stronger Rayleigh scattering.

photons    = 1e6        # Monte Carlo photons per spectral bin.
                        #   1e6  → fast, lower quality image
                        #   1e7  → noticeably cleaner image (recommended)
                        #   1e8  → production quality

solver     = '3D'       # *** THE KEY TOGGLE ***
                        #   '3D'  → realistic 3D RT — photons scatter sideways
                        #   'IPA' → standard satellite retrieval assumption (1D per column)
                        # Comparing these two images shows the 3D bias in satellite data!

# ╚══════════════════════════════════════════════════════════════════════════╝


# ── Internal configuration (do not need to change) ────────────────────────
name_tag = '05_3d_cloud_radiance'
fdir0    = er3t.common.fdir_examples
Ncpu     = max(1, multiprocessing.cpu_count() - 2)
rcParams['font.size'] = 14
# ──────────────────────────────────────────────────────────────────────────


def example_05_rad_les_cloud_3d(
        wavelength=wavelength,
        solver=solver,
        overwrite=True,
        plot=True
        ):

    """
    Radiance fields using LES data — nadir radiance at satellite altitude of 705 km.
    Uses Mie phase function instead of Henyey-Greenstein.

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


    # define mca_sca object — Mie phase function for water clouds
    #╭────────────────────────────────────────────────────────────────────────────╮#
    pha0 = er3t.pre.pha.pha_mie_wc(wavelength=wavelength)
    sca  = er3t.rtm.mca.mca_sca(pha_obj=pha0, fname='%s/mca_sca.bin' % fdir, overwrite=overwrite)
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define mcarats 1d and 3d "atmosphere"
    #╭────────────────────────────────────────────────────────────────────────────╮#
    atm3d0  = er3t.rtm.mca.mca_atm_3d(cld_obj=cld0, atm_obj=atm0, pha_obj=pha0, fname='%s/mca_atm_3d.bin' % fdir, overwrite=overwrite)
    atm1d0  = er3t.rtm.mca.mca_atm_1d(atm_obj=atm0, abs_obj=abs0)

    atm_1ds   = [atm1d0]
    atm_3ds   = [atm3d0]
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # define mcarats object and run (radiance mode)
    #╭────────────────────────────────────────────────────────────────────────────╮#
    mca0 = er3t.rtm.mca.mcarats_ng(
            date=datetime.datetime(2017, 8, 13),
            atm_1ds=atm_1ds,
            atm_3ds=atm_3ds,
            Ng=abs0.Ng,
            target='radiance',
            surface_albedo=0.03,
            sca=sca,
            solar_zenith_angle=30.0,
            solar_azimuth_angle=45.0,
            sensor_zenith_angle=0.0,        # nadir view
            sensor_azimuth_angle=0.0,
            sensor_altitude=705000.0,       # 705 km — typical LEO satellite
            fdir='%s/%4.4d/rad_%s' % (fdir, wavelength, solver.lower()),
            Nrun=3,
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
    fname_h5 = '%s/mca-out-rad-%s_%s.h5' % (fdir, solver.lower(), _metadata['Function'])
    out0 = er3t.rtm.mca.mca_out_ng(fname=fname_h5, mca_obj=mca0, abs_obj=abs0, mode='mean', squeeze=True, verbose=True, overwrite=overwrite)

    # data can be accessed at
    #     out0.data['rad']['data']   shape: (Nx, Ny)
    #╰────────────────────────────────────────────────────────────────────────────╯#


    # plot
    #╭────────────────────────────────────────────────────────────────────────────╮#
    if plot:
        fname_png = '%s-%s_%s.png' % (name_tag, _metadata['Function'], solver.lower())

        fig = plt.figure(figsize=(8, 6))
        ax1 = fig.add_subplot(111)
        cs = ax1.imshow(np.transpose(out0.data['rad']['data']), cmap='Greys_r', vmin=0.0, vmax=0.3, origin='lower')
        ax1.set_xlabel('X Index')
        ax1.set_ylabel('Y Index')
        ax1.set_title('Radiance at %.2f nm (%s Mode)' % (wavelength, solver))
        plt.savefig(fname_png, bbox_inches='tight')
        plt.close(fig)
        print('Plot saved: %s' % fname_png)
    #╰────────────────────────────────────────────────────────────────────────────╯#




if __name__ == '__main__':

    print('=' * 60)
    print('EaR³T Example 05 — 3D Cloud Radiance (Satellite View)')
    print('  wavelength = %.1f nm' % wavelength)
    print('  solver     = %s' % solver)
    print('  photons    = %.0e' % photons)
    print('  Ncpu       = %d' % Ncpu)
    print('=' * 60)
    print()
    print('Tip: run with solver="3D" and solver="IPA" and compare the images.')
    print('     The difference shows the 3D bias in satellite radiance measurements.')
    print('     A higher photon count (1e7) makes the pattern cleaner.')
    print()

    example_05_rad_les_cloud_3d(
            wavelength=wavelength,
            solver=solver,
            )
