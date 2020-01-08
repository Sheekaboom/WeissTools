# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 10:13:28 2020
tools for python plots (just plotly now)
@author: aweis
"""

from collections import defaultdict
import plotly.graph_objects as go
import plotly.io as pio
import os

def format_plot(fig_handle,**kwargs):
    '''
    @brief format text size, color, etc of a plot given by a figure handle
    @note currently only supports plotly
    @param[in] fig_handle - handle to the figure to format
    @param[in/OPT] kwargs - keyword arguments as follows:
        - font_size - size of the font in the plot
        - margin_size - dict with 't','l','r','b' with margin sizes (like plotly)
        - remove_background - whether or not to make background transparent (default True)
    '''
    options =  {}
    options['font_size'] = 24
    options['margins'] = {'t':60,'b':20,'l':20,'r':20}
    options['remove_background'] = True
    for k,v in kwargs.items():
        options[k] = v
    marker_symbol_types = list(range(45))
    line_dash_types = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    #set figure parameters
    fig_handle.update_layout(template='plotly_white') #clear our template
    fig_handle.update_layout(font=dict(size=options['font_size']))
    fig_handle.update_layout(margin=options['margins'])
    fig_handle.update_layout(paper_bgcolor='rgba(0,0,0,0)') #remove paper background
    #remove the background
    if options['remove_background']:
        fig_handle.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    #set title location
    title = fig_handle['layout']['title']['text']
    fig_handle.update_layout(
        title={
            'text': title,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'middle'})
    
    #now set trace specific values
    for i,tr in enumerate(fig_handle['data']): #get each trace
        if tr['type'] == 'scatter': #its a scatter/line plot
            dash_type = line_dash_types[i%len(line_dash_types)] #get mod value
            marker_type = marker_symbol_types[i%len(marker_symbol_types)]
            tr['line']['dash'] = dash_type #set line type
            tr['marker']['symbol'] = marker_type #set marker type
    #now return the handle for more clear code
    return fig_handle      
    
def save_plot(fig_handle,name,fig_folder,**kwargs):
    '''
    @brief saves a plot out to multiple file formats
    @note currently only supports plotly
    @param[in] fig_handle - handle to the figure to format
    @param[in] name - name (without extension) to save 
    @param[in] fig_folder - folder to save figures to
    @param[in/OPT] kwargs - keyword arguments as follows:
        - save_types - list of extensions to save to (e.g., png,epsc,html)
        - verbose - be verbose in the saving
        - format_plot - whether or not to format the plot
    @note kwargs also passed to format_plot()
    '''
    options = {}
    options['save_types'] = ['png','jpg','svg','eps','html','json']
    options['verbose'] = False
    options['format_plot'] = True
    for k,v in kwargs.items():
        options[k] = v
        
    #format if desired
    if options['format_plot']:
        fig_handle = format_plot(fig_handle,**kwargs)
    
    #now a dict of names of the attributes of fig for writing
    write_funct_dict = defaultdict(lambda:'write_image')
    write_funct_dict['html'] = 'write_html'
    write_funct_dict['json'] = 'write_json'
    if options['verbose']: print("Saving plot '{}':".format(name))
    for stype in options['save_types']:
        #create a folder
        fig_type_path = os.path.join(fig_folder,stype)
        if not os.path.exists(fig_type_path):
            os.makedirs(fig_type_path)
        #now save
        if options['verbose']: print("    {:6s}:".format(stype),end='')
        save_fun = getattr(fig_handle,write_funct_dict[stype])
        save_name = os.path.join(fig_type_path,'{}.{}'.format(name,stype))
        save_fun(save_name)
        print("SUCCESS")


if __name__=='__main__':
    
    import numpy as np
    x = np.linspace(0,2*np.pi,1000)
    y = np.cos(4*x)
    fig = go.Figure(go.Scatter(x=x,y=y))
    fig = format_plot(fig)
    fig.show()
    
    