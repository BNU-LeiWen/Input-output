#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

def get_fonts(abs_size):
    font_pro = FontProperties(family='serif', style='italic', weight='bold', size=abs_size)
    return font_pro

def plot_embed_for_country(file_name, fname, dis2ss, size, industry_info):
    
    country_abb = fname.split('_')[0]
    year = fname.split('_')[1]    
    
    fig, ax = plt.subplots(figsize=(15,8))
    figure_name = "%s's Industry Flow Network in %s" %(country_abb, year)
    plt.suptitle(figure_name, fontproperties=get_fonts(20))
        
    xy = dis2ss
    mean_xy = np.mean(dis2ss, axis=0)
    min_xy = np.min(xy)
    max_xy = np.max(xy) 
    sizes = size
    label_list = industry_info['label']
#    text_list = industry_info['abb']
    text_list = range(1,34)

    for i in range(len(xy)):
        if label_list[i] == '0':
            l0 = plt.scatter(xy[i, 0], xy[i, 1], s= sizes*150, c= 'lightskyblue', alpha=0.6)
        elif label_list[i] == '1':
            l1 = plt.scatter(xy[i, 0], xy[i, 1], s= sizes*150, c= 'palegreen', alpha=0.6)
        elif label_list[i] == '2':
            l2 = plt.scatter(xy[i, 0], xy[i, 1], s= sizes*150, c= 'lightcoral', alpha=0.6)
        elif label_list[i] == '3':
            l3 = plt.scatter(xy[i, 0], xy[i, 1], s= sizes*150, c= 'gold', alpha=0.6)  
        elif label_list[i] == '4':
            l4 = plt.scatter(xy[i, 0], xy[i, 1], s= sizes*150, c= 'violet', alpha=0.6)    

    for i in range(len(xy)):
        plt.text(xy[i, 0], xy[i, 1], text_list[i], fontsize=10,   
                 horizontalalignment='center', verticalalignment='center')

    x_y_line = [min_xy, max_xy]
    plt.plot(x_y_line, x_y_line, '--', linewidth =2, alpha=0.8)

    ax.axhline(mean_xy[1], ls= '--', lw= 4, color= 'grey', alpha=0.5)
    ax.axvline(mean_xy[0], ls= '--', lw= 4, color= 'grey', alpha=0.5)

    plt.xlabel('From-Source Distance (S)', fontproperties=get_fonts(12))
    plt.ylabel('To-Sink Distance (T)', fontproperties=get_fonts(12))
    plt.legend((l0, l1, l2, l3, l4),('AGRICULTURE, HUNTING, FORESTRY AND FISHING',\
               'MANUFACTURING','NON BUSINESS SECTOR SERVICES', 'BUSINESS SECTOR SERVICES',\
               'CONSTRUCTION, REAL ESTATE'), \
                scatterpoints=1, fontsize=8, markerscale= 0.3, loc='upper right')
       
    plt.savefig(file_name) 
    plt.clf()

def plot_embed_for_industry(figure_name, coor, size, text_info, country_label,fname):
    fig, ax = plt.subplots(figsize=(12,12))
    
    plt.suptitle(figure_name, fontproperties=get_fonts(20))
    
    for i in range(len(coor)):
        if country_label[text_info[i]] == '0':
            ax0 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='seagreen', alpha= 0.5)
        elif country_label[text_info[i]] == '1':
            ax1 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='orange', alpha= 0.5)
        elif country_label[text_info[i]] == '2':
            ax2 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='royalblue', alpha= 0.5)
        elif country_label[text_info[i]] == '3':
            ax3 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='lightcoral', alpha= 0.5)
        elif country_label[text_info[i]] == '4':
            ax4 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='mediumturquoise', alpha= 0.5)
        elif country_label[text_info[i]] == '5':
            ax5 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='blueviolet', alpha= 0.5)
        elif country_label[text_info[i]] == '6':
            ax6 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='hotpink', alpha= 0.5)
        elif country_label[text_info[i]] == '7':
            ax7 = plt.scatter(coor[i, 0], coor[i, 1], s= size*150, c='silver', alpha= 0.5)
            
    for i in range(len(coor)):
        plt.text(coor[i,0], coor[i,1], text_info[i], fontsize=10,\
                 horizontalalignment='center', verticalalignment='center')
                 
    plt.xlabel('From-source distance (S)', fontproperties=get_fonts(12))
    plt.ylabel('To-sink distance (T)', fontproperties=get_fonts(12))
    plt.legend((ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7),\
               ('EU', 'NAFTA', 'UNASUR', 'Asia', 'ASEAN', 'Pacific States', 'Africa', 'Others'),\
               scatterpoints=1, fontsize=8, markerscale= 0.3, loc='upper right')
    
    plt.savefig(fname)
    plt.clf()
