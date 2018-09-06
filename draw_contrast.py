import pickle
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import optimize

from utils.draw import get_fonts
from utils.files import makeifnotexist

# fiting curve
def fitting_f(x, A, B):
    return A*x + B 

def fiting_curve(f, x, y):
    a, b = optimize.curve_fit(f, x, y)

def compute_DC(F_mat, to_output):
    DC = np.zeros(F_mat.shape)
    cnt = 0
    for i in range(len(DC)):
        for j in range(len(DC)):
            DC[i, j] = F_mat[i,j] / to_output[j]
            
            if F_mat[i,j] == 0:
                cnt += 1
    print "%d pairs of nodes have no flows" %(cnt)
    assert(len(np.argwhere(F_mat < 0))==0)
    assert(len(np.argwhere(to_output < 0))==0)
    assert(len(np.argwhere(DC < 0))==0)
    return DC

def compute_CC(DC_mat):
    CC = np.linalg.inv(np.eye(len(DC_mat))-DC_mat) - np.eye(len(DC_mat))
    negetive_list = np.argwhere(CC < 0)
    zero_list = np.argwhere(CC == 0)
    print "there are %d negetive items, %d zeros in total" %(len(negetive_list), len(zero_list))
    return CC

def reshape_delete(mat, tu_list):
    mat_re = np.reshape(mat, (-1,1))
    new_mat = np.delete(mat_re, tu_list, axis=0)
    return new_mat

def get_tubulist():
    mat = np.reshape(np.eye(33), (-1, 1))
    tubulist =  np.argwhere(mat == 1)
    tu_list = [i[0] for i in tubulist]
    return tu_list

def get_country():
    with open('./files/COUNTRIES.txt', 'r') as f:
        lines = f.readlines()
    country_dict = {}
    for line in lines:
        item = line.strip().split(' ')
        abb = item[0]
        name = ''
        for i in item[1:]:
            name += i + ' '
        country_dict[abb] = name
    return country_dict

if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    picture_save_path = os.path.join(BASE_DIR, 'pics_compare')
    country_pickle_path = os.path.join(BASE_DIR, 'pickle')
    country_dict = get_country()
    
    makeifnotexist(picture_save_path)

    for dir_name in os.listdir(country_pickle_path):
        for i in range(1995, 2012):
            if dir_name[4:8] == str(i):
                country_key = dir_name[:3]
                country = country_dict[country_key]
                
                # wirting data
                with open(os.path.join(country_pickle_path, dir_name), 'r') as f:
                    data = pickle.load(f)
                L_mat =np.reshape(data['L_mat'][1:34, 1:34], (-1,1))
                F_mat = data['origin_data'][0:33, 0:33]
                to_output = data['origin_data'][-1, 0:33]
                    
                # compute distance    
                DC = compute_DC(F_mat, to_output)
                CC = compute_CC(DC)
                  
                # reshape and delete self loop  
                tu_list = get_tubulist() 
                L_rd = reshape_delete(L_mat, tu_list) 
                DC_rd = reshape_delete(DC.T, tu_list)
                CC_rd = reshape_delete(CC.T, tu_list)
                
                # dealing with zeros in DD_rd
                zeros_list = [i[0] for i in np.argwhere(DC_rd == 0)]
                L_rd_nz = np.delete(L_rd, zeros_list, axis=0)
                DC_rd_nz = np.delete(DC_rd, zeros_list, axis=0)
                assert len(np.argwhere(DC_rd_nz==0)) == 0
                assert len(np.argwhere(DC_rd_nz<0)) == 0

                # plot figure

                fig1, ax1 = plt.subplots(1, 1, figsize=(5,5))
                ax1.set_title(country, fontproperties=get_fonts(15)) 
                xy_1 = np.c_[np.log10(DC_rd_nz), L_rd_nz]
                ax1.scatter(xy_1[:, 0], xy_1[:, 1], c='cornflowerblue',s=30, alpha=0.7, edgecolors= 'grey')
                ax1.set_xlabel('direct consumption coefficient', fontproperties=get_fonts(10))
                ax1.set_ylabel('flow distance', fontproperties=get_fonts(10))
                
                # fitting curve
                a, b = optimize.curve_fit(fitting_f, xy_1[:, 0], xy_1[:, 1])[0]
                fitting_x = np.arange(np.min(xy_1[:, 0]), np.max(xy_1[:, 0]), 1)
                fitting_y = a*fitting_x + b
                ax1.plot(fitting_x, fitting_y, 'lightcoral', linewidth=5)
               
                figname = 'DC_' + dir_name[:-4] + '.png'
                fig1.savefig(os.path.join(picture_save_path, figname), dpi=300)
                plt.clf()

                
                fig2, ax2 = plt.subplots(1, 1, figsize=(5,5))
                ax2.set_title(country, fontproperties=get_fonts(15)) 
                xy_2 = np.c_[np.log10(CC_rd), L_rd]
                ax2.scatter(xy_2[:, 0], xy_2[:, 1], c='palegreen', s=30, alpha=0.7, edgecolors='grey')
                ax2.set_xlabel('complete consumption coefficient', fontproperties=get_fonts(10))
                ax2.set_ylabel('flow distance', fontproperties=get_fonts(10))
                    
                fname = 'CC_' + dir_name[:-4] + '.png'
                fig2.savefig(os.path.join(picture_save_path,fname), dpi=300)
                plt.clf()
