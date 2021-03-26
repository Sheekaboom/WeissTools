'''
@brief functions for rotating things and whatnot
@author aweiss
'''

import numpy as np

#%% Useful rotaion functions
#@cite https://en.wikipedia.org/wiki/Rotation_matrix
def Rx(theta):
    '''@brief x rotation matrix'''
    return np.asarray([[1,0            ,0             ],
                       [0,np.cos(theta),-np.sin(theta)],
                       [0,np.sin(theta),np.cos(theta)]])
def Ry(theta):
    '''@brief x rotation matrix'''
    return np.asarray([[np.cos(theta),0            ,np.sin(theta)],
                       [0            ,1            ,0             ],
                       [-np.sin(theta),0           ,np.cos(theta)]])
def Rz(theta):
    '''@brief x rotation matrix'''
    return np.asarray([[np.cos(theta),-np.sin(theta),0            ],
                       [np.sin(theta),np.cos(theta) ,0            ],
                       [0            ,0             ,1            ]])
