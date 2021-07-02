'''
@brief Some custom plots that are useful
@author aweiss
'''

import plotly.graph_objs as go
import numpy as np

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