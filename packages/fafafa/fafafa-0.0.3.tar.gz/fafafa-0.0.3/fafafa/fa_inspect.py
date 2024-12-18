from typing import *

import importlib
import inspect


def get_method_class(method: Callable) -> Optional[Type]:
  ret = None

  if getattr(method, '__class__').__name__ in ('function', 'method') and method.__qualname__ != method.__name__:
    try:
      mod = importlib.import_module(getattr(method, '__module__'))
      cls_name = method.__qualname__[:-len(method.__name__) - 1]
      cls = getattr(mod, cls_name, None)
      if cls is not None and isinstance(cls, type):
        ret = cls
    except ModuleNotFoundError as e:
      import traceback
      traceback.print_exc()
      pass
  return ret


CLASS_METHOD_KINDS = ('method',)
STATIC_METHOD_KINDS = ('function',)
INSTANCE_METHOD_KINDS = ('function', 'method')
DEFAULT_METHOD_KINDS = ('function', 'method')


def is_method(method: Callable, kinds: Union[str, list, tuple] = DEFAULT_METHOD_KINDS) -> bool:
  ret = False
  if callable(method):
    __class__ = getattr(method, '__class__', None)
    if isinstance(__class__, type):
      __name__ = getattr(__class__, '__name__', None)

      if isinstance(kinds, str):
        kinds = (kinds,)
      elif isinstance(kinds, (tuple, list)):
        kinds = tuple(kinds)
      else:
        kinds = DEFAULT_METHOD_KINDS

      if __name__ in kinds:
        ret = True
  return ret


def is_static_method(method: Callable) -> bool:
  ret = False
  if is_method(method, STATIC_METHOD_KINDS):
    args = inspect.getfullargspec(method).args
    ret = not len(args) or args[0] not in ('cls', 'self')
  return ret


def is_class_method(method: Callable) -> bool:
  ret = False
  if is_method(method, CLASS_METHOD_KINDS):
    args = inspect.getfullargspec(method).args
    ret = len(args) >= 1 and args[0] == 'cls'
  return ret


def is_instance_method(method: Callable) -> bool:
  ret = False
  if is_method(method, INSTANCE_METHOD_KINDS):
    args = inspect.getfullargspec(method).args
    ret = len(args) >= 1 and args[0] == 'self'
  return ret
