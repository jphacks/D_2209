#!/usr/bin/env python3
from flask import *
import os
import requests
import numpy as np
import sys
import time
import json
from PIL import Image
import pandas as pd

import torch
from torch.nn import CosineSimilarity

import torchvision.transforms as T
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.models.feature_extraction import create_feature_extractor

from env import GOOGLE_MAP_API_KEY

### Torch ------------------------------------

pickle_file_path = './satellite_resnet18/out/features.pkl'
out_dir = './satellite_resnet18/out/'

device = torch.device("cuda:0")

# pre-load calculated features
df = pd.read_pickle(pickle_file_path)
embed_features_np = np.vstack(df['feature'].values)
embed_features = torch.from_numpy(embed_features_np).to(device)


def extract_features(img_list):
    preprocess = T.Compose([
        T.CenterCrop(224),
        T.ToTensor(),
    ])

    input_images = torch.stack([preprocess(img) for img in img_list]).to(device)

    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1).cuda()
    feature_extractor = create_feature_extractor(model, {"avgpool": "feature"})

    fea_dict = feature_extractor(input_images)
    
    del model
    
    return fea_dict['feature']


def search_like_areas(user_img):
    with torch.inference_mode():
        user_f = extract_features([user_img]).squeeze(3).squeeze(2)
    
    user_f_expanded = user_f.expand(embed_features.shape[0], 512)
    

    
    cos_sim = CosineSimilarity(dim=1)
    sim_tensor = cos_sim(user_f_expanded, embed_features)
    
    recommend_num = 100
    recommend_args = torch.argsort(sim_tensor, descending=True)[:recommend_num].to('cpu').detach().numpy().copy()
    
    torch.cuda.empty_cache()
    
    rec_p = [[float(df.index[r].split(',')[0]), float(df.index[r].split(',')[1][:-4])] for r in np.random.choice(recommend_args, 10, replace=False)]
    return [{"lat": rec[0], "lng": rec[1]} for rec in rec_p]

### Google API ---------------------------------

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


def download_satellite_img(target_center):
    params['center'] = f'{target_center["lat"]:.6f},{target_center["lng"]:.6f}'
    ret = requests.get(api_url, params=params)

    with open(out_dir + params['center'] + '.png', 'wb') as f:
        f.write(ret.content)
    
    print(out_dir + params['center'] + '.png')
    
    user_img = Image.open(out_dir + params['center'] + '.png').convert('RGB')
    return user_img

### Flask ------------------------------------

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


# recommen API
@app.route("/", methods=['post'])
def index():
    rj = request.json
    
    # 検索地点
    center = rj['points'][0]
    user_img = download_satellite_img(center)
    
    like_areas = search_like_areas(user_img)
    
    return jsonify({'count': 10, 'areas': like_areas}), 200


# Dummy json
@app.route("/dummy/", methods=['post'])
def dummy_index():
    return jsonify({"count": 10, "areas": [{"lat": 36.285451, "lng": 139.33457}, {"lat": 34.696549, "lng": 137.946496}, {"lat": 36.269451, "lng": 139.16457}, {"lat": 34.713996, "lng": 136.486291}, {"lat": 36.109776, "lng": 140.218836}, {"lat": 35.861776, "lng": 140.338836}, {"lat": 36.085451, "lng": 139.76457}, {"lat": 36.093451, "lng": 139.42457}, {"lat": 36.085776, "lng": 140.218836}, {"lat": 36.018263, "lng": 139.98638}]})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)