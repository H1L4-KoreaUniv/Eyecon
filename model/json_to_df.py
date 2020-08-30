# -*- coding: utf-8 -*-
# title           : json_to_df.py
# description     : Make datarame from json file in order to use along whole analysis.
# date            : 20200830
# python_version  : 3.8.3
# ==============================================================================

import json
import pandas as pd
import re
import numpy as np

def make_df(path_json):
    """
    Make dataframe from json file in order to use along whole analysis.
    ----------
    - Parameters
    
    path_json: str
        json file`s path.
    ----------
    - Returns
    
    dataframe: DataFrame
        dataframe with seven columns.
    """
    with open(path_json) as file_json:
        data_json = json.load(file_json)

    dataframe = pd.DataFrame()
    dataframe['subject'] = list(''.join(re.compile('[A-Z]').findall(x['subject'])) for x in data_json['data'])
    dataframe['frame_name'] = list(x['video_name'].split('.')[0]+'_frame'+str(x['frame_num']) for x in data_json['data'])
    dataframe['label'] = list(x['label'] for x in data_json['data'])
    dataframe['img_face'] = list(x['faceimg_name'] for x in data_json['data'])
    dataframe['img_eyeleft'] = list(x['eyeimg_name'][0] for x in data_json['data'])
    dataframe['img_eyeright'] = list(x['eyeimg_name'][1] for x in data_json['data'])
    dataframe['vec_headpose'] = list([(np.array(list(x['head_pose'].values())).astype('float')) for x in data_json['data']])
    
    return dataframe