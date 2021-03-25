from osgeo import ogr, osr
from tqdm import tqdm

def valid(pred,gt):
    pred = ogr.Open(pred)
    gt = ogr.Open(gt)
    layer1 = pred.GetLayer(0)
    layer2 = gt.GetLayer(0)

    count=0
    sum = 0
    for feature1 in layer1:
        geom1 = feature1.GetGeometryRef()
        geom1 = geom1.Buffer(0.0000001)
        sum+=1
        for feature2 in layer2:
            geom2 = feature2.GetGeometryRef()
            if geom2.Intersect(geom1):
                if geom1.Intersection(geom2).Area() / geom1.Union(geom2).Area()>0.01:
                    count+=1
                    break
    print(count,len(layer1),len(layer2))
    print('虚警率', 1-count/sum)

    count=0
    sum = 0
    for feature2 in layer2:
        geom2 = feature2.GetGeometryRef()
        sum+=1
        for feature1 in layer1:
            geom1 = feature1.GetGeometryRef()
            if geom2.Intersect(geom1):
                geom1 = geom1.Buffer(0.0000001)
                if geom1.Intersection(geom2).Area() / geom1.Union(geom2).Area() > 0.01:
                    count += 1
                    break
    print('漏检率',1-count/sum)

if __name__ == '__main__':
    valid(r"N:\存档\项目\吉奥\results\分类后比较\vector\change_result.shp",r"N:\存档\项目\吉奥\vector\1920变化\1920final.shp")