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





def exprt(toexp):
    kml = simplekml.Kml()
    for x in range(len(toexp)):
        kml.newpolygon(name=str(x), outerboundaryis=toexp[x])
        kml.save("C:\\Users\\Prathvi\\Desktop\\prj\\codes\\testfile.kml")

def exprt2(toexp):
    kml = simplekml.Kml()
    for x in range(len(toexp)):
        kml.newpolygon(name=str(x), outerboundaryis=toexp[x])
		kml.save("C:\\Users\\Prathvi\\Desktop\\prj\\codes\\testfile2.kml")




def findTotalArea(pts):
	p = geod.Polygon()
	for pnt in pts:
		p.AddPoint(pnt[0], pnt[1])
	num, perim, area = p.Compute()
	area=abs(area);
	return area

def rectify(point):
	y=len(point)
	points=[]
	for i in range(1,y,2):
		points.append(point[i])
	points.append(point[0])
	for i in range(y-1,1,-2):
		points.append(point[i])
	return points


def findarea(point):
	y=len(point)
	points=[]
	for i in range(1,y,2):
		points.append(point[i])
	points.append(point[0])
	for i in range(y-1,1,-2):
		points.append(point[i])
	p = geod.Polygon()
	for pnt in points:
		p.AddPoint(pnt[0], pnt[1])
	num, perim, area = p.Compute()
	area=abs(area);
	return area
#---------------------------------------------------------












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
newcords[0],newcords[2]=newcords[2],newcords[0]

cos=newcords;
num=dronesnr #num of drones
reqarea=findTotalArea(cos)/num;
toexp=[]

for x in range(0,(num-1)):
    x=len(cos)-1
    points=[]
    points.append(cos[x])
    points.append(cos[(x-1)%(x+1)])
    points.append(cos[(x+1)%(x+1)])
    y=len(points)-1
    max2=points[y]
    max1=points[y-1]	
    min1=points[y-2]
    min2=points[y-2]
    area=findarea(points)
    while ((area-reqarea)<-0.01 or (area-reqarea)>0.01):
        if area<reqarea:
            min1=points[1]
            min2=points[2]
            if min1==max1:
                points.insert(1,cos[(x-2)%(x+1)])
                max1=points[1]
            if min2==max2:
                points.insert(2,cos[(x+2)%(x+1)])
                max2=points[2]
            points[2]=max2
            points[1]=max1
        else:
            max1=points[1]
            max2=points[2]
            points[1]=[float((points[1][0]+min1[0])*0.5),float((points[1][1]+min1[1])*0.5)]
            points[2]=[float((points[2][0]+min2[0])*0.5),float((points[2][1]+min2[1])*0.5)]
        area=findarea(points)
        print(area)
    print("--------------------------------------------------")
    print(points)
    #export(points)
    toexp.append(rectify(points));
    y=len(points)
    for x in range(0,y):
        try:
            cos.remove(points[x])
            print("removed")
        except:
            cos.append(points[x])
            print("exception")
    print("--------------------------------------------------")

toexp.append(cos);
exprt(toexp)
mapcords=[]
mapcords=deepcopy(toexp)

for i in range(len(mapcords)):
    for j in range(len(mapcords[i])):
        mapcords[i][j]=mapcords[i][j][::-1]

#converted to map equ
exprt2(mapcords)