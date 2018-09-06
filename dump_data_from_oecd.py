#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
import os

from utils.files import makeifnotexist


def load_infos(BASE_DIR):

    ABBRS = os.path.join(BASE_DIR, 'files', 'COUNTRIES.txt')
    ROWCOL = os.path.join(BASE_DIR, 'files', 'row_col.csv')

    COUNTRIES = []
    with open(ABBRS, 'r') as f:
        for line in f:
            COUNTRIES.append(line.strip().split(' ')[0])
    
    with open(ROWCOL, 'r') as f:
        lines= csv.reader(f) 
        ROWS = []
        COLS = []
        for line in lines:
            COLS.append(line[1].split(':')[0])
            try:
                ROWS.append(line[0].split(':')[0])
            except IndexError:
                pass
        ROWS = ROWS[:-5]

    YEARS = range(2011, 2012)
    
    return COUNTRIES, ROWS, COLS, YEARS


if __name__ == '__main__':
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    COUNTRIES, ROWS, COLS, YEARS = load_infos(BASE_DIR)

    API_URL = "http://stats.oecd.org/restsdmx/sdmx.ashx/GetData/IOTs/TTL.{0}/all?startTime={1}&endTime={1}"
    
    for ctr in COUNTRIES:
        save_dir = os.path.join(os.path.join(BASE_DIR, 'data'), ctr)
        print save_dir
        makeifnotexist(save_dir) 
    
        for yer in YEARS:
            temp_dict = {}
            url = API_URL.format(ctr, yer)
            req = requests.get(url, timeout=20)
            req.encoding='utf-8'
            with open('./temp.xml', 'w') as f:
                f.write(req.text.encode('utf-8'))
            
            soup = BeautifulSoup(open('temp.xml'), 'xml') 
            series_tags = soup.find_all('Series')
            for series_tag in series_tags:
                value_tags = series_tag.find_all('Value')
                value = series_tag.find('ObsValue')['value']
                key_list = []
                for value_tag in value_tags:
                    if value_tag['concept'] == 'ROW':
                        key_list.append(value_tag['value'])
                    if value_tag['concept'] == 'COL':
                        key_list.append(value_tag['value'])
                temp_dict[tuple(key_list)] = float(value) 
          
            data_array = np.zeros((len(ROWS), len(COLS)))
            for i in range(data_array.shape[0]):
                for j in range(data_array.shape[1]):
                   data_array[i,j] = temp_dict[(ROWS[i], COLS[j])]
    
            fname = ctr + '_' + str(yer) + '.txt'
            txt_dir = os.path.join(save_dir, fname)
            np.savetxt(txt_dir, data_array, fmt='%f', delimiter=',' )
            print 'data save at %s' %(txt_dir)


