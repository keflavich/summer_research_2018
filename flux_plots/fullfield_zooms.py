import numpy as np
from astropy.table import Table
from astropy import units as u
from astropy import coordinates
import pylab as pl
from astropy.io import fits
from astropy import wcs
import astropy.visualization
from astropy.convolution import convolve, Gaussian2DKernel
from mpl_plot_templates import asinh_norm
import matplotlib
from collections import defaultdict
import warnings
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

psf_center = coordinates.SkyCoord('5:35:14.511 -5:22:30.561',
                                  unit=(u.h, u.deg),
                                  frame='icrs')

zoomregions1 = {'SourceI (10)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.532",
                                                   "-5:22:30.810",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.502",
                                                 "-5:22:30.410",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.25,0.9],
                'loc': 2,
                'l1':3,
                'l2':1,
                'min': -0.001,
                'max': 0.03,
                'zoom': 10,
               },
               'BN (20)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.120",
                                                   "-5:22:22.820",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.092",
                                                 "-5:22:22.46",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.725,0.85],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.001,
                'max': 0.14,
                'zoom': 10,
               },
                '(9)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.816",
                                                   "-5:22:30.84",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.790",
                                                 "-5:22:30.49",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.25,0.3],
                'loc': 2,
                'l1':2,
                'l2':4,
                'min': -0.001,
                'max': 0.014,
                'zoom': 10,
               },
               'SourceN (5)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.372",
                                                   "-5:22:32.94",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.345",
                                                 "-5:22:32.50",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.75,0.3],
                'loc': 2,
                'l1':1,
                'l2':3,
                'min': -0.001,
                'max': 0.006,
                'zoom': 10,
               },
               'IRC6E (18)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.266",
                                                   "-5:22:28.186",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.249",
                                                 "-5:22:27.926",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.75,0.65],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.001,
                'max': 0.008,
                'zoom': 10,
               },
               'IRC2C (11)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.405",
                                                   "-5:22:30.51",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.394",
                                                 "-5:22:30.32",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.75,0.50],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.001,
                'max': 0.009,
                'zoom': 10,
               },
               '(16,17)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.435",
                                                   "-5:22:28.55",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.403",
                                                 "-5:22:28.28",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.5,0.85],
                'loc': 2,
                'l1':3,
                'l2':4,
                'min': -0.0005,
                'max': 0.0025,
                'zoom': 10,
               },
               '(8)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.585",
                                                   "-5:22:31.44",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.564",
                                                 "-5:22:31.13",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.5,0.25],
                'loc': 2,
                'l1':1,
                'l2':2,
                'min': -0.001,
                'max': 0.005,
                'zoom': 10,
               }
}

zoomregions2 = {'(4)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.884",
                                                   "-5:22:32.9",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.87",
                                                 "-5:22:32.67",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.25,0.2],
                'loc': 3,
                'l1':2,
                'l2':1,
                'min': -0.0001,
                'max': 0.005,
                'zoom': 15,
               },
                '(14)':
               {'bottomleft': coordinates.SkyCoord("5:35:15.185",
                                                   "-5:22:29.73",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:15.1738",
                                                 "-5:22:29.57",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.35,0.7],
                'loc': 5,
                'l1':4,
                'l2':3,
                'min': -0.0001,
                'max': 0.006,
                'zoom': 15,
               },
                '(15)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.982",
                                                   "-5:22:29.293",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.964",
                                                 "-5:22:29.05",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.55,0.7],
                'loc': 1,
                'l1':2,
                'l2':3,
                'min': -0.0001,
                'max': 0.003,
                'zoom': 17,
               },
                '(1)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.67",
                                                   "-5:22:38.638",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.6465",
                                                 "-5:22:38.370",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.59,0.3],
                'loc': 7,
                'l1':4,
                'l2':3,
                'min': -0.0001,
                'max': 0.004,
                'zoom': 15,
               },
                '(6)':
               {'bottomleft': coordinates.SkyCoord("5:35:13.969",
                                                   "-5:22:31.933",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:13.96",
                                                 "-5:22:31.838",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.72,0.25],
                'loc': 6,
                'l1':2,
                'l2':1,
                'min': -0.0001,
                'max': 0.002,
                'zoom': 28,
               },
                '(21)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.9508",
                                                   "-5:22:20.775",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.9398",
                                                 "-5:22:20.638",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.5,0.75],
                'loc': 8,
                'l1':3,
                'l2':2,
                'min': -0.0001,
                'max': 0.003,
                'zoom': 20,
               }

}

zoomregions3 = {'(0)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.3596",
                                                   "-5:22:40.505",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.344",
                                                 "-5:22:40.28",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.625,0.35],
                'loc': 2,
                'l1':3,
                'l2':2,
                'min': -0.001,
                'max': 0.005,
                'zoom': 20,
               },
                '(3)':
               {'bottomleft': coordinates.SkyCoord("5:35:14.4169",
                                                   "-5:22:33.386",                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:14.4072",
                                                 "-5:22:33.16",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.65,0.55],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.001,
                'max': 0.002,
                'zoom': 20,
               },
                '(13)':
               {'topright': coordinates.SkyCoord("5:35:14.726",
                                                   "-5:22:29.750",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'bottomleft': coordinates.SkyCoord("5:35:14.7364",
                                                 "-5:22:29.902",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.3,0.82],
                'loc': 2,
                'l1':3,
                'l2':4,
                'min': -0.0005,
                'max': 0.001,
                'zoom': 30,
               },
                '(19)':
               {'topright': coordinates.SkyCoord("5:35:14.2625",
                                                   "-5:22:27.00",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'bottomleft': coordinates.SkyCoord("5:35:14.283",
                                                 "-5:22:27.31",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.55,0.82],
                'loc': 2,
                'l1':4,
                'l2':3,
                'min': -0.001,
                'max': 0.003,
                'zoom': 15,
               },
                '(27)':
               {'topright': coordinates.SkyCoord("5:35:14.9813",
                                                   "-5:22:39.366",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'bottomleft': coordinates.SkyCoord("5:35:15.0137",
                                                 "-5:22:39.85",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.35,0.35],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.001,
                'max': 0.003,
                'zoom': 10,
               }
}


zoomregions4 = {'163-249 (69)':
               {'bottomleft': coordinates.SkyCoord("5:35:16.3535",
                                                   "-5:22:49.262",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:16.3289",
                                                 "-5:22:48.900",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.27,0.45],
                'loc': 2,
                'l1':3,
                'l2':2,
                'min': -0.0001,
                'max': 0.0015,
                'zoom': 20,
               },
                '163-222 (71)':
               {'bottomleft': coordinates.SkyCoord("5:35:16.3260",
                                                   "-5:22:21.744",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:16.2948",
                                                 "-5:22:21.274",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.5,0.8],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.0001,
                'max': 0.0005,
                'zoom': 20,
               },
                'HC393 (73)':
               {'bottomleft': coordinates.SkyCoord("5:35:16.1581",
                                                   "-5:22:55.494",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:16.1300",
                                                 "-5:22:55.068",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.57,0.4],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.0001,
                'max': 0.0005,
                'zoom': 30,
               },
                'HC401 (74)':
               {'bottomleft': coordinates.SkyCoord("5:35:16.0893",
                                                   "-5:22:54.510",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:16.0645",
                                                 "-5:22:54.142",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.35,0.3],
                'loc': 2,
                'l1':1,
                'l2':3,
                'min': -0.0001,
                'max': 0.0005,
                'zoom': 15,
               },
                'HC447 (72)':
               {'bottomleft': coordinates.SkyCoord("5:35:15.9025",
                                                   "-5:22:33.400",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:15.8711",
                                                 "-5:22:32.932",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.4,0.6],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.0001,
                'max': 0.0005,
                'zoom': 10,
               },
                'HC389 (75)':
               {'bottomleft': coordinates.SkyCoord("5:35:15.65",
                                                   "-5:22:56.632",
                                                   unit=(u.h, u.deg),
                                                   frame='icrs'),
                'topright': coordinates.SkyCoord("5:35:15.6223",
                                                 "-5:22:56.222",
                                                 unit=(u.h, u.deg),
                                                 frame='icrs'),
                'inregion': 'SourceI',
                'bbox':[0.45,0.25],
                'loc': 2,
                'l1':2,
                'l2':3,
                'min': -0.0001,
                'max': 0.0005,
                'zoom': 10,
               }
}



def inset_overlays(fn, zoomregions, fignum=1,
                   psffn=None,
                   vmin=-0.001, vmax=0.01,
                   directory = '/lustre/aoc/students/jotter/directory/',
                   bottomleft=coordinates.SkyCoord('5:35:16.3847 -5:22:58.542', unit=(u.h, u.deg), frame='icrs'),
                   topright=coordinates.SkyCoord('5:35:13.5 -5:22:15', unit=(u.h, u.deg), frame='icrs'),
                   tick_fontsize=pl.rcParams['axes.labelsize']):
    #bottomleft=coordinates.SkyCoord('5:35:15.236 -5:22:41.85', unit=(u.h, u.deg), frame='icrs'),
    #topright=coordinates.SkyCoord('5:35:13.586 -5:22:17.12', unit=(u.h, u.deg), frame='icrs'),
                  
    fn = directory+fn
    hdu = fits.open(fn)[0]
    print(fn)

    mywcs = wcs.WCS(hdu.header).celestial

    figure = pl.figure(fignum)
    figure.clf()
    ax = figure.add_axes([0.15, 0.1, 0.8, 0.8], projection=mywcs)

    ra = ax.coords['ra']
    ra.set_major_formatter('hh:mm:ss.s')
    dec = ax.coords['dec']
    ra.set_axislabel("RA (ICRS)", fontsize=pl.rcParams['axes.labelsize'])
    dec.set_axislabel("Dec (ICRS)", fontsize=pl.rcParams['axes.labelsize'], minpad=0.0)
    ra.ticklabels.set_fontsize(tick_fontsize)
    ra.set_ticks(exclude_overlapping=True)
    dec.ticklabels.set_fontsize(tick_fontsize)
    dec.set_ticks(exclude_overlapping=True)


    im = ax.imshow(hdu.data.squeeze()*1e3,
                   transform=ax.get_transform(mywcs),
                   vmin=vmin*1e3, vmax=vmax*1e3, cmap=pl.cm.gray_r,
                   interpolation='nearest',
                   origin='lower', norm=asinh_norm.AsinhNorm())

    (x1,y1),(x2,y2) = (mywcs.wcs_world2pix([[bottomleft.ra.deg,
                                             bottomleft.dec.deg]],0)[0],
                       mywcs.wcs_world2pix([[topright.ra.deg,
                                             topright.dec.deg]],0)[0]
                      )

    # we'll want this later
    #make_scalebar(ax, scalebarpos,
    #              length=(0.5*u.pc / distance).to(u.arcsec,
    #                                              u.dimensionless_angles()),
    #              color='k',
    #              label='0.5 pc',
    #              text_offset=1.0*u.arcsec,
    #             )


    ax.set_aspect(1)
    ax.axis([x1,x2,y1,y2])


    for zoomregion in zoomregions:

        ZR = zoomregions[zoomregion]

        parent_ax = zoomregions[ZR['inset_axes']]['axins'] if 'inset_axes' in ZR else ax

        bl, tr = ZR['bottomleft'],ZR['topright'],
        (zx1,zy1),(zx2,zy2) = (mywcs.wcs_world2pix([[bl.ra.deg,
                                                     bl.dec.deg]],0)[0],
                               mywcs.wcs_world2pix([[tr.ra.deg,
                                                     tr.dec.deg]],0)[0]
                              )
        print(zoomregion,zx1,zy1,zx2,zy2)

        inset_data = hdu.data.squeeze()[int(zy1):int(zy2), int(zx1):int(zx2)]
        #inset_data = hdu.data.squeeze()
        inset_wcs = mywcs.celestial[int(zy1):int(zy2), int(zx1):int(zx2)]
        #inset_wcs = mywcs

        axins = zoomed_inset_axes(parent_ax, zoom=ZR['zoom'], loc=ZR['loc'],
                                  bbox_to_anchor=ZR['bbox'],
                                  bbox_transform=figure.transFigure,
                                  axes_class=astropy.visualization.wcsaxes.core.WCSAxes,
                                  axes_kwargs=dict(wcs=inset_wcs))
        ZR['axins'] = axins
        imz = axins.imshow(inset_data,
                           #transform=parent_ax.get_transform(inset_wcs),
                           extent=[int(zx1), int(zx2), int(zy1), int(zy2)],
                           vmin=ZR['min'], vmax=ZR['max'], cmap=pl.cm.gray_r,
                           interpolation='nearest',
                           origin='lower', norm=asinh_norm.AsinhNorm())


        ax.axis([x1,x2,y1,y2])
        #axins.axis([zx1,zx2,zy1,zy2])
        #print(axins.axis())

        axins.set_xticklabels([])
        axins.set_yticklabels([])

        #parent_ax.text(zx1, zy1, zoomregion)
        axins.text(int(zx1)+5, int(zy1)+5, zoomregion, fontsize=6)
        lon = axins.coords['ra']
        lat = axins.coords['dec']
        lon.set_ticklabel_visible(False)
        lat.set_ticklabel_visible(False)
        lon.set_ticks_visible(False)
        lat.set_ticks_visible(False)

        # draw a bbox of the region of the inset axes in the parent axes and
        # connecting lines between the bbox and the inset axes area
        mark_inset(parent_axes=parent_ax, inset_axes=axins,
                   loc1=ZR['l1'], loc2=ZR['l2'], fc="none", ec="0.5",
                   lw=0.5)


        figure.canvas.draw()
        assert np.abs(ax.bbox._bbox.x1 - 0.95) > 1e-4

    cax = figure.add_axes([ax.bbox._bbox.x1+0.01, ax.bbox._bbox.y0, 0.02,
                           ax.bbox._bbox.y1-ax.bbox._bbox.y0])
    cb = figure.colorbar(mappable=im, cax=cax)
    #print("1. cb labels: {0}".format([x.get_text() for x in cb.ax.get_yticklabels()]))
    cb.set_label("$S_{1 mm}$ [mJy beam$^{-1}$]")
    #print("2. cb labels: {0}".format([x.get_text() for x in cb.ax.get_yticklabels()]))
    cb.formatter.format = "%3.1f"
    #print("3. cb labels: {0}".format([x.get_text() for x in cb.ax.get_yticklabels()]))
    cb.set_ticks(cb.formatter.locs)
    #print("4. cb labels: {0}".format([x.get_text() for x in cb.ax.get_yticklabels()]))
    cb.set_ticklabels(["{0:3.1f}".format(float(x)) for x in cb.formatter.locs])
    #print("5. cb labels: {0}".format([x.get_text() for x in cb.ax.get_yticklabels()]))
    cb.ax.set_yticklabels(["{0:3.1f}".format(float(x.get_text())) for x in cb.ax.get_yticklabels()])
    #print("6. cb labels: {0}".format([x.get_text() for x in cb.ax.get_yticklabels()]))
    


    if psffn is not None:
        psf = fits.open(psffn)
        psfwcs = wcs.WCS(psf[0].header)
        cx,cy = psfwcs.celestial.wcs_world2pix(psf_center.ra.deg, psf_center.dec.deg, 0)
        cx = int(cx)
        cy = int(cy)
        zy1 = cy-50
        zy2 = cy+50
        zx1 = cx-50
        zx2 = cx+50

        inset_wcs = psfwcs.celestial[zy1:zy2, zx1:zx2]
        inset_data = psf[0].data[cy-50:cy+50, cx-50:cx+50]

        axins = zoomed_inset_axes(parent_ax, zoom=10, loc=2,
                                  bbox_to_anchor=(0.05,0.25),
                                  bbox_transform=figure.transFigure,
                                  axes_class=astropy.visualization.wcsaxes.core.WCSAxes,
                                  axes_kwargs=dict(wcs=inset_wcs),
                                 )
        imz = axins.imshow(inset_data,
                           extent=[int(zx1), int(zx2), int(zy1), int(zy2)],
                           vmin=0, vmax=1, cmap=pl.cm.gray_r,
                           interpolation='nearest',
                           origin='lower', norm=asinh_norm.AsinhNorm())
        axins.contour(np.linspace(zx1, zx2, inset_data.shape[1]),
                      np.linspace(zy1, zy2, inset_data.shape[0]),
                      inset_data,
                      levels=[0.05, 0.1, 0.2, 0.3],
                      linewidths=[0.3]*10,
                      alpha=0.75,
                      #colors=['r']*10,
                     )
        axins.set_xticks([])
        axins.set_yticks([])
        axins.set_xticklabels([])
        axins.set_yticklabels([])
        lon = axins.coords['ra']
        lat = axins.coords['dec']
        lon.set_ticklabel_visible(False)
        lat.set_ticklabel_visible(False)
        lon.set_ticks_visible(False)
        lat.set_ticks_visible(False)


    return figure


if __name__ == "__main__":

    #for fn in (("Orion_SourceI_B6_continuum_r-2.clean0.1mJy.selfcal.phase4.deepmask.allbaselines.image.tt0.pbcor.fits", "/lustre/aoc/students/jotter/directory/"),
            #"Orion_SourceI_B3_continuum_r-2.clean0.1mJy.image.tt0.pbcor.fits", "/lustre/aoc/students/jotter/directory/"),
            #("Orion_SourceI_B6_continuum_r-2.clean0.5mJy.500klplus.image.tt0.pbcor.fits", "/lustre/aoc/students/jotter/directory/OrionB6/")):
    #fn = 'B6_convolved_r0.5.clean0.05mJy.150mplus.deepmask.image.tt0.pbcor.fits'
    fn = 'Orion_SourceI_B3_continuum_r0.5.clean0.05mJy.allbaselines.deepmask.image.tt0.pbcor.fits'
    directory='/lustre/aoc/students/jotter/directory/OrionB3/'
    figure = inset_overlays(fn, zoomregions=zoomregions4, directory=directory,
                                #psffn=fn.replace("image.tt0.pbcor","psf.tt0"),
                                vmin=-0.0005, vmax=0.005)
    figure.savefig('plots/'+fn.replace(".image.tt0.pbcor.fits","_inset4.pdf"), bbox_inches='tight', dpi=300)
