'''
@date 2021-05-06
@author ajw
@brief class for convenient logging
'''

import datetime
import copy
import sys

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
    'error'  : '\x1b[38;2;255;50;0m',
    'debug'  : '\x1b[38;2;128;0;128m'
    }

DEFAULT_LEVEL_NAMES = {
    'info'   : 'INFO',
    'warning': 'WARNING',
    'error'  : 'ERROR',
    'debug'  : 'DEBUG'
    }

VERBOSITY_LEVELS = {
    'info':1,
    'warning':2,
    'error':3,
    'debug':4
    }

MAX_VERBOSITY = max(VERBOSITY_LEVELS.values())

LEVEL_ALIASES = {
    'i':'info','w':'warning','e':'error','d':'debug',
    'err':'error','warn':'warning'}

LOG_TEMPLATE = '{ts_fmt}{timestamp}\x1b[0m - {lvl_fmt}{level}\x1b[0m - {msg_fmt}{msg}\x1b[0m'

#%% Generic Functions for logging
def log(msg:str,level:str=None,start_time:datetime.datetime=None,
        fonts:dict=DEFAULT_FONT_FORMAT,verbose:int=MAX_VERBOSITY,locs:list=[],**kwargs):
    '''
    @brief function for logging formatted information to select locations
    @param[in] msg - message to print
    @param[in] level - what level to print at (SEE DEFAULTS ABOVE)
    @param[in] start_time - time to make timestamps since (if not just print current time)
    @param[in] fonts - font dictionary for formatting
    @param[in] verbose - How verbose to be (see VERBOSITY_LEVELS)
    @param[in] locs - list of supported locations or things with 'write' methods (apart from stdout)
    @param[in] kwargs - other possible (less useful) arguments... (none yet though)
    @return handles to updated loc values
    '''
        # set default levels
    if level is None:
        if isinstance(msg,str):
            level = 'info'
        elif isinstance(msg,Exception): # make errror if its an exception
            level = 'error'; msg = repr(msg)
    # get our level if aliased
    level = LEVEL_ALIASES.get(level,level)
    # make our loggin template
    entry = {'timestamp':get_timestamp(start_time),
             'level':DEFAULT_LEVEL_NAMES[level],
             'msg':msg}       
    log_fonts = {'ts_fmt' :fonts['time'],
             'lvl_fmt':fonts[level],
             'msg_fmt':fonts['msg']}
    log_str = LOG_TEMPLATE.format(**log_fonts,**entry)
    log_str = (log_str+'\n'+' '.join(['---']*10)+'\n')
    # log the value
    if verbose>=VERBOSITY_LEVELS.get(level,1):
        sys.stdout.write(log_str)
    locs_out = []
    for l in locs:
        if isinstance(l,str): # append to string
            l+=log_str
        elif isinstance(l,list): # append entry to list
            l.append(entry)
        else: #otherwise try and write the string
            l.write(log_str)
        locs_out.append(l) # return handles to written values
    return locs_out

def get_timestamp(start_time=None):
    '''@brief get a log timestamp. start is start time as a datetime'''
    if start_time is not None:
        return '{:9.6f}'.format((datetime.datetime.now()-start_time).total_seconds())
    else:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

#%% Our actual logger class

class Logger(WDict):
    '''
    @brief class for logging (and possibly saving out)
    @param[in] args - passed to wdict constructor
    @param[in] fonts - dictionary of fonts to pass in. otherwise use default
    @param[in] kwargs - any other info to save in the dict
    '''
    
    # class variables for global usage
    _log_str = ''
    _log = []
    _start_time = datetime.datetime.now()
    _timestamp = _start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    _verbose = MAX_VERBOSITY
    fonts = DEFAULT_FONT_FORMAT
    
    @classmethod
    def log(cls,msg:str,level:str=None,**kwargs):
        '''@brief generic function to log'''
        cls._log,cls._log_str = log(msg,level=level,verbose=cls._verbose,
                                        start_time=cls._start_time,fonts=cls.fonts,
                                        locs=[cls._log,cls._log_str])
        
    @classmethod
    def info(cls,*args,**kwargs): return cls.log(*args,level='i',**kwargs)
    @classmethod
    def warning(cls,*args,**kwargs): return cls.log(*args,level='w',**kwargs)
    @classmethod
    def error(cls,*args,**kwargs): return cls.log(*args,level='e',**kwargs)
    @classmethod
    def debug(cls,*args,**kwargs): return cls.log(*args,level='d',**kwargs)
    
    @classmethod
    def set_verbose(cls,vlevel=MAX_VERBOSITY):
        cls._verbose = vlevel
    
    # variables for non-global usage
    def __init__(self,*args,fonts={},**kwargs):
        '''@brief constructor'''
        # init parent
        super().__init__(*args,**kwargs)
        # add in font formats (instance)
        self.ifonts = copy.deepcopy(DEFAULT_FONT_FORMAT)
        self.ifonts.update(fonts)
        #set verbosity (instance)
        self._iverbose = kwargs.get('verbose',MAX_VERBOSITY)
        # get the parent timestamp (when we were initialized)
        self._init_timestamp()
        # init the (local) log
        self._init_log()
        # initialize instance methods
        self._init_instance()
        
    def _init_log(self):
        '''@brief initialize our instance log if it wasnt provided'''
        if self.get('log',None) is None:
            self._ilog = self['log'] = []
            self._ilog_str = ''
        
    def _init_timestamp(self):
        '''@brief initialize our timestamp values'''
        self._istart_time = datetime.datetime.now()
        self['timestamp'] = self._start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    def _init_instance(self):
        '''@brief change from classmethods to instance methods'''
        # instantiate logging
        def ilog(msg:str,level:str=None,**kwargs):
            self._ilog,self._ilog_str = log(msg,level=level,verbose=self._iverbose,
                                            start_time=self._istart_time,fonts=self.ifonts,
                                            locs=[self._ilog,self._ilog_str])
        self.log = ilog
        # override easy access methods
        self.info = lambda *args,**kwargs: self.log(*args,level='i',**kwargs)
        self.warning = lambda *args,**kwargs: self.log(*args,level='w',**kwargs)
        self.error = lambda *args,**kwargs: self.log(*args,level='e',**kwargs)
        self.debug = lambda *args,**kwargs: self.log(*args,level='d',**kwargs)
        
        # verbosity setting
        def set_iverbose(vlevel=MAX_VERBOSITY):
            self._iverbose = vlevel
        self.set_verbose = set_iverbose
        
        
#%% testing
import unittest

class TestLogger(unittest.TestCase):
    '''@brief test logger functionality'''
    

    
    def test_logger_instances(self):
        '''@brief test the workings of global and instance logging'''
        loggers = self.get_loggers()
        # make sure globals are the same
        gloggers = [l for k,l in loggers.items() if 'global' in k]
        lloggers = [l for k,l in loggers.items() if 'local' in k]
        # test global loggers saved together
        for gl in gloggers[1:]: # assume more than 1 instance
            self.assertTrue((gloggers[0]._log==gl._log))
            self.assertTrue((gloggers[0]._log_str==gl._log_str))
        # now test locals
        for ll in lloggers[1:]:
            with self.subTest(i=ll.get('name')):
                # make sure theyre NOT the same
                self.assertTrue((lloggers[0]._ilog!=ll._ilog))
                self.assertTrue((lloggers[0]._ilog_str!=ll._ilog_str))
        # and finally make sure no locals log to global
        for ll in lloggers:
            for l in ll._ilog:
                self.assertTrue(l not in gloggers[0]._log)
            
            
    def get_loggers(self):
        '''@brief get a variety of loggin instances'''
        loggers = {'global_{}'.format(i):Logger for i in range(2)}
        loggers.update({'local_{}'.format(i):Logger(name='local_{}'.format(i)) for i in range(2)})
        # now do some logging
        for k in loggers.keys():
            for lvl in ['i','w','e','d']:
                lvl_name = LEVEL_ALIASES.get(lvl,lvl)
                loggers[k].set_verbose(0)
                loggers[k].log("this is a {} test on {}".format(lvl_name,k),lvl)
        return loggers

if __name__=='__main__':
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLogger)
    rv = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suite))  
    
    """
    mylog = Logger()
    for lvl in ['i','w','e','d']:
        lvl_name = LEVEL_ALIASES.get(lvl,lvl)
        mylog.log("this is a {} test".format(lvl_name),lvl)
        
    for lvl in ['info','warning','error','debug']:
        getattr(mylog,lvl)("This is a {} method test".format(lvl))
    """
        
    


