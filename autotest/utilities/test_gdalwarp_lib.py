#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  GDAL/OGR Test Suite
# Purpose:  test librarified gdalwarp
# Author:   Faza Mahamood <fazamhd @ gmail dot com>
# 
###############################################################################
# Copyright (c) 2015, Faza Mahamood <fazamhd at gmail dot com>
# Copyright (c) 2015, Even Rouault <even.rouault at spatialys.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import sys
import os

sys.path.append( '../pymod' )

from osgeo import gdal
import gdaltest

###############################################################################
# Simple test

def test_gdalwarp_lib_1():

    ds1 = gdal.Open('../gcore/data/byte.tif')
    dstDS = gdal.Warp('tmp/testgdalwarp1.tif', ds1)

    if dstDS.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    dstDS = None

    return 'success'


###############################################################################
# Test -of option

def test_gdalwarp_lib_2():

    ds1 = gdal.Open('../gcore/data/byte.tif')
    dstDS = gdal.Warp('tmp/testgdalwarp2.tif',[ds1], format = 'GTiff')

    if dstDS.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    dstDS = None

    return 'success'


###############################################################################
# Test -ot option

def test_gdalwarp_lib_3():

    ds1 = gdal.Open('../gcore/data/byte.tif')
    dstDS = gdal.Warp('', ds1, format = 'MEM', outputType = gdal.GDT_Int16)
    
    if dstDS.GetRasterBand(1).DataType != gdal.GDT_Int16:
        gdaltest.post_reason('Bad data type')
        return 'fail'

    if dstDS.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    dstDS = None

    return 'success'

###############################################################################
# Test -t_srs option

def test_gdalwarp_lib_4():
    
    ds1 = gdal.Open('../gcore/data/byte.tif')
    dstDS = gdal.Warp('', ds1, format = 'MEM', dstSRS = 'EPSG:32611')

    if dstDS.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    dstDS = None

    return 'success'

###############################################################################
# Test warping from GCPs without any explicit option

def test_gdalwarp_lib_5():

    ds = gdal.Open('../gcore/data/byte.tif')
    gcpList = [gdal.GCP(440720.000,3751320.000,0,0,0), gdal.GCP(441920.000,3751320.000,0,20,0), gdal.GCP(441920.000,3750120.000,0,20,20), gdal.GCP(440720.000,3750120.000,0,0,20)]
    ds1 = gdal.Translate('tmp/testgdalwarp_gcp.tif',ds,outputSRS = 'EPSG:26711',GCPs = gcpList)
    dstDS = gdal.Warp('', ds1, format = 'MEM', tps = True)

    if dstDS.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    if not gdaltest.geotransform_equals(ds.GetGeoTransform(), dstDS.GetGeoTransform(), 1e-9) :
        gdaltest.post_reason('Bad geotransform')
        return 'fail'

    dstDS = None

    return 'success'


###############################################################################
# Test warping from GCPs with -tps

def test_gdalwarp_lib_6():
    
    ds1 = gdal.Open('tmp/testgdalwarp_gcp.tif')
    dstDS = gdal.Warp('',ds1, format = 'MEM', tps = True)

    if dstDS.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    if not gdaltest.geotransform_equals(gdal.Open('../gcore/data/byte.tif').GetGeoTransform(), dstDS.GetGeoTransform(), 1e-9) :
        gdaltest.post_reason('Bad geotransform')
        return 'fail'

    dstDS = None

    return 'success'


###############################################################################
# Test -tr

def test_gdalwarp_lib_7():
    
    ds1 = gdal.Open('tmp/testgdalwarp_gcp.tif')
    dstDS = gdal.Warp('',[ds1], format = 'MEM',xRes = 120,yRes = 120)
    if dstDS is None:
        return 'fail'

    expected_gt = (440720.0, 120.0, 0.0, 3751320.0, 0.0, -120.0)
    if not gdaltest.geotransform_equals(expected_gt, dstDS.GetGeoTransform(), 1e-9) :
        gdaltest.post_reason('Bad geotransform')
        return 'fail'

    dstDS = None

    return 'success'

###############################################################################
# Test -ts

def test_gdalwarp_lib_8():
    
    ds1 = gdal.Open('tmp/testgdalwarp_gcp.tif')
    dstDS = gdal.Warp('',[ds1], format = 'MEM',width = 10,height = 10)
    if dstDS is None:
        return 'fail'

    expected_gt = (440720.0, 120.0, 0.0, 3751320.0, 0.0, -120.0)
    if not gdaltest.geotransform_equals(expected_gt, dstDS.GetGeoTransform(), 1e-9) :
        gdaltest.post_reason('Bad geotransform')
        return 'fail'

    dstDS = None

    return 'success'

###############################################################################
# Test -te

def test_gdalwarp_lib_9():

    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', outputBounds = [440720.000, 3750120.000, 441920.000, 3751320.000])

    if not gdaltest.geotransform_equals(gdal.Open('../gcore/data/byte.tif').GetGeoTransform(), ds.GetGeoTransform(), 1e-9) :
        gdaltest.post_reason('Bad geotransform')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -rn

def test_gdalwarp_lib_10():

    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', width = 40, height = 40, resampleAlg = gdal.GRIORA_NearestNeighbour)

    if ds.GetRasterBand(1).Checksum() != 18784:
        print(ds.GetRasterBand(1).Checksum())
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -rb

def test_gdalwarp_lib_11():

    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', width = 40, height = 40, resampleAlg = gdal.GRIORA_Bilinear)

    ref_ds = gdal.Open('ref_data/testgdalwarp11.tif')
    maxdiff = gdaltest.compare_ds(ds, ref_ds, verbose=0)
    ref_ds = None

    if maxdiff > 1:
        gdaltest.compare_ds(ds, ref_ds, verbose=1)
        gdaltest.post_reason('Image too different from reference')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -rc

def test_gdalwarp_lib_12():

    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', width = 40, height = 40, resampleAlg = gdal.GRIORA_Cubic)

    ref_ds = gdal.Open('ref_data/testgdalwarp12.tif')
    maxdiff = gdaltest.compare_ds(ds, ref_ds, verbose=0)
    ref_ds = None

    if maxdiff > 1:
        gdaltest.compare_ds(ds, ref_ds, verbose=1)
        gdaltest.post_reason('Image too different from reference')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -rcs

def test_gdalwarp_lib_13():

    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', width = 40, height = 40, resampleAlg = gdal.GRIORA_CubicSpline)

    ref_ds = gdal.Open('ref_data/testgdalwarp13.tif')
    maxdiff = gdaltest.compare_ds(ds, ref_ds, verbose=0)
    ref_ds = None

    if maxdiff > 1:
        gdaltest.compare_ds(ds, ref_ds, verbose=1)
        gdaltest.post_reason('Image too different from reference')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -r lanczos

def test_gdalwarp_lib_14():

    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', width = 40, height = 40, resampleAlg = gdal.GRIORA_Lanczos)

    ref_ds = gdal.Open('ref_data/testgdalwarp14.tif')
    maxdiff = gdaltest.compare_ds(ds, ref_ds, verbose=0)
    ref_ds = None

    if maxdiff > 1:
        gdaltest.compare_ds(ds, ref_ds, verbose=1)
        gdaltest.post_reason('Image too different from reference')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -dstnodata

def test_gdalwarp_lib_15():

    ds = gdal.Warp('', 'tmp/testgdalwarp_gcp.tif', format = 'MEM', dstSRS = 'EPSG:32610', dstNodata = 1)

    if ds.GetRasterBand(1).GetNoDataValue() != 1:
        print(ds.GetRasterBand(1).GetNoDataValue())
        gdaltest.post_reason('Bad nodata value')
        return 'fail'

    if ds.GetRasterBand(1).Checksum() != 4523:
        print(ds.GetRasterBand(1).Checksum())
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -of VRT which is a special case

def test_gdalwarp_lib_16():

    ds = gdal.Warp('/vsimem/test_gdalwarp_lib_16.vrt', 'tmp/testgdalwarp_gcp.tif', format = 'VRT')
    if ds is None:
        return 'fail'

    if ds.GetRasterBand(1).Checksum() != 4672:
        print(ds.GetRasterBand(1).Checksum())
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    ds = None

    gdal.Unlink('/vsimem/test_gdalwarp_lib_16.vrt')

    return 'success'

###############################################################################
# Test -dstalpha

def test_gdalwarp_lib_17():

    ds = gdal.Warp('', '../gcore/data/rgbsmall.tif', format = 'MEM', dstAlpha = True)
    if ds is None:
        return 'fail'

    if ds.GetRasterBand(4) is None:
        gdaltest.post_reason('No alpha band generated')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -et 0 which is a special case

def test_gdalwarp_lib_19():

    ds = gdal.Warp('', 'tmp/testgdalwarp_gcp.tif', format = 'MEM', errorThreshold = 0)
    if ds is None:
        return 'fail'

    if ds.GetRasterBand(1).Checksum() != 4672:
        print(ds.GetRasterBand(1).Checksum())
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test cutline from OGR datasource.

def test_gdalwarp_lib_21():

    ds = gdal.Warp('', '../gcore/data/utmsmall.tif', format = 'MEM', cutlineDSName = 'data/cutline.vrt', cutlineLayer = 'cutline')
    if ds is None:
        return 'fail'

    if ds.GetRasterBand(1).Checksum() != 19139:
        print(ds.GetRasterBand(1).Checksum())
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test cutline with ALL_TOUCHED enabled.

def test_gdalwarp_lib_23():

    ds = gdal.Warp('', '../gcore/data/utmsmall.tif', format = 'MEM', warpOptions = [ 'CUTLINE_ALL_TOUCHED=TRUE' ], cutlineDSName = 'data/cutline.vrt', cutlineLayer = 'cutline')
    if ds is None:
        return 'fail'

    if ds.GetRasterBand(1).Checksum() != 20123:
        print(ds.GetRasterBand(1).Checksum())
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -tap

def test_gdalwarp_lib_32():

    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', targetAlignedPixels = True, xRes = 100, yRes = 50)
    if ds is None:
        return 'fail'

    expected_gt = (440700.0, 100.0, 0.0, 3751350.0, 0.0, -50.0)
    got_gt = ds.GetGeoTransform()
    if not gdaltest.geotransform_equals(expected_gt, got_gt, 1e-9) :
        gdaltest.post_reason('Bad geotransform')
        print(got_gt)
        return 'fail'

    if ds.RasterXSize != 13 or ds.RasterYSize != 25:
        gdaltest.post_reason('Wrong raster dimensions : %d x %d' % (ds.RasterXSize, ds.RasterYSize) )
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test warping multiple sources

def test_gdalwarp_lib_34():

    srcds1 = gdal.Translate('', '../gcore/data/byte.tif', format = 'MEM', srcWin = [0,0,10,20])
    srcds2 = gdal.Translate('', '../gcore/data/byte.tif', format = 'MEM', srcWin = [10,0,10,20])
    ds = gdal.Warp('', [srcds1, srcds2], format = 'MEM')

    cs = ds.GetRasterBand(1).Checksum()
    gt = ds.GetGeoTransform()
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    ds = None

    if xsize != 20 or ysize != 20:
        gdaltest.post_reason('bad dimensions')
        print(xsize)
        print(ysize)
        return 'fail'

    if cs != 4672:
        gdaltest.post_reason('bad checksum')
        print(cs)
        return 'fail'

    expected_gt = (440720.0, 60.0, 0.0, 3751320.0, 0.0, -60.0)
    for i in range(6):
        if abs(gt[i] - expected_gt[i]) > 1e-5:
            gdaltest.post_reason('bad gt')
            print(gt)
            return 'fail'

    return 'success'

###############################################################################
# Test -te_srs

def test_gdalwarp_lib_45():

    ds = gdal.Warp('', ['../gcore/data/byte.tif'], format = 'MEM', outputBounds = [-117.641087629972, 33.8915301685897, -117.628190189534, 33.9024195619201 ], outputBoundsSRS = 'EPSG:4267')
    if ds.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('fail')
        print(ds.GetRasterBand(1).Checksum())
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test -crop_to_cutline

def test_gdalwarp_lib_46():

    ds = gdal.Warp('', ['../gcore/data/utmsmall.tif'], format = 'MEM', cutlineDSName = 'data/cutline.vrt', cropToCutline = True)
    if ds.GetRasterBand(1).Checksum() != 19582:
        print(ds.GetRasterBand(1).Checksum())
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Test callback

def mycallback(pct, msg, user_data):
    user_data[0] = pct
    return 1

def test_gdalwarp_lib_100():

    tab = [ 0 ]
    ds = gdal.Warp('', '../gcore/data/byte.tif', format = 'MEM', callback = mycallback, callback_data = tab)
    if ds is None:
        return 'fail'

    if ds.GetRasterBand(1).Checksum() != 4672:
        gdaltest.post_reason('Bad checksum')
        return 'fail'

    if tab[0] != 1.0:
        gdaltest.post_reason('Bad percentage')
        return 'fail'

    ds = None

    return 'success'

###############################################################################
# Cleanup

def test_gdalwarp_lib_cleanup():

    # We don't clean up when run in debug mode.
    if gdal.GetConfigOption( 'CPL_DEBUG', 'OFF' ) == 'ON':
        return 'success'
    
    for i in range(2):
        try:
            os.remove('tmp/testgdalwarp' + str(i+1) + '.tif')
        except:
            pass
    try:
        os.remove('tmp/testgdalwarp_gcp.tif')
    except:
        pass
    
    return 'success'

gdaltest_list = [
    test_gdalwarp_lib_cleanup,
    test_gdalwarp_lib_1,
    test_gdalwarp_lib_2,
    test_gdalwarp_lib_3,
    test_gdalwarp_lib_4,
    test_gdalwarp_lib_5,
    test_gdalwarp_lib_6,
    test_gdalwarp_lib_7,
    test_gdalwarp_lib_8,
    test_gdalwarp_lib_9,
    test_gdalwarp_lib_10,
    test_gdalwarp_lib_11,
    test_gdalwarp_lib_12,
    test_gdalwarp_lib_13,
    test_gdalwarp_lib_14,
    test_gdalwarp_lib_15,
    test_gdalwarp_lib_16,
    test_gdalwarp_lib_17,
    test_gdalwarp_lib_19,
    test_gdalwarp_lib_21,
    test_gdalwarp_lib_23,
    test_gdalwarp_lib_32,
    test_gdalwarp_lib_34,
    test_gdalwarp_lib_45,
    test_gdalwarp_lib_46,
    test_gdalwarp_lib_100,
    test_gdalwarp_lib_cleanup,
    ]

if __name__ == '__main__':

    gdaltest.setup_run( 'test_gdalwarp_lib' )

    gdaltest.run_tests( gdaltest_list )

    gdaltest.summarize()