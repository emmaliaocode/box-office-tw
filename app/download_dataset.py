# download_dataset.py

import os.path
import pandas as pd
import requests

from module import *


# get api responses
url = 'https://data.gov.tw/api/v2/rest/dataset/94224'
request_responses = requests.get(url)
responses = request_responses.json()['result']['distribution']


# get the number of weeks of the new and the existing dataset
keep_id_list = []
for ii in range(len(responses)):
    filename = responses[ii]['resourceDescription']
    if 'JSON格式' not in filename:
        keep_id_list.append(ii)
dataset_count = len(keep_id_list)
print('week count of the new dataset:', dataset_count)

if os.path.exists('./../data/count.txt'):
    count_file = open('./../data/count.txt', 'r')
    dataset_count_old = int(count_file.readlines()[0])
    print('week count of the existing dataset:', dataset_count_old)
else:
    dataset_count_old = 0
    print('week count of the new dataset:', dataset_count_old)


# check if the dataset needed to be update
if dataset_count > dataset_count_old:
    print(get_time(), 'updating dataset...')
    data_list = response_results.shape_data_list(keep_id_list, responses)
    data = response_results.data_list_to_data_frame(data_list)
    data = response_results.fix_data_bug(data)
    data.to_csv('./../data/box_office.csv', index = False)
    count_file = open('./../data/count.txt', 'w')
    count_file.writelines(str(dataset_count))
    count_file.close()
    print(get_time(), 'dataset updated!')
elif dataset_count == dataset_count_old:
    print(get_time(), 'assigning dataset...')
    data = pd.read_csv('./../data/box_office.csv')
    print(get_time(), 'dataset assigned!')
else:
    print(get_time(), 'the new dataset has less records, please check the response results!')
