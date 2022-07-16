import requests
import re
import csv
def text_normalize(text):
        text = ''.join(text.splitlines())
        return text

def get_coordinates(address):
    url = 'https://map.yahooapis.jp/geocode/V1/geoCoder'
    params = {
        'appid': 'dj00aiZpPVZRaFJuVUhNNmRtZyZzPWNvbnN1bWVyc2VjcmV0Jng9OTk-',
        'query': address,
        'output' :'json',
    }
    r = requests.get(url, params=params)
    res = r.json()
    coordinates = res['Feature'][0]['Geometry']['Coordinates'].split(',')
    return [coordinates[1], coordinates[0]]
data_list = []
with open('wikidata2_hand.csv', encoding="shift_jis") as file:
    reader = csv.reader(file)
    for row in reader:
        data_list.append(row)
for row in data_list:
    if row[4] == '住所':
        continue
    print(row[4])
    if row[4] != 'None':
        coordinates = get_coordinates(text_normalize(row[4]))
        row[3] = coordinates[0] + ',' + coordinates[1]
    else:
        dist_coordinates = row[3].split(' ')
        dist_lat_nums = re.findall(r'\d+', dist_coordinates[0])
        dist_lat = 0
        for i in range(len(dist_lat_nums)):
            c = i
            lat = float(dist_lat_nums[i])
            while True:
                if c == 0:
                    break
                lat /= 60
                c -= 1
            dist_lat += lat
        dist_lon_nums = re.findall(r'\d+', dist_coordinates[1])
        dist_lon = 0
        for i in range(len(dist_lon_nums)):
            c = i
            lon = float(dist_lon_nums[i])
            while True:
                if c == 0:
                    break
                lon /= 60
                c -= 1
            dist_lon += lon
        row[3] = str(dist_lat) + ',' + str(dist_lon)
with open('test.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data_list)
