
#%% Some function decorators for deprecation
import warnings
import functools

import functools
import inspect
import warnings

string_types = (type(b''), type(u''))

def deprecated(reason):
    """
    @brief decorator for deprecating old functions  
    @cite laurent laporte https://stackoverflow.com/questions/2536307/decorators-in-the-python-standard-lib-deprecated-specifically  
    @param[in] reason - why its deprecated and what to do  
    """
    if isinstance(reason, string_types):

        # The @deprecated is used with a 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated("please, use another function")
        #    def old_function(x, y):
        #      pass
        def decorator(func1):
            if inspect.isclass(func1):
                fmt1 = "Call to deprecated class {name} ({reason})."
            else:
                fmt1 = "Call to deprecated function {name} ({reason})."
            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)
            return new_func1
        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        # The @deprecated is used without any 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated
        #    def old_function(x, y):
        #      pass
        func2 = reason
        if inspect.isclass(func2):
            fmt2 = "Call to deprecated class {name}."
        else:
            fmt2 = "Call to deprecated function {name}."
        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs) 
        return new_func2

    else:
        raise TypeError(repr(type(reason)))


#incomplete functino decorator
def incomplete(reason):
    """
    @brief decorator for incomplete functions  
    @param[in] reason - reason that its incomplete. Unlike deprecation this REQUIRES a reason  
    """
    def decorator(func1):
        if inspect.isclass(func1):
            fmt1 = "Call to incomplete class {name} ({reason})."
        else:
            fmt1 = "Call to incomplete function {name} ({reason})."
        @functools.wraps(func1)
        def new_func1(*args, **kwargs):
            warnings.simplefilter('always', UserWarning)
            warnings.warn(
                fmt1.format(name=func1.__name__, reason=reason),
                category=UserWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', UserWarning)
            return func1(*args, **kwargs)
        return new_func1
    return decorator
