'''
@brief conversion functions for plots
@author aweiss
'''

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
    

