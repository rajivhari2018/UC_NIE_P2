import sys

sys.path.append('C:\\users//prathvi//anaconda3//lib//site-packages')
sys.path.append('I:\\mine//qgis//apps//qgis//python')
sys.path.append('I://mine//qgis//apps//qgis//.//python')
sys.path.append('I:\\mine//qgis//apps//Python27//Lib//site-packages')
import simplekml;
import csv;

filenam = csv.reader(open('geodata.csv', 'r'));

kml = simplekml.Kml();
#adding points



for row in filenam:
    point = kml.newpoint();
    point.name=row[0];
    point.coords= [(row[2],row[3])]


# adding lines
line = kml.newlinestring(name="line");
line.coords = [(-122.364383, 37.824664, 50), (-122.364152, 37.824322, 50)]
line.altitudemode = simplekml.AltitudeMode.relativetoground
kml.save('mykml.kml');
