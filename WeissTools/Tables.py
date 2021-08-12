# -*- coding: utf-8 -*-
"""
@date Wed Jul 14 11:02:30 2021
@brief Functions for formatting tables and other useful table things
@author ajw5
"""

#% import our required libraries
import pandas as pd
import numpy as np
import copy

#%% Some defaults
DEFAULT_FORMATS = {
    float:'%5.5g',
    str:'%s',
    }

#%% Table conversions
# these are essentially just wrappers of DataFrame functions for now

def table2word(table,cols=None,rows=None,rtype='text',formats={},**kwargs):
    '''
    @brief change table data to format usable in word
    @param[in] table - table (or just data) to get data from. 
        If pandas DataFrame try and get rows, cols from it too.
    @param[in/OPT] cols - list of names for columns
    @param[in/OPT] rows - list of names for rows (if specified)
    @param[in/OPT] rtype - return type. Text will print text to be copied into word, tab delimited,
        and should then use Insert > Table > Convert Text to Table.
    @param[in/OPT] format_override - dict of type/format specifier key values. Overrides 
    @param[in/OPT] kwargs - if DataFrame, passed to pd.DataFrame.to_csv()
    '''
    formatting = copy.deepcopy(DEFAULT_FORMATS)
    formatting.update(formats)
    options = {
        'sep':'\t',
        'float_format':formatting[float],
        'line_terminator':'\n', #default to just newline (no carriage return)
        }
    options.update(kwargs)
    # assume we built a dataframe here
    return table.to_csv(**options)
    
def table2latex(table,cols=None,rows=None,rtype='text',formats={},**kwargs):
    '''
    @brief change table data to format usable in word
    @param[in] table - table (or just data) to get data from. 
        If pandas DataFrame try and get rows, cols from it too.
    @param[in/OPT] cols - list of names for columns
    @param[in/OPT] rows - list of names for rows (if specified)
    @param[in/OPT] rtype - return type. Text will print text to be copied into word, tab delimited,
        and should then use Insert > Table > Convert Text to Table.
    @param[in/OPT] format_override - dict of type/format specifier key values. Overrides 
    @param[in/OPT] kwargs - if DataFrame, passed to pd.DataFrame.to_csv()
    '''
    formatting = {
        float:'%5.5f'
        }
    formatting.update(formats)
    options = {
        'float_format':formatting[float]
        }
    options.update(kwargs)
    # assume we built a dataframe here
    return table.to_latex(**options)

def merge_tables(*tables,merge_fun=None):
    '''
    @brief merge multiple tables (pandas dataframes) with the same size,rows,cols with a function specifed by merge_fun
    merge fun will be called with the values for a given index from each table (t1val[0],t2val[0],t3val[0]
    '''
    out_table = copy.deepcopy(tables[0])
    if merge_fun is None:
        def merge_fun(*vals):
            return ('%s'+'(%s)'*(len(vals)-1)) %tuple(vals)
    # now go through each value and select it
    for ri in range(len(out_table)):
        for ci in range(len(out_table.iloc[ri])):
            out_table.iloc[ri,ci] = merge_fun(*[t.iloc[ri,ci] for t in tables])
    # now return
    return out_table

def merge_tables_float(*tables,float_format=DEFAULT_FORMATS[float],str_format=DEFAULT_FORMATS[str]):
    '''@brief wrapper for floating point specifier'''
    def merge_fun(*vals):
        formatted_floats = tuple([float_format %v for v in vals])
        return (str_format+('('+str_format+')')*(len(vals)-1)) %formatted_floats
    return merge_tables(*tables,merge_fun=merge_fun)
    
    
    
#%% Some testing
if __name__=='__main__':
    
    table = pd.DataFrame(np.random.random((5,7)))
    table2 = pd.DataFrame(np.random.random((5,7)))
    print(table2word(table))
    print(table2latex(table,index=False))
    
    mtable = merge_tables(table,table2)
    mftable = merge_tables_float(table,table2)
    
    