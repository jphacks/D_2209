#!/usr/bin/env python3
from PIL import Image
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import islice
import sys
import os

import torch
from torch.nn import CosineSimilarity

import torchvision.transforms as T
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.models.feature_extraction import create_feature_extractor

pickle_file_path = './out/features.pkl'
image_dir = './out/'

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def load_images(df):
    img_dict = {}

    print('image loading...')

    for f in os.listdir(image_dir):
        if f.endswith('.png'):
            if f not in df.index:
                img_dict[f] = Image.open(image_dir + f).convert('RGB')

    print(f'NEW {len(img_dict)} images found.')

    return img_dict


def extract_features(img_list):
    preprocess = T.Compose([
        T.CenterCrop(224),
        T.ToTensor(),
    ])

    input_images = torch.stack([preprocess(img) for img in img_list])

    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    feature_extractor = create_feature_extractor(model, {"avgpool": "feature"})

    fea_dict = feature_extractor(input_images)
    
    return fea_dict['feature']


def calc_cos_sim(features):
    cos_sim = CosineSimilarity(dim=0)


def dict_chunks(data, size):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}


if __name__ == '__main__':
    if sys.argv[1] == 'init':
        df = pd.DataFrame(columns=['longitude', 'latitude', 'feature',])
        if os.path.isfile(pickle_file_path):
            print('すでにファイルが存在しています．')
            exit()
        else:
            df.to_pickle(pickle_file_path)
    elif sys.argv[1] == 'show':
        df = pd.read_pickle(pickle_file_path)
        print(f'{len(df)} records found.')
        print(df.head())
    elif sys.argv[1] == 'calc':
        df = pd.read_pickle(pickle_file_path)
        name_list, img_list = load_images(df)

        try:
            batch = 1000
            img_list_set  = [img_list[i:i+batch]  for i in range(0, len(img_list), batch)]

            with torch.inference_mode():
                features = [extract_features(img_set).to('cpu').detach().numpy().copy() for img_set in tqdm(img_list_set)]
            torch.cuda.empty_cache()

            features = np.concatenate(features)

            for i in tqdm(range(len(features))):
                df.loc[name_list[i]] = [
                        name_list[i].split(',')[0],
                        name_list[i].split(',')[1][:-4],
                        features[i].squeeze(2).squeeze(1)
                ]
        
            df.to_pickle(pickle_file_path)
        except KeyboardInterrupt:
            # 途中状態でも保存
            df.to_pickle(pickle_file_path)

