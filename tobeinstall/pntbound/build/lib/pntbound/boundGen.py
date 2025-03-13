import shapefile as shp
from geomath import hulls as gmh
import geomath.hulls as gmh
import numpy as np
import pycrs
from io import BytesIO
from shapely.geometry import Polygon

# 'C:/Users/nthorson2/Documents/PythonScripts/testData/Input/points_to_bound_Input/f2016W_Pre/f2016W_2017_PreApplication.shp'
# 'C:/Users/nthorson2/Documents/PythonScripts/testData/Output/points_to_bound_Output/f2016W_Pre_Output/f2016W_concave.shp'


def concave_hull(file, filetype, buffer):
    if filetype == 'shp':
        # read shapefile to memory and storage as object
        dataset = shp.Reader(file)
    elif filetype == 'zip':
        #    cpgName,dbfName,prjName,shpName,shxName,txtName = file.namelist()   #test data shapefile structure
        dbfName, prjName, shpName, shxName, jsonName = file.namelist()  # JD shapefile structure
        dataset = shp.Reader(shp=BytesIO(file.read(shpName)), shx=BytesIO(
            file.read(shxName)), dbf=BytesIO(file.read(dbfName)))

    if dataset:
      # develope points array from shapefile dataset geometry for concaveHull calculations
        pntsList = []
        for point in dataset.shapeRecords():
            feature = point.shape.__geo_interface__
            featCoords = feature['coordinates']
            lat = featCoords[1]
            lon = featCoords[0]
            pntArr = [lon, lat]
            pntsList.append(list(pntArr))
      # run concave hull calculations
        concaveHull = gmh.ConcaveHull(pntsList)
      # run concave hull object collections and return array
        hull_array = concaveHull.calculate()
      # write hull_array values to adequate array structure format for polygon creation
        poly = []
        for geo in hull_array:
            lat = geo[1]
            lon = geo[0]
            geoItem = (lon, lat)
            poly.append(geoItem)

      # convert to polygon shape
        polygon = Polygon(poly)
      # buffer polygon
        if buffer:
            bufferSize = buffer / 2
            buffPoly = bufferPoly(polygon, bufferSize, concaveHull)
        else:
            buffPoly = polygon
            #buffer = determinePolyBuffer(dataset, hull_array)

        return buffPoly, hull_array, dataset


def determinePolyBuffer(dataset, edge_points):
    i = 0
    x = 0
    ttlWdth = 0
    cnt = 0

    # sort dataset points by lat and lon
    # after sort then check for larger than edge point lat and edge point lon
    # once dataset coordinates become larger than edge point coordinates break nested loop
    # and move onto next edge point

    while i < len(edge_points):
        while x < len(dataset):
            eplat = round(edge_points[i][1], 6)
            eplon = round(edge_points[i][0], 6)
            geolat = round(dataset.geometry[x].coords[0][1], 6)
            geolon = round(dataset.geometry[x].coords[0][0], 6)
            if eplat == geolat and eplon == geolon:
                ttlWdth = ttlWdth + dataset.Width[x]
                cnt = cnt + 1
                break

        i = i + 1

    if ttlWdth > 0 and cnt > 0:
        avgWdth = ttlWdth / cnt
        buffWdth = avgWdth / 2
        return buffWdth
    else:
        return "Error in edge point calculation"

    # determine buffer size from original dataset
        # this will require compiling and array of edge points
        # look at swath width column of edge points and determine average value
        # buffer by one half of determined average swath width column

    # first test concave_hull on harvest dataset and determine if polygon edge is is placed on top of
    # edge points in point dataset
        # if this is proven to be true, then check each point for its correspondence to the polygon edge.
        # if the point falls on the polygon edge,
        # take this point into account when calculating width average. will need to set a cnt variable and
        # width variable that is then totalized to calculate an overall average width. halve this average
        # width value and apply the result as a buffer to the concave_hull polygon. other method could be to check


def bufferPoly(polygon, bufferSize, concaveHull):
  # convert buffer size from feet to meters
    buffWdth = bufferSize * 0.3048
  # apply buffer to concave polygon
    buffHull = concaveHull.buffer_in_meters(polygon, buffWdth)

    return buffHull


def write_to_file(geometryObject, outputFile):
    #crs = pycrs.parse.from_epsg_code(4326)
    #crs.name = 'GCS_WGS_1984'

    #crsOut = outputFile[0:(len(outputFile)-4)] + '.prj'

    shpOut = shp.Writer(outputFile, shapeType=5)

    shpOut.field('id', 'C')
    shpOut.record('0')
    shpOut.shape(geometryObject)

    prjFile = '/home/ymp1zkxjtgya/testData/input/wgs84Prj/WGS84.prj'
    with open(prjFile, 'rb') as prjInfile:
        lines = prjInfile.readlines()
        prjInfile.close()

    prjOut = outputFile[0:(len(outputFile)-4)] + '.prj'

    with open(prjOut, 'wb')as prjOutfile:
        prjOutfile.writelines(lines)
        prjOutfile.close()

    #prj = open(crsOut,'w')
    # prj.write(crs.to_esri_wkt())
    # prj.close()

    shpOut.close()
