from typing import *

import copy


class FaDecoratorHook(object):
  def __init__(self, *al, **kw):
    self._al = copy.copy(list(al))
    self._kw = copy.copy(kw)

  @property
  def al(self) -> List:
    return self._al

  @property
  def kw(self) -> Dict:
    return self._kw

  def filter(self, target: Any) -> bool:
    """
    用于判断目前对象(方法、类)是否符合要求
    """
    raise NotImplementedError()

  def target(self, target: Any) -> Any:
    """
    将原始对象(方法、类)处理后，返回处理后的包装对象
    """
    raise NotImplementedError()

  def set_args(self, *al, **kw):
    self._al = copy.copy(list(al))
    self._kw = copy.copy(kw)

  def get_arg(self, k: Union[int, str, List[Union[int, str]]], default: Optional[Any] = None) -> Any:
    ret = default
    if isinstance(k, int):
      if len(self.al) > k:
        ret = self.al[k]
    elif isinstance(k, str):
      if k in self.kw:
        ret = self.kw[k]
    elif isinstance(k, (list, tuple)):
      for kk in k:
        if isinstance(kk, int):
          if len(self.al) > kk:
            ret = self.al[kk]
            break
        elif isinstance(kk, str):
          if kk in self.kw:
            ret = self.kw[kk]
            break
    return ret


class FaDecoratorDefaultHook(FaDecoratorHook):
  def filter(self, target: Any) -> bool:
    return True

  def target(self, target: Any) -> Any:
    return target


def FaDecorator(hook_cls: Optional[Type[FaDecoratorHook]] = None):
  if isinstance(hook_cls, FaDecoratorHook):
    hook_cls = hook_cls.__class__

  if not (isinstance(hook_cls, type) and issubclass(hook_cls, FaDecoratorHook)) or hook_cls == FaDecoratorHook:
    hook_cls = FaDecoratorDefaultHook

  def __decorator__(*al, **kw):
    hook = hook_cls()

    def __target__(target):
      return hook.target(target)

    if len(al) == 1 and len(kw) == 0 and hook.filter(al[0]):
      return __target__(al[0])

    hook.set_args(*al, **kw)

    return __target__

  return __decorator__
