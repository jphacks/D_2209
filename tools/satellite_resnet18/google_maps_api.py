#!/usr/bin/env python3

import os
import requests

api_url = 'https://maps.googleapis.com/maps/api/staticmap'
params = {
    'key': 'API_KEYS',
    'size': '256x256',
    'center': '35.082962,135.902277',
    'zoom': '15',
    'maptype': 'satellite',
    'scale': '1',
}

ret = requests.get(api_url, params=params)
with open('hoge.png', 'wb') as f:
  f.write(ret.content)