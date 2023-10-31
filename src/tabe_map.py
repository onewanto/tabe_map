import os
import time
import urllib.parse
import urllib.request
import requests
from datetime import datetime
from random import random
from xml.etree.ElementTree import ElementTree

import folium
import numpy as np
import pandas as pd
from tqdm import tqdm


class TabeMap:
    def __init__(self):
        self.init_path()

    def init_path(self):
        self.is_debug = False
        self.output_path = './static'
        os.makedirs(self.output_path, exist_ok=True)

    def get_location(self, address):
        self.address = address
        url_geocoding = f'https://www.geocoding.jp/api/?q={urllib.parse.quote(address)}'

        # 住所から緯度経度の取得（Geocoding API）
        f = urllib.request.urlopen(url_geocoding)
        et = ElementTree()
        et.parse(f)
        self.lat = et.find("./coordinate/lat").text
        self.lng = et.find("./coordinate/lng").text
        return float(self.lat), float(self.lng)

    def test_get_location(self, address):
        self.lat = 35.4506175296651 + random() / 5 - 0.1
        self.lng = 139.63423904446174 + random() / 5 - 0.1
        return self.lat, self.lng

    def load_data(self, uploaded_file):
        self.df = pd.read_csv(uploaded_file)

    def init_location(self):
        self.locations = {'lat': [], 'lng': []}
        for idx in tqdm(self.df.index):
            if self.is_debug:
                lat, lng = self.test_get_location(self.df.at[idx, "address"])
            else:
                time.sleep(2)
                lat, lng = self.get_location(self.df.at[idx, "address"])
            self.locations['lat'].append(lat)
            self.locations['lng'].append(lng)

    def color_map(self, rating):
        # ratingの値を3.0~4.0の範囲に収める
        rating = min(4.0, max(3.0, rating))
        colors = ['red', 'red', 'lightred', 'lightred',
                  'orange', 'orange',
                  'lightgreen', 'green',
                  'lightblue', 'blue', 'darkblue']
        return colors[int(10 - (rating - 3.0) * 10)]

    def run(self, uploaded_file) -> folium.Map:
        self.load_data(uploaded_file)
        self.init_location()
        print(self.locations)

        figure = folium.Figure(width=1000, height=900)
        loc_central = [np.mean(self.locations['lat']), np.mean(self.locations['lng'])]
        maps = folium.Map(location=loc_central,
                          zoom_start=11).add_to(figure)
        for i in self.df.index:
            shop_info = self.get_shop_info(self.df.loc[i])
            iframe = folium.IFrame(shop_info)
            popup = folium.Popup(iframe, min_width=400, max_width=400)
            location = [self.locations['lat'][i], self.locations['lng'][i]]
            marker = folium.Marker(location=location,
                                   icon=folium.Icon(color=self.color_map(self.df.at[i, "rating"]),
                                                    icon="info-sign"),
                                   popup=popup)
            marker.add_to(maps)

        # 保存
        maps.save(os.path.join(self.output_path, 'map.html'))

    def get_shop_info(self, data):
        target_keys = ['name', 'address', 'budget', 'genre', 'rating', 'memo']

        for key in target_keys:
            if key not in data:
                data[key] = '<no data>'

        return f"""
店名：{data['name']}<br>
住所：{data['address']}<br>
予算：{data['budget']}<br>
ジャンル：{data['genre']}<br>
評価：{data['rating']}<br>
備考：{data['memo']}"""
