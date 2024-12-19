import binascii
from typing import *

from fafafa.fa_limits import *
from fafafa.fa_patterns import *
from fafafa.fa_url import FaUrl
from fafafa import fa_json as json

import base64
import copy
import pickle
from cached_property import cached_property


class FaValueUtils(object):
  @staticmethod
  def _typing_class(t: Any) -> Tuple[Type, Optional[Tuple]]:
    if isinstance(t, type):
      ret = t, ()
    elif str(t).startswith('typing.'):
      ret = t.__origin__, t.__args__
    else:
      ret = None, None
    return ret

  @staticmethod
  def str_to_bytes(s: Union[bytes, str], encoding: Optional[str] = 'utf-8') -> bytes:
    if isinstance(s, str):
      s = s.encode(encoding=encoding)
    return s

  @staticmethod
  def bytes_to_str(s: Union[bytes, str], encoding: Optional[str] = 'utf-8') -> str:
    if isinstance(s, bytes):
      s = s.decode(encoding=encoding)
    return s

  @staticmethod
  def auto_choose_base(base: Optional[Union[int, str]] = 'base32') -> int:
    if isinstance(base, int):
      base = str(base)

    if isinstance(base, str) and base.lower().startswith('base'):
      base = base[4:]

    if base in ('16', '32', '64', '85'):
      ret = int(base)
    else:
      ret = 32

    return ret

  @staticmethod
  def auto_choose_encoding(encoding: Optional[str] = 'utf-8') -> str:
    return encoding if encoding else 'utf-8'

  @staticmethod
  def base_encode(
    s: Union[bytes, str],
    base: Optional[Union[str, int]] = 'base32',
    encoding: Optional[str] = 'utf-8',
    with_meta: bool = False
  ) -> str:
    encoding = FaValueUtils.auto_choose_encoding(encoding)

    s = FaValueUtils.str_to_bytes(s, encoding=encoding)

    base = FaValueUtils.auto_choose_base(base)

    enc = getattr(base64, f'b{base}encode')
    assert callable(enc)

    ret = FaValueUtils.bytes_to_str(enc(s), encoding=encoding)

    if with_meta:
      ret = f'base{base},{ret}'

    return ret

  @staticmethod
  def base_decode(
    s: Union[bytes, str],
    base: Optional[Union[str, int]] = 'base32',
    encoding: Optional[str] = 'utf-8'
  ) -> Union[bytes, str]:
    encoding = FaValueUtils.auto_choose_encoding(encoding)

    s = FaValueUtils.bytes_to_str(s)

    if PATTERN_BASE_ENC.fullmatch(s):
      s_t = s.split(',', maxsplit=1)
      base = FaValueUtils.auto_choose_base(s_t[0][4:])
      s = s[1]
    else:
      base = FaValueUtils.auto_choose_base(base)

    dec = getattr(base64, f'b{base}decode')
    assert callable(dec)

    try:
      ret_t = dec(s)
    except binascii.Error:
      ret_t = s

    if isinstance(ret_t, bytes):
      try:
        ret = ret_t.decode(encoding=encoding)
      except UnicodeDecodeError:
        ret = ret_t
    else:
      ret = ret_t

    return ret

  @staticmethod
  def base_encode_v(
    v: Any,
    base: Optional[Union[str, int]] = 'base32',
    encoding: str = 'utf-8',
    encoder: str = 'json'
  ) -> str:
    encoder = encoder.lower() if isinstance(encoder, str) else 'json'
    if encoder == 'pickle':
      def enc(x):
        return pickle.dumps(x)
    else:
      def enc(x):
        return json.dumps(x, indent=0, ensure_ascii=False)

    s = enc(v)
    s = FaValueUtils.str_to_bytes(s)

    ret = FaValueUtils.base_encode(s, base=base, encoding=encoding, with_meta=True)

    return ret

  @staticmethod
  def base_decode_v(v: Any, encoding: str = None) -> Any:
    ret = v

    if isinstance(v, str):

      v = FaValueUtils.base_decode(v, encoding=encoding)

      if isinstance(v, bytes) and len(v) >= 3 and v[0] == 0x80 and v[-1] == ord('.'):
        def loads(x):
          return pickle.loads(x)
      else:
        def loads(x):
          return json.loads(x)

      if PATTERN_URL_QUERY.fullmatch(v) and v.count('"') == 0 and v.count("'") == 0 and (v.count('&') > 0 or v.count('=') > 0):
        ret = FaUrl.parse_query_str(v)
      else:
        try:
          ret = loads(v)
        except (pickle.PickleError, json.JSONDecodeError, TypeError, ValueError):
          ret = v

    return ret

  @staticmethod
  def is_callable(v: Any) -> bool:
    return callable(v)

  @staticmethod
  def is_function(v: Any) -> bool:
    return v.__class__.__name__ == 'function'

  @staticmethod
  def is_method(v: Any) -> bool:
    return v.__class__.__name__ == 'method'

  @staticmethod
  def is_none(v: Any, strict: bool = False) -> bool:
    ret = False
    if v is None:
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if v is None:
        ret = True
      elif isinstance(v, str) and PATTERN_NONE.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_bool(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, bool):
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, bool):
        ret = True
      elif isinstance(v, int) and v in (1, 0):
        ret = True
      elif isinstance(v, str) and PATTERN_BOOL.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_true(v: Any, strict: bool = False) -> bool:
    ret = False
    if v is True:
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if v is True:
        ret = True
      elif isinstance(v, int) and v == 1:
        ret = True
      elif isinstance(v, str) and PATTERN_TRUE.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_false(v: Any, strict: bool = False) -> bool:
    ret = False
    if v is False:
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if v is False:
        ret = True
      elif isinstance(v, int) and v == 0:
        ret = True
      elif isinstance(v, str) and PATTERN_FALSE.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_not_true(v: Any, strict: bool = False) -> bool:
    return not FaValueUtils.is_true(v, strict=strict)

  @staticmethod
  def is_not_false(v: Any, strict: bool = False) -> bool:
    return not FaValueUtils.is_false(v, strict=strict)

  @staticmethod
  def is_int(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, int) and not isinstance(v, bool):
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, int):
        ret = True
      elif isinstance(v, float) and abs(v - int(v)) <= FLOAT32_EPSILON:
        ret = True
      elif isinstance(v, str) and PATTERN_INT.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_float(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, float):
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, (int, float)):
        ret = True
      elif isinstance(v, str) and PATTERN_FLOAT.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_str(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, str):
      ret = True
    elif not strict:
      ret = True
    return ret

  @staticmethod
  def is_list(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, (tuple, list, set)):
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      ret = isinstance(v, (tuple, list, set, str, dict))
    return ret

  @staticmethod
  def is_dict(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, dict):
      ret = True
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      ret = isinstance(v, dict)
    return ret

  @staticmethod
  def to_bool(v: Any, default: Optional[bool] = None, strict: bool = False) -> Union[None, bool]:
    ret = default
    if isinstance(v, bool):
      ret = v
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, bool):
        ret = v
      elif isinstance(v, int):
        if v == 1:
          ret = True
        elif v == 0:
          ret = False
      elif isinstance(v, str):
        if PATTERN_TRUE.fullmatch(v):
          ret = True
        elif PATTERN_FALSE.fullmatch(v):
          ret = False
    return ret

  @staticmethod
  def to_int(v: Any, default: Optional[int] = None, strict: bool = False) -> Union[None, int]:
    ret = default
    if isinstance(v, int) and not isinstance(v, bool):
      ret = v
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, int):
        ret = int(v)
      elif isinstance(v, float) and abs(v - int(v)) <= FLOAT32_EPSILON:
        ret = int(v)
      elif isinstance(v, str) and PATTERN_INT.fullmatch(v):
        try:
          ret = int(v)
        except ValueError:
          pass
    return ret

  @staticmethod
  def to_float(v: Any, default: Optional[float] = None, strict: bool = False) -> Union[None, float]:
    ret = default
    if isinstance(v, float):
      ret = v
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, (int, float)):
        ret = float(v)
      elif isinstance(v, str) and PATTERN_FLOAT.fullmatch(v):
        try:
          ret = float(v)
        except ValueError:
          pass
    return ret

  @staticmethod
  def to_str(v: Any, default: Optional[str] = None, strict: bool = False) -> Union[None, str]:
    ret = default
    if isinstance(v, str):
      ret = v
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, str):
        ret = v
      else:
        try:
          ret = json.dumps(v, indent=0, ensure_ascii=False)
        except ValueError:
          ret = str(v)
    return ret

  @staticmethod
  def clone(v: Any, deep: Optional[bool] = None) -> Any:
    if deep is True:
      v = copy.deepcopy(v)
    elif deep is False:
      v = copy.copy(v)
    return v

  @staticmethod
  def to_list(v: Any, default: Optional[List] = None, strict: bool = False, deep_clone: Optional[bool] = None) -> Union[None, List]:
    ret = default

    if isinstance(v, list):
      ret = v
    elif isinstance(v, (tuple, set)):
      ret = list(v)
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, list):
        ret = v
      elif isinstance(v, (tuple, set)):
        ret = list(v)
      elif isinstance(v, str):
        ret = [v]
        for sp in ('|', ',', ';'):
          if v.find(sp) >= 0:
            ret = list(v.split(sp))
            break
      elif isinstance(v, dict):
        ret = list(v.items())

    ret = FaValueUtils.clone(ret, deep=deep_clone)

    return ret

  @staticmethod
  def to_dict(v: Any, default: Optional[Dict] = None, strict: bool = False, deep_clone: Optional[bool] = None) -> Union[None, Dict]:
    ret = default

    if isinstance(v, dict):
      ret = v
    elif not strict:
      v = FaValueUtils.base_decode_v(v)
      if isinstance(v, dict):
        ret = v

    ret = FaValueUtils.clone(ret, deep=deep_clone)

    return ret


class FaValue(object):
  def __init__(self, v: Any):
    self._raw_value = v.raw_value if isinstance(v, FaValue) else v

  @property
  def raw_value(self) -> Any:
    return self._raw_value

  @cached_property
  def bool_value(self) -> bool:
    return self.to_bool(default=False)

  @cached_property
  def int_value(self) -> int:
    return self.to_int(default=0)

  @cached_property
  def float_value(self) -> float:
    return self.to_float(default=0.0)

  @cached_property
  def str_value(self) -> str:
    return self.to_str(default='')

  @cached_property
  def list_value(self) -> list:
    return self.to_list(default=[])

  @cached_property
  def dict_value(self) -> dict:
    return self.to_dict(default={})

  def __bool__(self) -> bool:
    return self.bool_value

  def __int__(self) -> int:
    return self.int_value

  def __float__(self) -> float:
    return self.float_value

  def __str__(self) -> str:
    return self.str_value

  def is_callable(self) -> bool:
    return FaValueUtils.is_callable(self.raw_value)

  def is_function(self) -> bool:
    return FaValueUtils.is_function(self.raw_value)

  def is_method(self) -> bool:
    return FaValueUtils.is_method(self.raw_value)

  def is_none(self, strict: bool = False) -> bool:
    return FaValueUtils.is_none(self.raw_value, strict=strict)

  def is_bool(self, strict: bool = False) -> bool:
    return FaValueUtils.is_bool(self.raw_value, strict=strict)

  def is_true(self, strict: bool = False) -> bool:
    return FaValueUtils.is_true(self.raw_value, strict=strict)

  def is_false(self, strict: bool = False) -> bool:
    return FaValueUtils.is_false(self.raw_value, strict=strict)

  def is_not_true(self, strict: bool = False) -> bool:
    return FaValueUtils.is_not_true(self.raw_value, strict=strict)

  def is_not_false(self, strict: bool = False) -> bool:
    return FaValueUtils.is_not_false(self.raw_value, strict=strict)

  def is_int(self, strict: bool = False) -> bool:
    return FaValueUtils.is_int(self.raw_value, strict=strict)

  def is_float(self, strict: bool = False) -> bool:
    return FaValueUtils.is_float(self.raw_value, strict=strict)

  def is_num(self, strict: bool = False) -> bool:
    return self.is_float(strict=strict) or self.is_int(strict=strict)

  def is_str(self, strict: bool = False) -> bool:
    return FaValueUtils.is_str(self.raw_value, strict=strict)

  def is_list(self, strict: bool = False) -> bool:
    return FaValueUtils.is_list(self.raw_value, strict=strict)

  def is_dict(self, strict: bool = False) -> bool:
    return FaValueUtils.is_dict(self.raw_value, strict=strict)

  def to_bool(self, default: Optional[bool] = None, strict: bool = False) -> Union[None, bool]:
    return FaValueUtils.to_bool(self.raw_value, default=default, strict=strict)

  def to_int(self, default: Optional[int] = None, strict: bool = False) -> Union[None, int]:
    return FaValueUtils.to_int(self.raw_value, default=default, strict=strict)

  def to_float(self, default: Optional[float] = None, strict: bool = False) -> Union[None, float]:
    return FaValueUtils.to_float(self.raw_value, default=default, strict=strict)

  def to_str(self, default: Optional[str] = None, strict: bool = False) -> Union[None, str]:
    return FaValueUtils.to_str(self.raw_value, default=default, strict=strict)

  def to_list(self, default: Optional[list] = None, strict: bool = False) -> Union[None, list]:
    return FaValueUtils.to_list(self.raw_value, default=default, strict=strict)

  def to_dict(self, default: Optional[dict] = None, strict: bool = False) -> Union[None, dict]:
    return FaValueUtils.to_dict(self.raw_value, default=default, strict=strict)

  def __eq__(self, other: Any) -> bool:
    v = other.raw_value if isinstance(other, FaValue) else other
    return self.raw_value == v

  def __call__(self, *al, **kw):
    if self.is_callable():
      ret = self.raw_value(*al, **kw)
    else:
      ret = None
    return ret

  # -x
  def __neg__(self):
    if self.is_bool(strict=True):
      ret = not self.bool_value
    elif self.is_num(strict=True):
      ret = - self.raw_value
    else:
      ret = None
    return FaValue(ret)

  # ~x
  def __invert__(self):
    if self.is_bool(strict=True):
      ret = not self.bool_value
    elif self.is_int(strict=True):
      ret = ~self.int_value
    elif self.is_list(strict=True):
      ret = reversed(self.list_value)
    else:
      ret = None
    return ret

  # x | y
  def __or__(self, other) -> 'FaValue':
    other = FaValue(other)
    if other.is_callable():
      ret = other.raw_value(self)
    elif self.is_bool(strict=True) and other.is_bool(strict=True):
      ret = self.bool_value or other.bool_value
    elif self.is_int(strict=True) and other.is_int(strict=True):
      ret = self.int_value | other.int_value
    else:
      ret = None
    return FaValue(ret)

  # x & y
  def __and__(self, other) -> 'FaValue':
    other = FaValue(other)
    if self.is_str(strict=True) and other.is_str(strict=True):
      ret = f'{self.str_value}{other.str_value}'
    elif self.is_bool(strict=True) and other.is_bool(strict=True):
      ret = self.bool_value and other.bool_value
    elif self.is_int(strict=True) and other.is_int(strict=True):
      ret = self.int_value & other.int_value
    else:
      ret = None
    return FaValue(ret)

  # x ^ y
  def __xor__(self, other) -> 'FaValue':
    other = FaValue(other)
    if self.is_int(strict=True) and other.is_int(strict=True):
      ret = self.int_value ^ other.int_value
    else:
      ret = None
    return FaValue(ret)

  # x + y
  def __add__(self, other) -> 'FaValue':
    other = FaValue(other)
    ret = None
    if self.is_str(strict=True) and other.is_str(strict=True):
      ret = f'{self.str_value}{other.str_value}'
    elif self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value + other.raw_value
    elif self.is_list(strict=True):
      if other.is_list(strict=True):
        ret = self.list_value + other.list_value
      else:
        ret = copy.copy(self.list_value)
        ret.append(other.raw_value)
    elif self.is_dict(strict=True) and other.is_dict(strict=True):
      ret = copy.copy(self.dict_value)
      ret.update(other.dict_value)
    return FaValue(ret)

  # x - y
  def __sub__(self, other) -> 'FaValue':
    other = FaValue(other)
    ret = None
    if self.is_str(strict=True) and other.is_str(strict=True):
      ret = self.str_value.replace(other.str_value, '')
    elif self.is_num(strict=True) and other.is_num(strict=True):
        ret = self.raw_value - other.raw_value
    elif self.is_list(strict=True):
      if other.is_list(strict=True):
        other_s = set(other.list_value)
      else:
        other_s = set()
        other_s.add(other.raw_value)
      ret = [x for x in self.list_value if x not in other_s]
    elif self.is_dict(strict=True):
      if other.is_list(strict=True):
        self_d = self.dict_value
        other_s = set(other.list_value)

        ret = copy.copy(self_d)
        ret.clear()
        for k, v in self_d.items():
          if k not in other_s:
            ret[k] = v
      elif other.is_dict(strict=True):
        self_d = self.dict_value
        other_d = other.dict_value

        ret = copy.copy(self_d)
        ret.clear()
        for k, v in self_d.items():
          if not (k in other_d and other_d.get(k) == v):
            ret[k] = v

    return FaValue(ret)

  # x * y
  def __mul__(self, other) -> 'FaValue':
    other = FaValue(other)
    ret = None
    if self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value * other.raw_value
    return FaValue(ret)

  # x / y
  def __divmod__(self, other) -> 'FaValue':
    other = FaValue(other)
    ret = None
    if self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value / other.raw_value
    return FaValue(ret)

  # x % y
  def __mod__(self, other) -> 'FaValue':
    other = FaValue(other)
    ret = None
    if self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value % other.raw_value
    return FaValue(ret)

  # x ** y
  def __pow__(self, power: Union['FaValue', int, float]) -> 'FaValue':
    power = FaValue(power)
    ret = None
    if self.is_num(strict=True) and power.is_int(strict=True):
      ret = self.raw_value ** power.int_value
    return FaValue(ret)

  def __copy__(self) -> 'FaValue':
    return FaValue(copy.deepcopy(self.raw_value))
