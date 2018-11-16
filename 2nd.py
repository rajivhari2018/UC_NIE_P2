import sys
sys.path.append( 'c:\\python27\\lib\\site-packages');

from pykml import parser
from qgis.core import *
from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84 
import math
from copy import deepcopy
import simplekml
kml = simplekml.Kml()
#-----------------------assumptions-----------------------

dronesnr=12;
battery=3300;
n=2;
dist_of_location=1000;#in meters



#--------------------------------------------------------------
#------------------------declaration for model-----------------

numcenter=0;
speed=6;

#--------------------------------------------------------------



file = parser.fromstring(open('C:\\Users\\Prathvi\\Desktop\prj\\codes\\qgis\\85.kml', 'r').read())

#file.Document.Placemark.Point.coordinates ==> to check once if want..

num, cor = 2,4;
cords = [[0.0 for x in range(num)] for y in range(cor)] # create empty 4*3 matrix

for x in range(cor):
	for y in range(num):
		cords[x][y]=float(str(file.Document.Placemark.Point[x].coordinates).split(',')[y]);

cordsmap=deepcopy(cords)

for i in range(cor):
	cordsmap[i].reverse()



layer = iface.addVectorLayer('I:\\TM_WORLD_BORDERS-0.3\\TM_WORLD_BORDERS-0.3.shp','test','ogr')
features=layer.featureCount()
vpr = layer.dataProvider()
poly= QgsGeometry.fromPolygonXY([[QgsPointXY(cordsmap[0][0],cordsmap[0][1]),QgsPointXY(cordsmap[1][0],cordsmap[1][1]), QgsPointXY(cordsmap[2][0],cordsmap[2][1]), QgsPointXY(cordsmap[3][0],cordsmap[3][1])]])
f=QgsFeature();
f.setGeometry(poly);
f.setAttributes([features])
vpr.addFeatures([f])

#-------------to find total area-------------------------------
p = geod.Polygon()
for pnt in cords:
	p.AddPoint(pnt[0], pnt[1])

num, perim, area = p.Compute()
area=abs(area);


#--------------------------------------------------------------
#-----------------------model----------------------------------

capacity=battery/1000*0.9;
maxtime=(capacity/8)*60*60;
maxdist=(maxtime*speed)-2*(dist_of_location);
distdrone=maxdist*dronesnr;
maxarea=n*distdrone;

numcenter=math.floor(area/maxarea)
presarea=area-numcenter*maxarea;
eacharea=presarea/dronesnr
print("_____________________________________________")
print("each drone have to cover area of ",eacharea)
print("number of extra centers required is",numcenter);
print("_____________________________________________")

# to make smaller sized total area
num, cor = 2,4;
pressize=math.sqrt(presarea)
g = geod.Direct(cords[0][0],cords[0][1], 90, pressize)
g['lat2'],g['lon2']=cords[0][0],cords[0][1];
newcords = [[0.0 for x in range(num)] for y in range(cor)]
for x in range(4):
	g = geod.Direct(g['lat2'],g['lon2'],(x+((-1)**x))*90 , pressize)	
	newcords[x][0],newcords[x][1]=g['lat2'],g['lon2']

#--------------------------------------------------------------
#--------------------side--------------------------------------

points = [[[1.0 for x in range(1)] for y in range(4)]for z in range(dronesnr)]
prevg=[0,0]
prevh=[0,0]
c=0
eachside=math.sqrt(eacharea);
g = geod.Direct(cords[0][0],cords[0][1], 90, eachside)
h = geod.Direct(cords[0][0],cords[0][1], 0, eachside)
g['lat2'],g['lon2']=cords[0][0],cords[0][1]

while h['lat2']<newcords[1][0]:
    prevg=g['lat2'],g['lon2']
    prevh=h['lat2'],h['lon2']
    while g['lon2']<newcords[1][1]:
        g= geod.Direct(g['lat2'],g['lon2'], 90, eachside)
        h= geod.Direct(h['lat2'],h['lon2'], 90, eachside)
        points[c][0]=prevh
        points[c][1]=prevg
        points[c][2]=g['lat2'],g['lon2']
        points[c][3]=h['lat2'],h['lon2']
        #g['lat2'],g['lon2']
        prevg=g['lat2'],g['lon2']
        prevh=h['lat2'],h['lon2']
        c=c+1
    g= geod.Direct(g['lat2'],cords[0][1], 0, eachside)
    h= geod.Direct(g['lat2'],g['lon2'], 0, eachside)


#--------------------------------------------------------------
kml = simplekml.Kml()
for x in range(dronesnr):
	kml.newpolygon(name=str(x), outerboundaryis=points[x])
	kml.save("C:\\Users\\Prathvi\\Desktop\\prj\\codes\\qgis\\testfile.kml")

#--------------------------------------------------------------

#----------------drawing in map--------------------------------
for x in range(dronesnr):
	poly=QgsGeometry.fromPolygonXY([[QgsPointXY(points[x][0][1],points[x][0][0]),QgsPointXY(points[x][1][1],points[x][1][0]),QgsPointXY(points[x][2][1],points[x][2][0]),QgsPointXY(points[x][3][1],points[x][3][0])]])
	f=QgsFeature();
	f.setGeometry(poly);
	f.setAttributes([features])
	vpr.addFeatures([f])

print("===============>done<====================")

#--------------------------------------------------------------

# 75.9,16.1	--- 75.9,16.4 ----- 76.2,16.4 ---- 76.2,16.1
# 16.1,75.9 --- 16.4,75.9 ----- 16.4,76.2 ---- 16.1,76.2 .9

#[[(16.010876568366573, 75.09), (16.01, 75.09), (16.009999998087924, 75.09090629591385), (16.010876566454385, 75.09090629986781)], [(16.010876566454385, 75.09090629986781), (16.009999998087924, 75.09090629591385), (16.009999996175846, 75.09181259182769), (16.0108765645422, 75.09181259973562)], [(16.0108765645422, 75.09181259973562), (16.009999996175846, 75.09181259182769), (16.00999999426377, 75.09271888774151), (16.010876562630013, 75.09271889960341)], [(16.010876562630013, 75.09271889960341), (16.00999999426377, 75.09271888774151), (16.009999992351688, 75.09362518365533), (16.010876560717826, 75.0936251994712)], [(16.011753129013393, 75.09), (16.010876560718255, 75.09), (16.01087655880607, 75.09090629986778), (16.011753127101095, 75.090906303822)], [(16.011753127101095, 75.090906303822), (16.01087655880607, 75.09090629986778), (16.010876556893887, 75.09181259973555), (16.0117531251888, 75.09181260764397)], [(16.0117531251888, 75.09181260764397), (16.010876556893887, 75.09181259973555), (16.0108765549817, 75.09271889960331), (16.011753123276502, 75.09271891146595)], [(16.011753123276502, 75.09271891146595), (16.0108765549817, 75.09271889960331), (16.010876553069515, 75.09362519947106), (16.011753121364208, 75.09362521528791)], [(16.012629689588334, 75.09), (16.011753121364645, 75.09), (16.01175311945235, 75.09090630382197), (16.01262968767593, 75.09090630777642)], [(16.01262968767593, 75.09090630777642), (16.01175311945235, 75.09090630382197), (16.011753117540053, 75.09181260764392), (16.01262968576352, 75.09181261555283)], [(16.01262968576352, 75.09181261555283), (16.011753117540053, 75.09181260764392), (16.011753115627755, 75.09271891146585), (16.01262968385111, 75.09271892332923)], [(16.01262968385111, 75.09271892332923), (16.011753115627755, 75.09271891146585), (16.011753113715457, 75.09362521528779), (16.012629681938705, 75.09362523110562)], [[0.0], [0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0], [0.0]]]
#poly=QgsGeometry.fromPolygonXY([[QgsPointXY(points[0][0][1],points[0][0][0]),QgsPointXY(points[0][1][1],points[0][1][0]),QgsPointXY(points[0][2][1],points[0][2][0]),QgsPointXY(points[0][3][1],points[0][3][0])]])
