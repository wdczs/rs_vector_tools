from osgeo import gdal, ogr
NoDataVal = 0

# Open the data source and read in the extent
inPolygonShp = r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\hyd_py.shp'
img_path = r"N:\存档\项目\吉奥\影像\images\2020_test.tif"
outputRaster = r"N:\存档\项目\吉奥\影像\masks\test_label.tif"

driver = gdal.GetDriverByName("GTiff")
refer_ds = gdal.Open(img_path)

save_ds = driver.Create(outputRaster, refer_ds.RasterXSize,
                                      refer_ds.RasterYSize,
                                      1, gdal.GDT_Byte, options=['COMPRESS=LZW'])

save_ds.SetGeoTransform(refer_ds.GetGeoTransform())
save_ds.SetProjection(refer_ds.GetProjection())



# Create the destination data source



# Define spatial reference

rBand = save_ds.GetRasterBand(1)
rBand.SetNoDataValue(NoDataVal)
rBand.Fill(NoDataVal)


inPolygonShp = r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\hyd_py.shp'
shpDS = ogr.Open(inPolygonShp)
shpLayer = shpDS.GetLayer()
err = gdal.RasterizeLayer(save_ds, [1], shpLayer, burn_values=[1], options=["ALL_TOUCHED=TRUE"])

inPolygonShp = r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\res_py.shp'
shpDS = ogr.Open(inPolygonShp)
shpLayer = shpDS.GetLayer()
err = gdal.RasterizeLayer(save_ds, [1], shpLayer, burn_values=[2], options=["ALL_TOUCHED=TRUE"])

inPolygonShp = r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\tra_py.shp'
shpDS = ogr.Open(inPolygonShp)
shpLayer = shpDS.GetLayer()
err = gdal.RasterizeLayer(save_ds, [1], shpLayer, burn_values=[3], options=["ALL_TOUCHED=TRUE"])

inPolygonShp = r'E:\\项目\\吉奥\\嘉善裁剪影像\\矢量\\2019年\\2019年1：500数据\\veg_py.shp'
shpDS = ogr.Open(inPolygonShp)
shpLayer = shpDS.GetLayer()
err = gdal.RasterizeLayer(save_ds, [1], shpLayer, burn_values=[4], options=["ALL_TOUCHED=TRUE"])

# for rasterizing with a attribute value of polygon
# err = gdal.RasterizeLayer(rasterDS, [1], shpLayer, burn_values=[0], options = ["ATTRIBUTE= Height"])