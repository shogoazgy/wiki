import csv
import pandas as pd
import folium
import re
import base64
import pyproj

def cal_distance(lat1, lon1, lat2, lon2):
    grs80 = pyproj.Geod(ellps='GRS80')
    azimuth, reazimuth, distance = grs80.inv(lon1, lat1, lon2, lat2)
    return distance

if __name__ == '__main__':
    asakusa_akiba_d = cal_distance(35.69833333333333, 139.77305555555557, 35.71202777777778, 139.7966898148148)
    print(str(asakusa_akiba_d) + 'm')
    skytree_shibuya_d = cal_distance(35.710023148148146, 139.81083333333333,35.659935185185184, 139.7030185185185)
    print(str(skytree_shibuya_d) + 'm')



