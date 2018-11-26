												GRID MARKING 

final2.py is the final integrated code

INPUT OF THE CODE:
Co-ordinates of the disaster area is provided as the input to the code from the command centre in kml format.

OUTPUT OF THE CODE:
Coordinates of the subgrids based on the mathematical model being used is the output.

MODULES USED:
Python language is used for coding.

QGIS:It is a geographic platform that supports viewing,editing and analysis of geospatial data.Open street maps are taken into consideration.  
Output of the code is in the kml format.

KML is the keyhole markup language is an XML notation for expressing geographic data.

Pykml format is implied.

Geographic libraries are used which are the python libraries for geospatial data.
Geodesic which gives the shortest route between two points on earth's surface.
WGS84-GPS uses the World Geodetic System as its reference coordinate system.


ASSUMPTIONS:
1.Number of drones.
2.Battery life of the drone.
3.Distance the drone can cover




FUNCTIONS USED IN THE CODE:
1.exprt:to export the coordinates in a kml format
2.findTotalarea:to find the total area of the master grid
3.findarea:to find the area of smaller grids after applying the line division algorithm

-	Based on the coordinates from the command centre,decision takes place whether the master grid can be a square or 	 any polygon.
-	In the model the capacity of the drone is calculated.The maximum distance it can cover is calculated.The total 		distance which can be covered by each drone is calculated.
-	Then finally the maximum area that can be covered using the given number of drones is found out.
-	The number of extra centres required to cover that particular area is given by the numcenter value.
-	Using the line division algorithm the master grids is divided into smaller grids.

Finally,the coordinates of each subgrids is obtained as the output which is in a kml format.
