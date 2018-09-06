#!/usr/bin/env python

import os
import pickle
import numpy as np
import csv
from collections import defaultdict

from utils.data import *
from utils.files import makeifnotexist

if __name__ == '__main__':
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(BASE_DIR, 'data')
    save_dir = os.path.join(BASE_DIR, 'country_pics')
    pickle_dir = os.path.join(BASE_DIR, 'pickle')

    makeifnotexist(pickle_dir)

    data_files = os.listdir(data_dir)
    for data_file in data_files:
        picture_save_dir = os.path.join(save_dir, data_file)
        makeifnotexist(picture_save_dir)

        if not data_file.startswith('.'):  
            folder_dir = os.path.join(data_dir, data_file)
            folder_names = os.listdir(folder_dir)
            for folder_name in folder_names:
                pickle_data = {}
                fname = os.path.splitext(folder_name)[0]
                txt_dir = os.path.join(folder_dir, folder_name)
                f = np.loadtxt(txt_dir, delimiter=',')
            
                F = construct_flow_network(f)
                size = log_size(F)
                L = compute_l_from_f(F)        
                dis2ss = compute_dis_to_ss(L)
                
                pickle_data['origin_data'] = f
                pickle_data['F_mat'] = F
                pickle_data['L_mat'] = L
                pickle_data['size'] = size
                pickle_data['ss'] = dis2ss
    
                pickle_path = os.path.join(pickle_dir, fname) + '.pkl'
                with open(pickle_path, 'w') as f:
                    pickle.dump(pickle_data, f)
               
                print "DATA SAVED AS PICKLE FILE in %s" %(pickle_path)
