# import folium package
import folium

my_map3 = folium.Map(location = [28.5011226, 77.4099794],
										zoom_start = 15)

# Pass a string in popup parameter
folium.Marker([28.5011226, 77.4099794],
			popup = ' Geeksforgeeks.org ').add_to(my_map3)


folium.Marker([28.40, 77.4099794],
			popup = ' Geeksforgeeks.org ').add_to(my_map3)


folium.Marker([28.30, 77.4099794],
			popup = ' Geeksforgeeks.org ').add_to(my_map3)


my_map3.save(" my_map3.html ")
