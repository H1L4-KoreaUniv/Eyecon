# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 21:51:02 2020

@author: 이다혜
"""

import json
import pandas as pd
import numpy as np


# metadata가 저장된 json 파일을 받아 dataframe으로 바꿔주는 함수
def json_to_dataframe(jsonpath):
    
    with open(jsonpath) as json_file:
        meta = json.load(json_file)
        
    meta_df = pd.DataFrame()
    meta_df['frame_name'] = list(x['facelmname'][:-11] for x in meta['data'])
    meta_df['video_name'] = list(x['file_name'] for x in meta['data'])
    meta_df['subject'] = list(''.join(re.compile('[A-Z]').findall(x['subject'])) for x in meta['data'])
    meta_df['head_pose'] = list([(np.array(list(x['head_pose'].values())).astype('float')) for x in meta['data']])
    meta_df['face_landmarks'] = list([(x['face_landmarks']) for x in meta['data']])
    meta_df['faceimg_name'] = list(x['facelmname'] for x in meta['data'])
    meta_df['lefteyeimg_name'] = list(x['eyelmname'][0] for x in meta['data'])
    meta_df['righteyeimg_name'] = list(x['eyelmname'][1] for x in meta['data'])
    meta_df['label'] = list(x['label'] for x in meta['data'])
    
    return meta_df

