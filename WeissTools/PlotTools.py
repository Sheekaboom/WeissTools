# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 10:13:28 2020
tools for python plots (just plotly now)
@author: aweiss
"""

from collections import defaultdict
import plotly.graph_objects as go
import plotly.io as pio
import os
from plotly.subplots import make_subplots
import numpy as np 
import re

from WeissTools.generic import num2pi

from WeissTools.MatTools import load_mat,openfig_mat
from WeissTools.MatTools import findall_mat

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

    # Set axes to use scientific notation (if needed)
    fig_handle.update_xaxes(exponentformat='e',showexponent='all')
    fig_handle.update_yaxes(exponentformat='e',showexponent='all')
    
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
    options['save_types'] = ['png','jpg','svg','html','json']
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
        if options['verbose']: print("SUCCESS")
        
def merge_figs_to_subplot(*args,rows=1,cols=2,**kwargs):
    '''
    @brief Take a list of figures and merge them into a subplot
    @note this will use the layout from the first plot
    @param[in] args - figures to merge
    @param[in/OPT] rows - rows in the subplot
    @param[in/OPT] cols - columns in the subplot
    @param[in/OPT] kwargs - passed to make_subplots()
    @return Handle to merged figure
    '''
    fig = make_subplots(rows=rows,cols=cols,**kwargs)
    raise NotImplementedError("Decided I didn't actually want this right now")
        
def fig2plotly(fig_path,**kwargs):
    '''
    @brief load a *.fig file from matlab and convert to a python (plotly) plot.
    @param[in] fig_path - path to the *.fig file to load
    @return A handle to a plotly plot.
    '''
    fig_mat = openfig_mat(fig_path) #open the figure
    axes = findall_mat(fig_mat,'axes')
    
    fig = go.Figure() #start our figure (assume 1 axis)
    ax = axes[0]
    #first find all error bars
    err_bar = findall_mat(ax,'specgraph.errorbarseries')
    for obj in err_bar: #plot each of these
        line = go.Scatter(x=obj.properties.XData,y=obj.properties.YData,
                         name=obj.properties.DisplayName,
                         error_y = dict(type='data',symmetric=False,
                                        array=obj.properties.UData,
                                        arrayminus=obj.properties.LData)
                         )
        fig.add_trace(line)
    return fig

def set_pi_axis(fig,increment:float,xyz:str):
    '''
    @brief take an axis and label in increments of pi
    @param[in] ax - axis to set pi on
    @param[in] interval - interval to put ticks on (e.g. np.pi/2). 
       Should be expressed in terms of a multiple of pi
    @param[in] xyz - chararray with single or combo of 'x','y','z'
    to specify which direction of the axis to set
    @note Currently only for Plotly
    '''
    for ax_char in xyz:
        #get the string for the axis
        ax_str = '{}axis'.format(ax_char.lower())
        
        #get the min/max for the axis
        myrange = np.array([min([min(d[ax_char]) for d in fig.data])
                           ,max([max(d[ax_char]) for d in fig.data])])
        
        # now lets create our values and text
        norm_range = np.round(myrange/increment)
        tvals = np.arange(norm_range[0],norm_range[1]+1)*increment
        ttext = num2pi(tvals)
        ttext = ['${}$'.format(t) for t in ttext]
        
        #now update the figure
        fig.update_layout({ax_str:dict(tickmode='array',tickvals=tvals,ticktext=ttext)})
        
    return fig

def figs2video(figs,file_path,**kwargs):
    '''
    @brief Take a list of figures (plotly for now) and save to a video
    @param[in] figs - list of figures to make into video
    @param[in] file_path - path to write the video to (should be a *.avi)
    @param[in/OPT] kwargs - keyword arguments as follows
        - verbose - whether or not to be verbose when running (False)
        - fps - frames per second to write out the video to
    @note This requires the opencv python library
    @cite https://plot.ly/python/static-image-export/
    @cite https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
    '''
    #parse input and import opencv
    import cv2 #import opencv
    options = {}
    options['verbose'] = False
    options['fps'] = 25
    for k,v in kwargs.items():
        options[k] = v
        
    # get the images from the figure list
    imgs = [] # list of our images
    if options['verbose']: print("CONVERT IMAGE: {:10d}".format(0),end='')
    for i,fig in enumerate(figs):
        if options['verbose']: print("{}CONVERT IMAGE: {:10d}".format('\b'*25,i),end='')
        img = np.array(bytearray(fig.to_image('png'))) # correct conversion
        imgs.append(cv2.imdecode(img, 1)) # decode as color image    
    if options['verbose']: print() #print newline
    
    #now lets turn this into a movie!
    height,width = imgs[0].shape[:2]
    myvid = cv2.VideoWriter(file_path,0,options['fps'],(width,height))
    if options['verbose']: print("WRITE VIDEO: {:10d}".format(0),end='')
    for i,img in enumerate(imgs):
        if options['verbose']: print("{}WRITE VIDEO: {:10d}".format('\b'*23,i),end='')
        myvid.write(img) #write images to video
    if options['verbose']: print() #print newline
    
    #now close the video and opencv windows
    cv2.destroyAllWindows()
    myvid.release()
    return file_path
    

def scatter_uncert(nom_trace,err=None,**kwargs):
    '''
    @brief plot a plotly scatter (line) plot with continuous error bars
    @param[in] nom_trace - nominal trace to generate error bars from (need x values and color)
    @param[in] err - tuple of (lo,hi) y error values
    @return a filled go.Scatter trace for the continuous error bars of the provided nominal trace
    '''
    xvals = list(nom_trace['x'])+list(nom_trace['x'])[::-1]
    yvals = list(err[0])+list(err[1])[::-1]
    trace_color = nom_trace['line']['color']
    if trace_color is None: trace_color=[100,100,100]
    else: trace_color = [int(v) for v in trace_color.strip('rgb(').strip(')').split(',')] #get int list
    uncert_trace = go.Scatter(x=xvals,y=yvals,name=str(nom_trace['name'])+'_uncert'
                    ,fill='toself',fillcolor='rgba({},{},{},0.2)'.format(*trace_color)
                    ,line=dict(color='rgba(255,255,255,0)'),showlegend=False,**kwargs)
    return uncert_trace

def histogram_bar(x,*args,**kwargs):
    '''
    @brief create a plotly histogram using go.bar. This is useful when converting to MATLAB
        as go.Histogram data is not stored in the JSON (see https://plotly.com/python/histograms/#accessing-the-counts-yaxis-values)
    @param[in] x - data to create a histogram from
    @param[in] kwargs - keyword args for np.histogram and go.bar. histogram variables will be separated out
    @return plotly bar object
    '''
    nphist_kwnames = ['bins','range','normed','weights','density']
    nphist_kwargs = {k:kwargs.pop(k) for k in nphist_kwnames if k in kwargs.keys()}
    counts,bins = np.histogram(x,**nphist_kwargs)
    bins = 0.5 * (bins[:-1] + bins[1:])
    avg_width = np.mean(np.abs(bins[:-1]-bins[1:]))
    trace = go.Bar(x=bins, y=counts,width=avg_width,marker={'line':{'width':0}},**kwargs)
    return trace
    
def polar_db(r,theta,r_range=100,**kwargs):
    '''
    @brief produce a polar trace for dB. This will adjust negative values of r to be above 0
    @param[in] r - r values (in db) for plotting
    @param[in] theta - theta values (radians) for plotting
    @parma[in] r_range - dynamic range of the plot (max-min). All values lower
        than max(r)-range will be set to max(r)-range
    @param[in/OPT] kwargs - passed to plotting routine (go.Scatterpolar)
    @note currently produces a plotly Plot with a scatterpolar trace
    '''
    # Adjust data
    r_max = np.round(np.nanmax(r),-1)
    r_min = np.round(r_max-r_range,-1)
    r[r<r_min] = r_min
    r_ticks = np.unique([np.int(np.round(v,-1)) for v in np.linspace(r_min,r_max,5)])
    theta_deg = np.rad2deg(theta)
    
    # Now plot
    fig = go.Figure()
    trace = go.Scatterpolar(r=r,theta=theta_deg,**kwargs)
    fig.add_trace(trace)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(tickmode='array',tickvals=r_ticks, ticktext=[str(v) for v in r_ticks])
            )
        )
    return fig

if __name__=='__main__':
    
    import numpy as np
    x = np.linspace(0,2*np.pi,1000)
    y = np.cos(4*x)
    fig = go.Figure(go.Scatter(x=x,y=y))
    fig = format_plot(fig)
    fig.show(renderer='svg')
    
    t = np.linspace(-np.pi,np.pi,361)
    r = 20*np.log10(np.cos(t)**2)
    db_plot = polar_db(r,t)
    db_plot.show(renderer='svg')
    
    #fig_path = r"C:\Users\aweis\Google Drive\GradWork\papers\2019\python-matlab\data\figs\fig\add_speed_comp.fig"
    #fig_mat = openfig_mat(fig_path)
    #import scipy.io as spio
    #fig_mat_raw = spio.loadmat(fig_path,struct_as_record=False,squeeze_me=True)
    #fig = fig2plotly(fig_path)
    pass
    
    