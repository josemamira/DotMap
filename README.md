# DotMap
Dot density map plugin for Qgis 

Screenshot:
![alt text](https://github.com/josemamira/DotMap/blob/master/doc/Selecci%C3%B3n_156.png "Plugin")
### Description
Easy plugin to make a density layer from a polygon layer with an integer field.

### Result
E![alt text](https://github.com/josemamira/DotMap/blob/master/doc/Selecci%C3%B3n_157.png "Result")

### Version
1.0

### Autor
José Manuel Mira Martínez

### Steps
1. Select a polygon layer from combo 1
2. Select a numeric field from combo 2. Then the min and max value data are filled.
3. Make a "simulation" to know the numbers of point in polygon with min and max value
4. Clic on "OK" button to run the algoritm

### Thanks
This plugin is based in Chapter 8: "Creating a dot density map" from book "QGIS Python Programming Cookbook", author: Joel Lawhead

### Limitations
For each polygon, the plugin gets its box (minx, maxx, miny, maxy). Then, divide the value of the attribute of the field selected by the user's divisor to know the number of points per polygon.
For each point, the algorithm generates a random point included in the table. Next, it verify if the point is inside the polygon, and then this is designed as a candidate.
If the geometry is a multipolygon with many islands the algorithm slows down because the spatial box is very large, and the chances of the point falling is an island is very small.

### Notes
There are two folder, each one for Qgis 2.X or Qgis 3.X

### Tested
Tested in Linux box with Qgis 2.14, 2.18 and 3.03
