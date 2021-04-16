# -*- coding: utf-8 -*-
"""
@brief Some useful generic python functions

@date Wed Jun 17 12:48:24 2020

@author aweiss
"""

import numpy as np



def num2pi(num):
    '''
    @brief Change number(s) to string fractions of pi
    @param[in] num - number(s) (could be iterable) to convert
    @return list of strings with converted values
    '''
    #make iterable
    if not hasattr(num,'__iter__'):
        num = [num]
    #now convert
    out_vals = []
    for n in num:
        num,den = float.as_integer_ratio(n/np.pi)
        if num==0:
            out_vals.append('0')
        else:
            pi_str = r'{}\pi/{}'.format(num,den)
            pi_str = pi_str.replace(r'1\pi',r'\pi') #remove 1 pi
            pi_str = pi_str.replace(r'/1','') #remove divided by 1
            out_vals.append(pi_str)
    return out_vals


