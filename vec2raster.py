import gdal
import ogr
import gdalconst
import os
# https://blog.csdn.net/weixin_40450867/article/details/103601810
# 使用gdal和ogr
# 参考https://gis.stackexchange.com/questions/212795/rasterizing-shapefiles-with-gdal-and-python。这个答案得到的结果是上下翻转的，不能直接使用
# 本人修改后的代码
# gdal.RasterizeLayer的options一些注意的地方：
# ALL_TOUCHED=TRUE 表示所有与矢量相交的像元都赋值
# "ATTRIBUTE=%s"%field 表示栅格的值为field字段的值，如果不加这条表示矢量转换为一个值

def vec2raster(shp_file_path, template_path, out_raster_path, field, nodata=0):
    """
    shp:字符串，一个矢量，从0开始计数，整数
    templatePic:字符串，模板栅格，一个tif，地理变换信息从这里读，栅格大小与该栅格一致
    output:字符串，输出栅格，一个tif
    field:字符串，栅格值的字段
    nodata:整型或浮点型，矢量空白区转换后的值
    """
    ndsm = template_path
    data = gdal.Open(ndsm, gdalconst.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()
    proj=data.GetProjection()
    #source_layer = data.GetLayer()
    x_min = geo_transform[0]
    y_max = geo_transform[3]
    x_max = x_min + geo_transform[1] * data.RasterXSize
    y_min = y_max + geo_transform[5] * data.RasterYSize
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    mb_v = ogr.Open(shp_file_path)
    mb_l = mb_v.GetLayer()
    pixel_width = geo_transform[1]
    #输出影像为16位整型

    shp_file = os.path.basename(shp_file_path)
    shp_name, _ = os.path.splitext(shp_file)
    target_ds = gdal.GetDriverByName('GTiff').Create(out_raster_path+shp_name+'.tif', x_res, y_res, 1, gdal.GDT_Byte)

    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(proj)
    band = target_ds.GetRasterBand(1)
    NoData_value = nodata
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    gdal.RasterizeLayer(target_ds, [1], mb_l, options=["ATTRIBUTE=%s"%field,'ALL_TOUCHED=TRUE'])

    target_ds = None

def file_test():
    shp_file_path = '/home/wangjue/from_Sunan/洪山_定板/1516CDGT/1516CDGT.shp'
    ref = '/home/wangjue/from_Sunan/洪山_定板/2015/洪山2015_Clip.tif'
    raster_folder = '/home/wangjue/'
    # shp, templatePic, output, field, nodata = 0
    vec2raster(shp_file_path, ref, raster_folder, field='changeGT')

if __name__ == '__main__':
    file_test()