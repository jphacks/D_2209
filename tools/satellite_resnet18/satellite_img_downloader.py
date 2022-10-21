#!/usr/bin/env python3

from asyncio import wait_for
import os
from turtle import right
import requests
import numpy as np
from tqdm import tqdm
import sys
import time

from env import GOOGLE_MAP_API_KEY

api_url = 'https://maps.googleapis.com/maps/api/staticmap'
params = {
    'key': GOOGLE_MAP_API_KEY,
    'size': '230x230',
    'center': '0,0',
    'zoom': '15',
    'maptype': 'hybrid',
    'style': 'feature:all|element:labels|visibility:off',
    'scale': '1',
}

lat_delta = -0.008
lon_delta = 0.01
out_dir = './out/'
download_interval = 0.1

def download_img(lat, lon, zoom=15):
    params['zoom'] = zoom
    params['center'] = f'{lat:.6f},{lon:.6f}'

    ret = requests.get(api_url, params=params)
    tqdm.write(out_dir + params['center'] + '.png')

    with open(out_dir + params['center'] + '.png', 'wb') as f:
        f.write(ret.content)


def download_area_map_grid(left_top, right_buttom):
    for _lat in tqdm(np.arange(left_top[0], right_buttom[0], lat_delta)):
        for _lon in tqdm(np.arange(left_top[1], right_buttom[1], lon_delta), leave=False):
            download_img(_lat, _lon)
            time.sleep(download_interval)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f'Usage: {sys.argv[0]} 開始緯度 開始経度 終了緯度 終了経度')
        exit()
    else:
        start_point = (float(sys.argv[1]), float(sys.argv[2]))
        fin_point   = (float(sys.argv[3]), float(sys.argv[4]))

        print(f'開始地点:{start_point}')
        print(f'終了地点:{fin_point}')
        print(f'概算リクエスト回数：{int((start_point[0]-fin_point[0])/lat_delta * (start_point[1]-fin_point[1])/lon_delta)}回')

        # 安全対策
        print(f'2秒後にダウンロードを開始します')
        time.sleep(2)

        download_area_map_grid(start_point, fin_point)
