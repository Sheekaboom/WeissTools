'''
@date 2021-05-06
@author ajw
@brief class for convenient logging
'''

import datetime
import copy

from WeissTools.Dict import WDict

#%% Some default values and aliases

# text color is '\x1b[38;2;r;g;b'
# background color is '\x1b[38;2;r;g;b'
# bell is \x07

DEFAULT_FONT_FORMAT = {
    'time'   : '\x1b[38;2;128;128;128m',
    'msg'    : '\x1b[38;2;255;255;255m',
    'info'   : '\x1b[38;2;255;255;255m',
    'warning': '\x1b[38;2;255;255;0m',
    'error'  :'\x1b[38;2;255;50;0m'
    }

DEFAULT_LEVEL_NAMES = {
    'info'   : 'INFO',
    'warning': 'WARNING',
    'error'  : 'ERROR'
    }

LEVEL_ALIASES = {
    'i':'info','w':'warning','e':'error',
    'err':'error','warn':'warning'}

LOG_TEMPLATE = '{ts_fmt}{timestamp:9.6f}\x1b[0m - {lvl_fmt}{level}\x1b[0m - {msg_fmt}{msg}\x1b[0m'

#%% Our actual logger class

class Logger(WDict):
    '''
    @brief class for logging (and possibly saving out)
    @param[in] args - passed to wdict constructor
    @param[in] fonts - dictionary of fonts to pass in. otherwise use default
    @param[in] kwargs - any other info to save in the dict
    '''
    def __init__(self,*args,fonts={},**kwargs):
        '''@brief constructor'''
        # init parent
        super().__init__(*args,**kwargs)
        # add in font formats
        self.fonts = copy.deepcopy(DEFAULT_FONT_FORMAT)
        self.fonts.update(fonts)
        # get the parent timestamp (when we were initialized)
        self._init_timestamp()
        # init the log
        self._init_log()
        
    def _init_log(self):
        '''@brief initialize our log if it wasnt provided'''
        if self.get('log',None) is None:
            self._log = self['log'] = []
            self._log_str = ''
        
    def _init_timestamp(self):
        '''@brief initialize our timestamp values'''
        self._start_time = datetime.datetime.now()
        self['timestamp'] = self._start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        
    def get_timestamp(self):
        '''@brief return seconds since self['timestamp']'''
        return (datetime.datetime.now()-self._start_time).total_seconds()
        
    def log(self,msg:str,level:str=None,**kwargs):
        '''@brief generic function to log'''
        # set default levels
        if level is None:
            if isinstance(msg,str):
                level = 'info'
            elif isinstance(msg,Exception): # make errror if its an exception
                level = 'error'; msg = repr(msg)
        # get our level if aliased
        level = LEVEL_ALIASES.get(level,level)
        # make our loggin template
        entry = {'timestamp':self.get_timestamp(),
                 'level':level,
                 'msg':msg}       
        fonts = {'ts_fmt' :self.fonts['time'],
                 'lvl_fmt':self.fonts[level],
                 'msg_fmt':self.fonts['msg']}
        log_str = LOG_TEMPLATE.format(**fonts,**entry)
        # log the value
        print(log_str) # print
        self._log.append(entry) # add to entry
        self._log_str += (log_str+'\n'+' '.join(['---']*10)+'\n')
        
    def info(self,*args,**kwargs):
        '''@brief log info'''
        self.log(*args,level='info',**kwargs)    
        
    def warning(self,*args,**kwargs):
        '''@brief log a warning'''
        self.log(*args,level='warning',**kwargs)
        
    def error(self,*args,**kwargs):
        '''@brief log an error'''
        self.log(*args,level='error',**kwargs)
        
        
#%% testing

if __name__=='__main__':
    
    mylog = Logger()
    for lvl in ['i','w','e']:
        lvl_name = LEVEL_ALIASES.get(lvl,lvl)
        mylog.log("this is a {} test".format(lvl_name),lvl)
        
    for lvl in ['info','warning','error']:
        getattr(mylog,lvl)("This is a {} method test".format(lvl))
        
        
    


