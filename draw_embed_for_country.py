#!/usr/bin/env python

import os
import pickle
from collections import defaultdict

from utils.data import min_max_norm_for_vec, load_industry_infos
from utils.files import makeifnotexist
from utils.draw import plot_embed_for_country

if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    infos_dir = os.path.join(BASE_DIR, 'files', 'abb_label.csv')
    industry_infos = load_industry_infos(infos_dir)

    pickle_dir = os.path.join(BASE_DIR, 'pickle')
    filelist = os.listdir(pickle_dir)
    for datafile in filelist:
        if datafile.endswith('.pkl'):
            fname = datafile[:-4]
            pics_save_dir = os.path.join(BASE_DIR, 'pics_country')
            makeifnotexist(pics_save_dir)
            pics_save_path = os.path.join(pics_save_dir, fname)

            with open(os.path.join(pickle_dir, datafile), 'r') as f:
                data = pickle.load(f)

            dis2ss_norm = min_max_norm_for_vec(data['ss'])
            size = data['size']
            plot_embed_for_country(pics_save_path, fname, dis2ss_norm, size, industry_infos)
            

