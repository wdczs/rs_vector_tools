from rasterio.mask import mask
from collections import Counter
from osgeo import gdal
from osgeo import ogr
import json
import rasterio
import numpy as np
import os
import glob
from tqdm import tqdm


def vec2mask(img_path, shape_path):
    ds = ogr.Open(shape_path)
    src = rasterio.open(img_path)

    layer = ds.GetLayer()
    feature_count = layer.GetFeatureCount()

    feats = [layer.GetFeature(i) for i in range(feature_count)]
    invalid = []
    for i in range(feature_count):
        if feats[i].Validate() == 0:
            invalid.append(i)

    newfeats = []
    for i in range(len(feats)):
        if i not in invalid:
            newfeats.append(feats[i])
    feats = newfeats

    geos = [feats[i].geometry() for i in range(len(feats))]
    jsons = [json.loads(geos[i].ExportToJson()) for i in range(len(feats))]

    out_image, out_transform = rasterio.mask.mask(src, jsons)

    original = gdal.Open(img_path)
    driver = gdal.GetDriverByName("GTiff")
    savename = os.path.basename(img_path).replace('.tif',
                                                  ('_' + os.path.basename(shape_path).split('.shp')[0] + '.tif'))
    saveimage = driver.Create(os.path.join(save_dir, savename), original.RasterXSize, original.RasterYSize,
                              1,
                              gdal.GDT_Byte, options=['COMPRESS=LZW'])
    saveimage.SetGeoTransform(original.GetGeoTransform())
    saveimage.SetProjection(original.GetProjection())
    saveband = saveimage.GetRasterBand(1)
    saveband.WriteArray(out_image[0] != 0)
    saveimage = saveband = None


if __name__ == '__main__':
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    ogr.RegisterAll()

    save_dir = r"N:\存档\项目\吉奥\影像\masks"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


    shapes = [r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\hyd_py.shp',
              r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\res_py.shp',
              r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\tra_py.shp',
              r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\veg_py.shp']
    imgs = glob.glob(r"N:\存档\项目\吉奥\影像\images\Tiff\*.tif")
    for img_path in imgs:
        for shape_path in shapes:
            vec2mask(img_path,shape_path)