# importing pygmaps
import pygmaps

# list of latitudes
latitude_list = [30.3358376, 30.307977, 30.3216419, 30.3427904, 30.378598, 30.3548185, 30.3345816, 30.387299,
                 30.3272198, 30.3840597, 30.4158, 30.340426, 30.3984348, 30.3431313, 30.273471]

# list of longitudes
longitude_list = [77.8701919, 78.048457, 78.0413095, 77.886958, 77.825396, 77.8460573, 78.0537813, 78.090614,
                  78.0355272, 77.9311923, 77.9663, 77.952092, 78.0747887, 77.9555512, 77.9997158]

mymap3 = pygmaps.maps(30.3164945, 78.03219179999999, 15)

for i in range(len(latitude_list)):
    # add a point into a map
    # 1st argument is latitude
    # 2nd argument is longitude
    # 3rd argument is colour of the point showed in thed map
    # using HTML colour code e.g.
    # red "# FF0000", Blue "# 0000FF", Green "# 00FF00"
    mymap3.addpoint(latitude_list[i], longitude_list[i], "# FF0000")

mymap3.draw('pygmap3.html')