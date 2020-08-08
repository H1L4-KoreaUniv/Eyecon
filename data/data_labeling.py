#!/usr/bin/env python
# coding: utf-8

import os
import json
from collections import OrderedDict

path_dir = 'your_path' # path with image
file_list = os.listdir(path_dir)

data = []
for i in file_list:
    file_data = OrderedDict()
    file_data['file_name'] = i
    file_data['label'] = i[0]
    data.append(file_data)
data
data_dict = {}
data_dict['data'] = data
data_dict

# print(json.dumps(data_dict, ensure_ascii=False, indent='\t'))

with open('save_path/data_label.json', 'w', encoding='utf-8') as make_file:
    json.dump(data_dict, make_file, ensure_ascii=False, indent='\t')
