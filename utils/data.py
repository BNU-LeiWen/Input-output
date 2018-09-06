#!/urs/bin/env python

import numpy as np

##
def construct_flow_network(f):
    
    """construct flow network from original IO table
    Agrs:
        f: numpy array of original data
    Return:
        F: adjaceny matrix of flow network
    """

    #value-added as sink
    #VA = VALU
    VA = f[36, 0:34]    
    
    #final demands as source
    #FD = HFCE + NPISH + GGFC + GFCF + INVNT \
    #        - CONS_ABR + CONS_NONRES + EXPO + IMPO
    FD = np.zeros((1, 34))
    for i in range(34):
        FD[0, i] =  (f[i, 34] + f[i, 35] + f[i, 36] +  f[i, 37] + \
                f[i, 38] - f[i, 39] + f[i, 40] + f[i, 41] + f[i, 42])
    
    #intermediate input and output 
    A = f[0:34, 0:34]
    
    #restruct the data
    F = np.zeros((36, 36))
    F[1:35, 1:35] = A.T
    F[0, 1:35] = FD
    F[1:35, 35] = VA
    
    #balance the network
    for i in range(1, len(F) - 1):
        a = np.sum(F[i, :]) - np.sum(F[:, i])
        if a >= 0:
            F[0, i] = F [0, i] + a
        if a < 0:
            F[i, 35] = F[i, 35] - a
            
    #manage negetive final demand cases
    for i in range(1, len(F) - 1):
        if F[0, i] < 0:
            F[i, 35] = F[i, 35] - F[0, i]
            F[0, i] = 0
        
    #cheak the balance    
    for i in range(1, len(F) - 1):
        if not np.sum(F[i, :]) - np.sum(F[:, i]) <= 0.00001:
            print 'BALANCE FAIL'
    
    #delete sepaical industry C95
    F = np.delete(F, 34, axis= 1 )
    F = np.delete(F, 34, axis= 0 )
	
    return F
  

##
def log_size(F):

    """compute log10(total out-flow of industry)
    Args:
        F: adjacent matrix of flow network
    Return:
        size: out-flow size of industry
    """
    a = np.sum(F, axis = 1)[1: len(F)-1]
    size = np.log10(a)
   
    return size
 
  
##     
def compute_l_from_f(f):
    
    """compute flow distance
    Args:
        f: adjacent matrix of flow network
    Return:
        l: flow distance matrix
    """

    a = np.sum(f, axis = 1)
    
    m = np.zeros((len(f), len(f)))
    for i in range(len(f)):
        for j in range(len(f)):
            if i < len(f) - 1:
                m[i, j] = f[i, j] / a[i]
            else:
                m[i, j] = 0
                
    u = np.linalg.inv(np.eye(len(f), len(f)) - m)
    
    m1 = m.dot(u.dot(u))
    l = np.zeros((len(f), len(f)))
    for i in range(len(l)):
        for j in range(len(l)):
            l[i, j] = m1[i, j] / u[i, j] - m1[j,j] / u[j,j]
        
    return l
 
##
def compute_c_from_l(l_mat, method):
    
    """compute flow distance
    Args:
        l_mat: flow distance matrix
        method: method of symmetrization
    Return:
        c: symmetric flow distance matrix
    """
    
    l = l_mat[1:-1, 1:-1] 
    c = np.zeros((len(l), len(l)))
    if method == 'add':
        for i in range(len(l)):
            for j in range(len(l)):
                c[i, j] =l[i, j] + l[j, i]
 
    return c  



##
def compute_dis_to_ss(l):
    """compute flow distance from source and to sink
    Agrs: 
        l: flow distance matrix
    Return:
        dis_ss: [numpy array(N * 2)] 
                first col: source to i
                second col: i to i to sink

    """
  
    l = np.delete(l, 0, axis = 1)
    l = np.delete(l, len(l) - 1, axis = 0)    

    source_to_i = l[0, :]
    source_to_i = np.delete(source_to_i, len(l) - 1, axis = 0)     
    i_to_sink = l[:, len(l) - 1]
    i_to_sink = np.delete(i_to_sink, 0, axis = 0)  
    
    dis_ss = np.c_[source_to_i, i_to_sink]
    
    return dis_ss


##
def min_max_norm_for_vec(arr):
    new_arr = np.zeros(arr.shape)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            new_arr[i][j] = float(arr[i][j] - np.min(arr[:,j]))/(np.max(arr[:,j]) - np.min(arr[:, j]))
    return new_arr


##
def load_industry_infos(path):
    
    from collections import defaultdict 
    import csv

    industry_info = defaultdict(list)
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            industry_info['abb'].append(row[0])
            industry_info['label'].append(row[1])
    return industry_info
