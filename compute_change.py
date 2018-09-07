import os
import pickle
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

from utils.data import min_max_norm_for_vec, load_industry_infos


def load_data(path):
    with open(path, 'r') as f:
        data = pickle.load(f)
    arr = data['ss']
    f = data["origin_data"]
    total_output = f[f.shape[0]-1, 0:33] 
    total_output = total_output / np.sum(total_output)
    new_arr = min_max_norm_for_vec(arr)
    return new_arr, total_output

def define_change(arr1, arr2, weights):
    assert arr1.shape == arr2.shape
    
    # define change
    result = np.zeros((len(arr1),5))
    for i in range(len(arr1)):
        result[i, 0] = arr1[i, 0] - arr2[i, 0]
        result[i, 1] = arr1[i, 1] - arr2[i, 1] 
        result[i, 2] = np.square(arr1[i, 0] - arr2[i, 0]) 
        result[i, 3] = np.square(arr1[i, 1] - arr2[i, 1])
        result[i, 4] = np.sqrt(np.square(arr1[i, 0] - arr2[i, 0]) + np.square(arr1[i, 1] - arr2[i, 1]))
   
    # define change of country as weighted sum of industry change
    coefficent = 0
    for i in range(len(arr1)):
        coefficent += result[i, 4] * weights[i]
    
    return result, coefficent

def define_distance(arr1):
    # define change of industry as euclidean distance
    result = np.zeros(len(arr1))
    for i in range(len(arr1)):
        result[i] = np.sqrt(np.square(arr1[i, 0]) + \
                            np.square(arr1[i, 1]))
    return result


if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(BASE_DIR, 'pickle')
    industry_info = load_industry_infos(os.path.join(BASE_DIR, 'files', 'abb_label.csv'))

    countries = sorted(set([i.split('_')[0] for i in os.listdir(data_dir)]))
    years = ['1995', '2011']

    # fetch data
    data_dic = {}
    for country in countries:
        data_dic[country] = []
        for data_file in sorted(os.listdir(data_dir)):
            cny = os.path.splitext(data_file)[0].split("_")[0]
            yer = os.path.splitext(data_file)[0].split("_")[1]
            if cny == country and yer in years:
                data_norm, weights = load_data(os.path.join(data_dir, data_file))
                data_dic[country].append({yer: [data_norm, weights]})

    # define change and rank industry
    
    t = []
    result = {}
    industry = {}
    for ckey in countries:
        print len(data_dic[ckey])
        arr1 = data_dic[ckey][0].values()[0][0]
        arr2 = data_dic[ckey][1].values()[0][0]
        weight = data_dic[ckey][1].values()[0][1]
        scores, tscores = define_change(arr1,arr2,weight)
        t.append(tscores)
        idx = sorted(range(len(scores)), key=lambda k:scores[:, 4][k])
        inlabel = [industry_info['abb'][i] for i in idx][::-1]
        result[ckey] = {"scores":scores, "rank":inlabel}
        industry[ckey] = inlabel[:10]
    

#    # rank countries which have undergone dramatic chagne

#    idx_c = sorted(range(len(t)), key=lambda k:t[k])
#    rank_c = [countries[i] for i in idx_c][::-1]
#    print rank_c
    
        
    counter_list = []
    for row in industry.values():
        for cnt in row:
            counter_list.append(cnt)

    c = Counter(counter_list)
    
    print "first 10 industries which dramatic changed from %s to %s" %(years[0], years[1])
    print c

