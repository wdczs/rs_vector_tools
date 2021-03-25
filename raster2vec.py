# http://www.soolco.com/post/95379_1_1.html

import os
from osgeo import gdal, ogr, osr

def deleteBackground(shp_file_path, BG_value):
    """
    删除背景,一般背景的像素值为0
    """
    driver = ogr.GetDriverByName('ESRI Shapefile')
    pFeatureDataset = driver.Open(shp_file_path, 1)
    pFeaturelayer = pFeatureDataset.GetLayer(0)
    strValue = BG_value

    strFilter = "Value = '" + str(strValue) + "'"
    pFeaturelayer.SetAttributeFilter(strFilter)
    pFeatureDef = pFeaturelayer.GetLayerDefn()
    pLayerName = pFeaturelayer.GetName()
    pFieldName = "Value"
    pFieldIndex = pFeatureDef.GetFieldIndex(pFieldName)

    for pFeature in pFeaturelayer:
        pFeatureFID = pFeature.GetFID()
        pFeaturelayer.DeleteFeature(int(pFeatureFID))

    strSQL = "REPACK " + str(pFeaturelayer.GetName())
    pFeatureDataset.ExecuteSQL(strSQL, None, "")
    pFeatureLayer = None
    pFeatureDataset = None

def RasterToPoly(raster_file_path, out_vec_path, DelBG=False):
    inraster = gdal.Open(raster_file_path)  # 读取路径中的栅格数据
    inband = inraster.GetRasterBand(1)  # 这个波段就是最后想要转为矢量的波段，如果是单波段数据的话那就都是1
    prj = osr.SpatialReference()
    prj.ImportFromWkt(inraster.GetProjection())  # 读取栅格数据的投影信息，用来为后面生成的矢量做准备

    raster_file = os.path.basename(raster_file_path)
    raster_name, _ = os.path.splitext(raster_file)
    shp_file_path = os.path.join(out_vec_path, raster_name+'.shp')

    drv = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(shp_file_path):
        drv.DeleteDataSource(shp_file_path)
    Polygon = drv.CreateDataSource(shp_file_path)  # 创建一个目标文件
    Poly_layer = Polygon.CreateLayer(shp_file_path[:-4], srs=prj, geom_type=ogr.wkbMultiPolygon)  # 对shp文件创建一个图层，定义为多个面类
    newField = ogr.FieldDefn('Value', ogr.OFTReal)  # 给目标shp文件添加一个字段，用来存储原始栅格的pixel value
    Poly_layer.CreateField(newField)
    gdal.FPolygonize(inband, None, Poly_layer, 0, ['8CONNECTED=8'])  # 核心函数，执行的就是栅格转矢量操作
    Polygon.SyncToDisk()
    Polygon = None
    if DelBG:
        deleteBackground(shp_file_path, 0)  # 删除背景　　　　

def folder_test():
    raster_folder = '/home/wangjue/script/vector_raster_tools/2'
    shp_folder = '/home/wangjue/script/vector_raster_tools/2_wobg_output'

    for raster in os.listdir(raster_folder):  # 遍历路径中每一个文件，如果存在gdal不能打开的文件类型，则后续代码可能会报错。
        if os.path.splitext(raster)[1] == '.tif':
            raster_file_path = os.path.join(raster_folder, raster)
            RasterToPoly(raster_file_path, shp_folder, True)

def file_test():
    raster_file_path = '/home/wangjue/from_Sunan/洪山_定板/1516CDGT/1516gt_twoclass.tif'
    shp_folder = '/home/wangjue/'
    RasterToPoly(raster_file_path, shp_folder, False)

if __name__ == '__main__':
    file_test()