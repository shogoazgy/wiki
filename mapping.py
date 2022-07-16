import csv
import pandas as pd
import folium
import re
import base64
import pyproj

def to_xy(lat, lon):
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")
    y,x = pyproj.transform(EPSG4612, EPSG2451, lon, lat)
    return [x, y]

def calculate_distance(x0, y0, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    r = dx**2 + dy**2
    tt = -(dx * (x1 - x0) + dy * (y1 - y0))
    if (tt < 0):
        return (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)
    elif tt > r:
        return (x2 - x0) * (x2 - x0) + (y2 - y0) * (y2 - y0)
    return (dx * (y1 - y0) - dy * (x1 - x0))**2 / r

def map_plot(filename='map',data_file='test.csv'):
    data_dict = pd.read_csv(data_file, index_col=0, squeeze=True).to_dict()
    hino = [35.661221,139.365734]
    map = folium.Map(location=hino, zoom_start=10)
    folium.Marker(location=hino,popup='東京都立大日野キャンパス').add_to(map)
    """
    dist_name = input()
    if data_dict['リード文'][dist_name] is None:
        print('error')
        return
    else:
        pass
    
    for dist in data_dict['リード文']:
        dist_name = dist
        hino = [35.661221,139.365734]
        map = folium.Map(location=hino, zoom_start=10)
        folium.Marker(location=hino,popup='東京都立大日野キャンパス').add_to(map)
        dist_coordinates = data_dict['緯度経度'][dist_name].split(',')
        dist_lat = float(dist_coordinates[0])
        dist_lon = float(dist_coordinates[1])
        
        encoded = base64.b64encode(open(dist_name + '_tfidf.png', 'rb').read())
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = folium.IFrame(html(encoded.decode('utf-8')), width=300, height=200)
        popup = folium.Popup(iframe, max_width=1000)
        folium.Marker(location=[dist_lat, dist_lon],popup=popup).add_to(map)
        folium.PolyLine(locations=[hino,[dist_lat, dist_lon]]).add_to(map)
        
        dist_x, dist_y = to_xy(dist_lat, dist_lon)
        hino_x, hino_y = to_xy(hino[0], hino[1])
        m = 1.7e+15
        m_name = None
        for name in data_dict['緯度経度']:
            if name == dist_name:
                continue
            d_coordinates = data_dict['緯度経度'][name].split(',')
            d_lat = float(d_coordinates[0])
            d_lon = float(d_coordinates[1])
            d_x, d_y = to_xy(d_lat, d_lon)
            distance = calculate_distance(d_x, d_y, dist_x, dist_y, hino_x, hino_y)
            if m > distance:
                m = distance
                m_name = name
        d_coordinates = data_dict['緯度経度'][m_name].split(',')
        d_lat = float(d_coordinates[0])
        d_lon = float(d_coordinates[1])
        folium.Marker(location=[d_lat, d_lon],popup='寄り道: ' + m_name, icon=folium.Icon(color='red')).add_to(map)
        """
    map.save(filename + '.html')
    
if __name__ == "__main__":
    map_plot()