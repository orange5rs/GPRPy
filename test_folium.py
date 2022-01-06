# https://bikeshbade.com.np/tutorials/Detail/?title=Generate%20Slope%20Elevation%20data%20from%20SRTM%20-%20Python%20API&code=7

# import Google earth engine module
import ee
import folium

#Authenticate the Google earth engine with google account
ee.Authenticate()
ee.Initialize()
#Define year
startyear = 2019;
endyear = 2019;

#Create the Date object
startdate = ee.Date.fromYMD(startyear,1,1);
enddate = ee.Date.fromYMD(endyear,12,1);

# Define a method for displaying Earth Engine image tiles on a folium map.
def add_ee_layer(self, ee_object, vis_params, name):
    
    try:    
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):    
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)
    except:
        print("Could not display {}".format(name))
        
# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

#Load the SRTM image.
srtm = ee.Image('USGS/SRTMGL1_003');

#Apply slope algorithm to an image.
slope = ee.Terrain.slope(srtm);

#Scale and Projection
scale = srtm.projection().nominalScale();

#styling
visualization_params = {min: 0, max: 10000, 'palette': [
    '3ae237', 'b5e22e', 'd6e21f', 'fff705', 'ffd611', 'ffb613', 'ff8b13',
    'ff6e08', 'ff500d', 'ff0000', 'de0101', 'c21301', '0602ff', '235cb1',
    '307ef3', '269db1', '30c8e2', '32d3ef', '3be285', '3ff38f', '86e26f'
  ],};


# Add the data to the map object.
my_map.add_ee_layer(srtm, visualization_params ,"DEM");
my_map.add_ee_layer(slope, visualization_params , "slope");

# Display the map.
display(my_map)


my_map.save('index.html')
