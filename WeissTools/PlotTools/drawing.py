'''
@brief functions for drawing with plotly. Currently mainly designed for drawing coordinate systems.
@author aweiss
'''


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
        midx = int(np.ceil(nvals*loc_dist))
        if nvals%2==0: # if even number
            mloc = np.mean([[trace[ax][midx],trace[ax][midx-1]] for ax in 'xyz'],axis=-1)
        else: # if odd
            mloc = np.asarray([trace[ax][midx] for ax in 'xyz'])
    else:
        raise Exception("Location '{}' not recognized. Must be 'start'|'middle'|'end'".format(loc))
    # now get the annotation
    annot = {
        'showarrow':False,
        'x':mloc[0],'y':mloc[1],'z':mloc[2],
        'text':label}
    annot.update(**kwargs)
    return annot

#%% Some useful functions
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
    # now calculate our rotation
    zt = np.arctan2(arr_vec[1],arr_vec[0]) # atan(y,x)
    yt = np.arctan2(arr_vec[2],np.sqrt(np.sum(arr_vec[:2]**2))) # atan(z,euc_norm(x,y))
    # now calculate the positions
    coords = np.ndarray((3,3),dtype=np.double)
    coords[0] = end #end point
    meshes = []
    for xr in [0,np.pi/2]:
        coords[1] = (Rz(zt)@Ry(yt)@Rx(xr)@Ry(np.pi/2)@np.asarray([1,0,0])*size)+end-(arr_vec_norm*size)
        coords[2] = (Rz(zt)@Ry(yt)@Rx(xr)@Ry(-np.pi/2)@np.asarray([1,0,0])*size)+end-(arr_vec_norm*size)
        tc = {
          'x':coords[:,0],
          'y':coords[:,1],
          'z':coords[:,2],
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
    
    ah = arrowhead3d(coords[0], coords[1],size=size,color=trace['marker']['color'])
    return ah

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
