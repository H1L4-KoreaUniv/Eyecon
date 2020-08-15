#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json # import json module

# with statement
with open('/Users/hong-yujin/Downloads/test/metadata.json') as json_file:
    json_data1 = json.load(json_file)

with open('/Users/hong-yujin/Downloads/test/metadata2.json') as json_file:
    json_data2 = json.load(json_file)

    
json_data1['data'].extend(json_data2['data'])

with open('/Users/hong-yujin/Downloads/test/metadata_merge.json', 'w') as outfile:
    json.dump(json_data1, outfile,indent=4)


# In[ ]:




