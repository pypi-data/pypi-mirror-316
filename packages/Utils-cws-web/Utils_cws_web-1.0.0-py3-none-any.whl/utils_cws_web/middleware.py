from typing import Any
from functools import wraps

class Middleware:
    _instances = {}

    def __init__(self):
        self.__pre = None
        self.__post = None
        self.__class__._instances[self.__class__] = self

    @property
    def pre(self) -> Any:
        return self.__pre

    @pre.setter
    def pre(self, value: Any):
        self.__pre = value   

    @property
    def post(self) -> Any:
        return self.__post

    @post.setter
    def post(self, value: Any):
        self.__post = value   

    @classmethod
    def get_instance(cls) -> "Middleware":
        if cls not in cls._instances:
            raise ValueError(f"No active instance found for {cls.__name__}")
        return cls._instances[cls]

    @classmethod
    def middleware_in(cls):
        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                instance = cls.get_instance()
                if not instance.pre:
                    raise ValueError(f"Middleware '{cls.__name__}' does not have a 'pre' function defined")
                pre_value = instance.pre(*args, **kwargs)
                return function(pre=pre_value, *args, **kwargs)
            return wrapper
        return decorator
    
    @classmethod
    def middleware_out(cls):
        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                instance = cls.get_instance()
                if not (instance.pre and instance.post):
                    raise ValueError(f"Middleware '{cls.__name__}' does not have both 'pre' and 'post' functions defined")
                pre_value = instance.pre(*args, **kwargs)
                result = function(pre=pre_value, *args, **kwargs)
                return instance.post(result)
            return wrapper
        return decorator