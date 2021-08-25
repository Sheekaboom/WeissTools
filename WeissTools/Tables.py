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
import re

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
    
def table2latex(table,formats={},add_hline=True,bold_cols=True,column_format=None,mathmode=True,**kwargs):
    '''
    @brief change table data to format usable in word
    @param[in] table - table (or just data) to get data from. 
        If pandas DataFrame try and get rows, cols from it too.
    @param[in/OPT] add_hline - add hline in between each row
    @param[in/OPT] bold_cols - bold column names
    @param[in/OPT] mathmode - remove any "\$" and replace with "$" at the end to allow mathmode
    @param[in/OPT] formats - dict of type/format specifier key values. Overrides 
    @param[in/OPT] kwargs - if DataFrame, passed to pd.DataFrame.to_csv()
    '''
    # more in depth column formatting (can pass single value to extend to all columns)
    ncols = len(table.columns)
    if kwargs.get('columns',None) is not None:
        ncols = len(kwargs.get('columns'))
        
    if column_format is not None and len(re.findall('([rcl]|[pmb]{.*})',column_format))==1: # if we only have 1 format (e.g. c or |c|)
        myformat = re.findall('\|*.*(?=\|)',column_format)[0]    
        myend = re.findall('\|$',column_format)[0] if re.findall('\|$',column_format) else ''
        column_format = "*{%d}{%s}%s" %(ncols,myformat,myend)
    # more in depth formatting ajustment
    formatting = {
        float:'%5.5f'
        }
    formatting.update(formats)
    # write to options
    options = {
        'float_format':formatting[float],
        'column_format':column_format
        }
    options.update(kwargs)
    # assume we built a dataframe here
    tex_table = table.to_latex(**options)
    # add bolded column names if desired
    if bold_cols:
        col_names = kwargs.get('columns',table.columns) # get the column names
        tex_table = wrap_tex_table_columns(tex_table, col_names,'\\textbf{%s}')
            
    # add hline in between non rule specified rows (e.g. midrule, toprule, bottomrule)
    if add_hline:
        tex_table = add_tex_table_hlines(tex_table)
    # make mathmode (if desired)
    if mathmode:
        tex_table = set_mathmode(tex_table)
    # now return
    return tex_table
    
def add_tex_table_hlines(tex_str):
    '''@brief add hlines in between non-ruled or hlined rows in tex table'''
    split_table = tex_str.split(r'\\') # split on table row
    keywords = ['rule','tabular']
    # find unruled lines
    lined = [any([kw in split_table[i+1] for kw in keywords]) for i in range(len(split_table)-1)]
    # now add hline to unruled lines
    for i in range(len(lined)):
        if not lined[i]: #if its not lined, add a line to the next one.
            split_table[i+1] = '\n\\hline'+split_table[i+1] 
    return r'\\'.join(split_table)

def wrap_tex_table_columns(tex_str,col_names,format_str='\\textbf{%s}'):
    '''@brief wrap column names given a tex string and the column names in a format string'''
    col_re = '&'.join(['\s*{}\s*'.format(c) for c in col_names])
    col_match = re.findall(col_re,tex_str)[0]
    match_split = col_match.split('&') # split on separator
    updated_split = []
    for ms,col in zip(match_split,col_names): # now replace with formatter
        updated_split.append(ms.replace(str(col),format_str %(col)))
    new_cols = '&'.join(updated_split)
    return tex_str.replace(col_match,new_cols)

def set_mathmode(tex_str):
    '''@brief set mathmode by changing "\$" to "$"'''
    return re.sub(r'\\*\$','$',tex_str)

def table2strtable(table,formats={}):
    '''@brief convert a table to a set of strings given formats for datatypes'''
    def format_fun(val): # formatter for each value
        #first get the formatter
        formatter="%s" #init to string
        for k,v in formats.items():
            if isinstance(val,k): # if its an instance of a specified type, first match is chosen
                formatter=v
                break 
        # return the forma
        return (formatter %(val))
    return table.applymap(format_fun)
        
def merge_tables(*tables,merge_fun=None):
    '''
    @brief merge multiple tables (pandas dataframes) with the same size,rows,cols with a function specifed by merge_fun
    merge fun will be called with the values for a given index from each table (t1val[0],t2val[0],t3val[0]
    '''
    out_table = copy.deepcopy(tables[0])
    if merge_fun is None:
        def merge_fun(*vals):
            return ('%s'+' (%s)'*(len(vals)-1)) %tuple(vals)
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
    print(table2latex(table,index=False,column_format='|c|'))
    
    mtable = merge_tables(table,table2)
    mftable = merge_tables_float(table,table2)
    
    sl = ['|c','|r|r|r|','|m{.15\textwidth}|','||l|']
    [re.findall('([rcl]|[pmb]{.*})',s) for s in sl]
    
    strtable = table2strtable(table,formats={float:'$%4.2f$'})
    print(strtable)
    