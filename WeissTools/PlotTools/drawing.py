'''
@brief functions for drawing with plotly. Currently mainly designed for drawing coordinate systems.
@author aweiss
'''

import numpy as np
import plotly.graph_objs as go
from WeissTools.rotations import Rx,Ry,Rz

#%% Some generally useful things
def get_line_loc3d(trace,loc='middle'):
    '''@brief approximate the location on the line at the 'start'|'middle'|'end' or at some decimal [0,1]'''
    if isinstance(loc,float): 
        loc_dist = loc;
        loc='middle'
    else: loc_dist = 0.5
    if loc=='start':
        mloc = np.asarray([trace[ax][0] for ax in 'xyz'])
    elif loc=='end':
        mloc = np.asarray([trace[ax][-1] for ax in 'xyz'])
    elif loc=='middle':
        nvals = len(trace['x'])
        if nvals==2: midx=1
        else: midx = int(np.round(nvals*loc_dist))
        # now get the actual location
        if midx==0:
            mloc =[trace[ax][midx] for ax in 'xyz']
        else:
            mloc = [trace[ax][midx-1]+(trace[ax][midx]-trace[ax][midx-1])*loc_dist for ax in 'xyz']
        # now adjust the size
        
    else:
        raise Exception("Location '{}' not recognized. Must be 'start'|'middle'|'end'".format(loc))
    return np.asarray(mloc)

def cart2sphere(x,y,z):
    '''@brief convert cartesian coordinates to spherical coordinates (as defined in balanis)'''
    phi = np.arctan2(y,x)
    theta = np.arctan2(np.sqrt(x**2+y**2),z)
    r = np.sqrt(x**2+y**2+z**2)
    return r,theta,phi

def sphere2cart(r,theta,phi):
    '''@brief convert spherical coords to cartesian (as defined in balanis)'''
    x = r*np.sin(theta)*np.cos(phi)
    y = r*np.sin(theta)*np.sin(phi)
    z = r*np.cos(theta)
    return x,y,z

        
#%% Some arc functions
def get_arc_2d(start,radius,angle,num_pts=100):
    '''@brief create points of a 2D arc. These can then be rotated as needed'''
    pts = np.linspace(0,angle,num_pts)
    y = radius*(np.sin(pts))
    x = radius*(np.cos(pts)-1)
    return np.asarray([x,y])+np.asarray(start)[...,np.newaxis]

def get_arc_3d(*args,**kwargs):
    '''@brief create points of a 3D arc. This can then be rotated as needed'''
    a2d = get_arc_2d(*args,**kwargs)
    return  np.concatenate((a2d,np.zeros((1,*np.shape(a2d)[1:]))),axis=0)

def get_line_label_3d(trace,label,loc='middle',**kwargs):
    '''@brief get an annotation for a 3D line (must add to scene.annotations). Add to 'start'|'middle'|'end'|float(0,1) '''
    # Get the location to put the annotation
    mloc = get_line_loc3d(trace,loc)
    # now get the annotation
    annot = {
        'showarrow':False,
        'x':mloc[0],'y':mloc[1],'z':mloc[2],
        'text':label}
    annot.update(**kwargs)
    return annot

#%% Creating arrowheads for vectors
def arrowhead3d(start,end,size=None,**kwargs):
    '''
    @brief plot an arrowhead on a 3d plotly plot (just 2 perpidicular planes)
    @param[in] start - iterable of (x,y,z) starting points (back of the arrow)
    @param[in] stop - iterable of (x,y,z) end points (tip of the arrow)
    '''
    arr_vec = np.asarray(end)-np.asarray(start)
    arr_vec_norm = arr_vec/np.sqrt(np.sum(arr_vec**2))
    if size is None:
        size=np.sqrt(np.sum(arr_vec**2))
    # now create the template arrow. arrow tip at the origin pointing up the z axis [[xxx],[yyy],[zzz]]
    template = np.asarray([[0,0,0],[0,1,-1],[0,-1,-1]])*size
    # now calculate our rotation
    r,theta,phi = cart2sphere(*arr_vec) # get theta,phi
    # now calculate the positions
    meshes = []
    for rot in [0,np.pi/2]:
        coords = (Rz(phi)@Ry(theta)@Rz(rot)@template)+np.asarray(end)[...,np.newaxis]
        tc = {
          'x':coords[0,:],
          'y':coords[1,:],
          'z':coords[2,:],
          'i':[0],'j':[1],'k':[2],
          }
        tc.update(**kwargs)
        meshes.append(go.Mesh3d(**tc))
    return meshes    
    
def get_line_arrowhead(trace,side,size=None):
    '''
    @brief get an arrowhead for a given trace (line)
    @param[in] trace - scatter trace to add arrow to
    @param[in] side - what side to add to. can be 'start'|'end'
    @note Tried some other things, but this is a custom implementation
    @return list of meshes to add to our figure
    '''
    num_pts = len(trace['y']) # y because we may not always have x or z
    coords = np.asarray([[0,0,0],[1,1,1]],dtype=np.double) #default coordinates
    if side=='start':
        coords[:,0] = trace['x'][:2:-1]
        coords[:,1] = trace['y'][:2:-1]
        coords[:,2] = trace['z'][:2:-1]
    else:
        coords[:,0] = trace['x'][num_pts-2:]
        coords[:,1] = trace['y'][num_pts-2:]
        coords[:,2] = trace['z'][num_pts-2:]
    
    ah = arrowhead3d(coords[0], coords[1],size=size,color=trace['marker']['color'] or trace['line']['color'])
    return ah

#%% Creating axes
def get_axes_lines(mag=1,ax_keys=['x','y','z']):
    '''@brief return a dict of 3D traces for our xyz axes with a given magnitude'''
    axes_coords = {
        'x':[[0,0,0],[1,0,0]],
        'y':[[0,0,0],[0,1,0]],
        'z':[[0,0,0],[0,0,1]],
        'xn':[[0,0,0],[-1,0,0]],
        'yn':[[0,0,0],[0,-1,0]],
        'zn':[[0,0,0],[0,0,-1]]
    }
    axes_lines = {}
    for k in ax_keys:
        v = np.asarray(axes_coords[k])*mag
        line = go.Scatter3d(x=v[:,0],y=v[:,1],z=v[:,2],name='{}_axis'.format(k),showlegend=False,mode='lines')
        line['marker']['color'] = 'black'
        axes_lines[k] = line
    # add arrows
    return axes_lines

def get_normal_plane(start,end,size=None):
    '''
    @brief create a 'plane' normal to a line (xyz). This plane is centered
        at the origin but rotated to be normal to the trace. This returns 4 coordinates
        for each corner of a 'plane' (a square actually)
    @param[in] start - starting (xyz) coordinates iterable of line to be normal to 
    @param[in] end - ending (xyz) coordinates iterable of line to be normal to 
    @param[in/OPT] size - size of the plane. If none default to .5 size of vector
    @return array of [x,y,z] coordinates for each corner of the plane
    '''
    # get distances
    dv = np.asarray(end)-np.asarray(start)
    if size is None: size = np.sqrt(np.sum(dv**2))*0.5
    # make rotatable plane
    plane = np.asarray([[1,1,-1,-1],[1,-1,1,-1],[0,0,0,0]])*size # xyz coordinates
    # calculate our rotations. This is done differently than arrowheads... cause theres no orientation component
    r,theta,phi = cart2sphere(*dv)
    plane = Rz(phi)@Ry(theta)@plane
    return plane


#%% Some EM specific things

def get_plane_wave(theta,phi,r=1,size=None,incident=False,**kwargs):
    '''
    @brief get traces for drawing a 3D plane wave in plotly. This assumes a plane
        wave travelling out of the origin
    @param[in] theta - theta angle of the plane wave
    @param[in] phi   - phi angle of the plane wave
    @param[in] r     - distance fromt he origin to the end of the vector
    @param[in/OPT] len - length of the vector (default .25*r)
    @param[in/OPT] incident - whether we are going into (True) or out of (False) the origin (default false)
    @return A list of traces for drawing this will be [line,arrowhead1,...,plane1,...,planeN]
    '''
    # default length
    if size is None: size = 0.35*r
    start = sphere2cart(r-size,theta,phi)
    end = sphere2cart(r,theta,phi)
    # if incident flip start and end
    if incident: tmp=start;start=end;end=tmp
    # now make our plots
    color = (255,165,0)
    line_spec = {'mode':'lines','line':{'color':'rgb{}'.format(color)},'showlegend':False}
    line_spec.update(kwargs)
    line = go.Scatter3d(**{k:[start[i],end[i]] for i,k in enumerate('xyz')},**line_spec)
    head = get_line_arrowhead(line, 'end',0.025)
    planes = []
    for l in [0.4,0.5,0.6]:
        plane = get_normal_plane(start,end,size=0.05)
        myloc   = get_line_loc3d(line,loc=l)
        plane += myloc[...,np.newaxis]
        mesh_spec = {'color':'rgba{}'.format(tuple(list(color)+[0.25])),'showlegend':False}
        mesh = go.Mesh3d(**{ax:coords for ax,coords in zip('xyz',plane)},**mesh_spec)
        planes.append(mesh)
    return [line]+head+planes
    
    
    
    
    
    
    
    
