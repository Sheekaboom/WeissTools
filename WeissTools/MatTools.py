'''
@brief Tools for interfacing with a variety of MATLAB things. Note that all
    plotting interfaces most likely exist in the PlotTools module
@author aweiss
@date January 2020
'''

import scipy.io as spio
import numpy as np

def load_mat_dict(mat_file,**kwargs):
    '''
    @brief Load a *.mat file. If its a structure convert to a nested dict.
        This is not the default of scipy.io. It by default loads as some
        weird version of object numpy arrays for structures.
    @param[in] mat_file - path to *.mat file to load
    @param[in/OPT] kwargs - keyword args as follows:
        - None - Yet!
    @cite https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries    
    @return A dictionary of the loaded MATLAB structure
    '''
    def _check_keys(dict):
        '''@breif change matlab structs to dicts'''
        for key in dict:
            if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
                dict[key] = _todict(dict[key])
        return dict        

    def _todict(matobj):
        '''@brief Recursively construct nested dictionaries from matobjects'''
        dict = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, spio.matlab.mio5_params.mat_struct):
                dict[strg] = _todict(elem)
            else:
                dict[strg] = elem
        return dict

    data = spio.loadmat(mat_file, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def load_mat(mat_file,**kwargs):
    '''
    @brief this is just a wrapper for scipy.io.loadmat
    @param[in] mat_file - path to *.mat file to load
    @param[in/OPT] kwargs - keyword args as follows:
        - None - Yet!
    '''
    data = spio.loadmat(mat_file, struct_as_record=False, squeeze_me=True)
    return data
    
def get_mat(handle,val):
    '''
    @brief this is a function to perform the same operation as matlabs get
    @param[in] handle - handle to matlab object (loaded with scipy)
    @param[in] val - string name of property to get
    @return Retrieved property
    '''
    return getattr(handle,val)

def fieldnames_mat(handle):
    '''
    @brief get the fildnames of a matlab structure
    @param[in] handle - handle of structure to get fieldnames of
    @return List of fieldnames
    '''
    return getattr(handle,'_fieldnames')

def openfig_mat(fig_path):
    '''
    @brief open a matlab figure and get the relevant data
    @param[in] fig_path - path to *.fig file
    '''
    fig = load_mat(fig_path)
    fig = fig['hgS_070000'] #not exactly sure what the other crap is
    return fig

def findall_mat(handle,type):
    '''
    @brief Findall like in matlab (find all of a certain type from a struct)
    @param[in] handle - handle to structure
    @param[in] type - type of object we are looking for
    '''
    if not isinstance(handle,spio.matlab.mio5_params.mat_struct):
        #if its not a matlab struct return nothing
        return []
    elif 'type' in fieldnames_mat(handle) and handle.type==type: 
        #if this is what we want, return it
        return [handle]
    else:
        obj_list = [] #otherwise look through children
        if len(fieldnames_mat(handle))>0:
            for fname in fieldnames_mat(handle):
                #check if its another struct
                field = getattr(handle,fname)
                if isinstance(field,spio.matlab.mio5_params.mat_struct):
                    #then recursively go through it
                    findall_mat(field,type)
                elif isinstance(field,np.ndarray) and field.dtype==np.object: 
                    #if its an array search through that
                    if np.ndim(field)>0:
                        for fld in field:
                            obj_list+=findall_mat(fld,type)
            return obj_list
        else:
            return []


if __name__=='__main__':

    fig_path = r"C:\Users\aweis\Google Drive\GradWork\papers\2019\python-matlab\data\figs\fig\add_speed_comp.fig"
    fig_mat = openfig_mat(fig_path)
    ax = findall_mat(fig_mat,'axes')
