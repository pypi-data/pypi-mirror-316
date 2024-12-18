from typing import *

import builtins
import asyncio
if asyncio.TimeoutError == builtins.TimeoutError:
  class FaBuiltinTimeoutError1(asyncio.TimeoutError):
    pass

  class FaBuiltinTimeoutError2(asyncio.TimeoutError):
    pass

  builtins.TimeoutError = FaBuiltinTimeoutError1
  asyncio.TimeoutError = FaBuiltinTimeoutError2
import aioredis
import calendar
import orjson
import pickle
import pytz
from datetime import date, datetime, timedelta
from collections import OrderedDict


class FaRedisEncoder(object):
  def encode(self, v: Any) -> bytes:
    pass

  def decode(self, s: bytes) -> Any:
    pass


class FaRedisJsonEncoder(FaRedisEncoder):
  def encode(self, v: Any) -> bytes:
    return orjson.dumps(v)

  def decode(self, s: bytes) -> Any:
    return orjson.loads(s)


class FaRedisPickleEncoder(FaRedisEncoder):
  def encode(self, v: Any) -> bytes:
    return pickle.dumps(v)

  def decode(self, s: bytes) -> Any:
    return pickle.loads(s)


class FaRedisSmartEncoder(FaRedisEncoder):
  def encode(self, v: Any) -> bytes:
    if isinstance(v, str):
      v = v.encode('utf-8')
    elif isinstance(v, (bool, int, float, list, dict)):
      try:
        v = orjson.dumps(v)
      except orjson.JSONEncodeError:
        v = pickle.dumps(v)
    else:
      v = pickle.dumps(v)
    return v

  def decode(self, s: bytes) -> Any:
    if isinstance(s, bytes):
      if len(s) >= 4 and s[0] == 0x80 and s[-1] == ord('.'):
        s = pickle.loads(s)
      else:
        try:
          s = orjson.loads(s)
        except orjson.JSONDecodeError:
          for enc in ('utf-8', 'gb2312', 'gbk'):
            try:
              s = s.decode(enc)
              break
            except UnicodeDecodeError:
              ...
    return s


################################################################################


class FaRedis(object):
  def __init__(self, redis: aioredis.Redis, now: Optional[datetime] = None, encoder: FaRedisEncoder = None):
    self._redis = redis
    self._now = now if isinstance(now, datetime) else datetime.now()
    self._encoder = encoder if isinstance(encoder, FaRedisEncoder) else FaRedisSmartEncoder()
    self._redis_info = None

  @staticmethod
  def from_url(url: str, now: Optional[datetime] = None, encoder: FaRedisEncoder = None, **kw) -> 'FaRedis':
    return FaRedis(aioredis.from_url(url, **kw), now, encoder)

  @property
  def now(self) -> datetime:
    return self._now

  @property
  def redis(self) -> aioredis.Redis:
    return self._redis

  def _dumps(self, v: Any) -> bytes:
    return self._encoder.encode(v)

  def _loads(self, s: bytes) -> Any:
    return self._encoder.decode(s)

  def _process_ttl(self, ttl: Optional[Union[int, float, timedelta, datetime, date]] = None) -> Optional[Union[int, timedelta]]:
    if isinstance(ttl, (int, float)):
      ttl = int(ttl)
    elif isinstance(ttl, timedelta):
      pass
    elif isinstance(ttl, datetime):
      ttl = ttl - self.now
    elif isinstance(ttl, date):
      ttl = datetime(*ttl.timetuple()[:3]) - self.now
    else:
      ttl = None

    return ttl

  def _process_at_ttl(self, ttl: Optional[Union[int, float, timedelta, datetime, date]] = None) -> Optional[Union[int, datetime]]:
    if isinstance(ttl, (int, float)):
      ttl = int(ttl)
    elif isinstance(ttl, timedelta):
      ttl = self.now + ttl
    elif isinstance(ttl, datetime):
      pass
    elif isinstance(ttl, date):
      ttl = datetime(*ttl.timetuple()[:3])
    else:
      ttl = None

    return ttl

  ################################################################################
  # SYSTEM
  ################################################################################

  async def execute_command(self, *args, **options):
    val = await self._redis.execute_command(*args, **options)
    val = self._encoder.decode(val)
    return val

  async def FLUSHDB(self, is_async: bool = False) -> int:
    return await self._redis.flushdb(is_async)

  async def TIME(self) -> datetime:
    ts, ms = await self._redis.time()
    return datetime.fromtimestamp(ts)

  async def INFO(self) -> dict:
    if not isinstance(self._redis_info, dict):
      self._redis_info = await self._redis.info()
    return self._redis_info

  async def VERSION(self) -> str:
    info = await self.INFO()
    return info.get('redis_version')

  async def VERSION_CMP(self, v: Union[str, tuple, list]) -> int:
    def _process_version(vv: Union[str, tuple, list]) -> list:
      if isinstance(vv, str):
        vv = [int(vvx) for vvx in vv.split('.')]
      elif isinstance(vv, (tuple, list)):
        vv = [int(vvx) for vvx in vv]
      else:
        vv = None

      return vv

    x = _process_version(await self.VERSION())
    y = _process_version(v)

    print(x, y)

    cmp = 0

    if isinstance(x, list) and isinstance(y, list):
      x += [0] * (max(len(x), len(y)) - len(x))
      y += [0] * (max(len(x), len(y)) - len(y))

      print(x, y)

      for i in range(len(x)):
        cmp = x[i] - y[i]
        if cmp != 0:
          break

    return cmp

  async def VERSION_EQ(self, v: Union[str, tuple, list]) -> bool:
    cmp = await self.VERSION_CMP(v)
    return cmp == 0

  async def VERSION_LT(self, v: Union[str, tuple, list]) -> bool:
    cmp = await self.VERSION_CMP(v)
    return cmp < 0

  async def VERSION_GT(self, v: Union[str, tuple, list]) -> bool:
    cmp = await self.VERSION_CMP(v)
    return cmp > 0

  async def VERSION_LE(self, v: Union[str, tuple, list]) -> bool:
    cmp = await self.VERSION_CMP(v)
    return cmp <= 0

  async def VERSION_GE(self, v: Union[str, tuple, list]) -> bool:
    cmp = await self.VERSION_CMP(v)
    return cmp >= 0

  ################################################################################
  # KEY
  ################################################################################

  async def DEL(self, *keys: str) -> int:
    return await self._redis.delete(*keys)

  async def EXISTS(self, *keys: str) -> int:
    return await self._redis.exists(*keys)

  async def _EXECUTE_EXPIRE_COMMAND(
    self,
    _ms: bool,
    _at: bool,
    key: str,
    ttl: Optional[Union[int, float, timedelta, datetime, date]] = None,
    nx: bool = False,
    xx: bool = False,
    gt: bool = False,
    lt: bool = False,
  ) -> int:
    if not isinstance(ttl, (int, datetime if _at else timedelta)):
      ret = await self.PERSIST(key)
    elif isinstance(ttl, int) and ttl <= 0:
      ret = await self.DEL(key)
    else:
      cmd = '{}EXPIRE{}'.format(
        'P' if _ms else '',
        'AT' if _at else '',
      )

      if _at:
        ttl = self._process_at_ttl(ttl)
        if isinstance(ttl, datetime):
          ttl = ttl.astimezone(pytz.UTC)
          if _ms:
            ttl = calendar.timegm(ttl.timetuple()) * 1000 + int(int(ttl.microsecond / 1000) % 1000)
          else:
            ttl = calendar.timegm(ttl.timetuple())
      else:
        ttl = self._process_ttl(ttl)
        if isinstance(ttl, timedelta):
          if _ms:
            ttl = int(ttl.total_seconds()) * 1000
          else:
            ttl = int(ttl.total_seconds())

      do_expire = True

      opt = None

      if nx:
        if xx or gt or lt:
          do_expire = False
        else:
          opt = 'NX'
      elif gt and lt:
        do_expire = False
      elif gt:
        opt = 'GT'
      elif lt:
        opt = 'LT'
      elif xx:
        opt = 'XX'

      if do_expire:
        if opt:
          if await self.VERSION_LE('7.0.0'):
            ret = await self._redis.execute_command(cmd, key, ttl, opt)
          else:
            old_ttl = await self._redis.ttl(key)

            if isinstance(old_ttl, int):
              do_expire = (opt == 'NX')
            else:
              do_expire = (opt == 'XX' or (opt == 'GT' and ttl > old_ttl) or (opt == 'LT' and ttl < old_ttl))

            if do_expire:
              ret = await self._redis.execute_command(cmd, key, ttl)
            else:
              ret = 0
        else:
          ret = await self._redis.execute_command(cmd, key, ttl)
      else:
        ret = 0

    return ret

  async def EXPIRE(
    self,
    key: str,
    ttl: Optional[Union[int, float, timedelta, datetime, date]] = None,
    nx: bool = False,
    xx: bool = False,
    gt: bool = False,
    lt: bool = False,
  ):
    return await self._EXECUTE_EXPIRE_COMMAND(False, False, key, ttl, nx, xx, gt, lt)

  async def EXPIREAT(
    self,
    key: str,
    ttl: Optional[Union[int, float, timedelta, datetime, date]] = None,
    nx: bool = False,
    xx: bool = False,
    gt: bool = False,
    lt: bool = False,
  ):
    return await self._EXECUTE_EXPIRE_COMMAND(False, True, key, ttl, nx, xx, gt, lt)

  async def KEYS(self, pattern: str = '*') -> list[str]:
    return await self._redis.keys(pattern)

  async def MOVE(self, key: str, db: int) -> int:
    return await self._redis.move(key, db)

  async def PERSIST(self, key: str) -> int:
    return await self._redis.persist(key)

  async def PEXPIRE(
    self,
    key: str,
    ttl: Optional[Union[int, float, timedelta, datetime, date]] = None,
    nx: bool = False,
    xx: bool = False,
    gt: bool = False,
    lt: bool = False,
  ):
    return await self._EXECUTE_EXPIRE_COMMAND(True, False, key, ttl, nx, xx, gt, lt)

  async def PEXPIREAT(
    self,
    key: str,
    ttl: Optional[Union[int, float, timedelta, datetime, date]] = None,
    nx: bool = False,
    xx: bool = False,
    gt: bool = False,
    lt: bool = False,
  ):
    return await self._EXECUTE_EXPIRE_COMMAND(True, True, key, ttl, nx, xx, gt, lt)

  async def PTTL(self, key: str) -> int:
    return await self._redis.pttl(key)

  async def RANDOMKEY(self) -> str:
    return await self._redis.randomkey()

  async def RENAME(self, key: str, new_key: str):
    return await self._redis.rename(key, new_key)

  async def RENAMENX(self, key: str, new_key: str):
    return await self._redis.renamenx(key, new_key)

  async def SORT(
    self,
    key: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    by: Optional[str] = None,
    get: Optional[str] = None,
    desc: bool = False,
    alpha: bool = False,
    store: Optional[str] = None,
  ) -> list:
    return await self._redis.sort(
      key,
      start=offset,
      num=limit,
      by=by,
      get=get,
      desc=desc,
      alpha=alpha,
      store=store,
    )

  async def TTL(self, key: str) -> int:
    return await self._redis.ttl(key)

  async def TYPE(self, key: str) -> str:
    return await self._redis.type(key)

  async def TYPE_IS_NONE(self, key: str) -> bool:
    return (await self._redis.type(key)) == 'none'

  async def TYPE_IS_STRING(self, key: str) -> bool:
    return (await self._redis.type(key)) == 'string'

  async def TYPE_IS_LIST(self, key: str) -> bool:
    return (await self._redis.type(key)) == 'list'

  async def TYPE_IS_SET(self, key: str) -> bool:
    return (await self._redis.type(key)) == 'set'

  async def TYPE_IS_ZSET(self, key: str) -> bool:
    return (await self._redis.type(key)) == 'zset'

  async def TYPE_IS_HASH(self, key: str) -> bool:
    return (await self._redis.type(key)) == 'hash'

  ################################################################################
  # STRING
  ################################################################################

  async def APPEND(self, key: str, val: str) -> int:
    return await self._redis.append(key, val)

  async def BITCOUNT(self, key: str, start: Optional[int] = None, end: Optional[int] = None) -> int:
    return await self._redis.bitcount(key, start=start, end=end)

  async def BITOP(self, op: str, dst: str, *keys: str) -> int:
    return await self._redis.bitop(op, dst, *keys)

  async def BITOP_AND(self, dst: str, *keys: str) -> int:
    return await self._redis.bitop('AND', dst, *keys)

  async def BITOP_OR(self, dst: str, *keys: str) -> int:
    return await self._redis.bitop('OR', dst, *keys)

  async def BITOP_XOR(self, dst: str, *keys: str) -> int:
    return await self._redis.bitop('XOR', dst, *keys)

  async def BITOP_NOT(self, dst: str, *keys: str) -> int:
    return await self._redis.bitop('NOT', dst, *keys)

  async def DECR(self, key: str, val: int = 1) -> int:
    return await self._redis.decrby(key, val)

  async def DECRBY(self, key: str, val: int = 1) -> int:
    return await self._redis.decrby(key, val)

  async def GET(self, key: str, default: Any = None) -> Any:
    val = await self._redis.get(key)

    if val is None and not self._redis.exists(key):
      val = default
    else:
      val = self._encoder.decode(val)

    return val

  async def GETBIT(self, key: str, offset: int = 0) -> int:
    return await self._redis.getbit(key, offset)

  async def GETRANGE(self, key: str, start: int = 0, end: int = -1) -> str:
    val = await self._redis.getrange(key, start, end)
    val = self._encoder.decode(val)

    return val

  async def GETSET(self, key: str, val: Any) -> Any:
    val = self._encoder.encode(val)

    old_val = await self._redis.getset(key, val)
    old_val = self._encoder.decode(old_val)

    return old_val

  async def INCR(self, key: str, val: int = 1) -> int:
    return await self._redis.incr(key, val)

  async def INCRBY(self, key: str, val: int = 1) -> int:
    return await self._redis.incrby(key, val)

  async def INCRBYFLOAT(self, key: str, val: float = 1.0) -> float:
    return await self._redis.incrbyfloat(key, val)

  async def MGET(self, keys: list[str]) -> list:
    vals = await self._redis.mget(keys)

    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def MSET(self, items: Union[dict, list]) -> int:
    _items = dict()

    if isinstance(items, dict):
      for k, v in items.items():
        _items[k] = self._encoder.encode(v)
    elif isinstance(items, list) and len(items) > 0:
      if isinstance(items[0], tuple) and len(items[0]) == 2:
        for k, v in items:
          _items[k] = self._encoder.encode(v)
      elif len(items) % 2 == 0:
        for i in range(0, len(items), 2):
          k = items[i]
          v = self._encoder.encode(items[i + 1])
          _items[k] = v

    return await self._redis.mset(_items)

  async def MSETNX(self, items: Union[dict, list[tuple[str, Any]]]) -> int:
    args = dict()

    if isinstance(items, dict):
      for k, v in items.items():
        args[k] = self._encoder.encode(v)
    elif isinstance(items, list):
      for k, v in items:
        args[k] = self._encoder.encode(v)

    return await self._redis.msetnx(args)

  async def SET(
    self,
    key: str,
    val: Any,
    ex: Optional[Union[int, float, timedelta, datetime, date]] = None,
    px: Optional[Union[int, float, timedelta, datetime, date]] = None,
    nx: bool = False,
    xx: bool = False,
  ) -> int:
    val = self._encoder.encode(val)
    ex = self._process_ttl(ex)
    px = self._process_ttl(px)
    return await self._redis.set(key, val, ex=ex, px=px, nx=nx, xx=xx)

  async def SETBIT(self, key: str, offset: int, val: Union[int, bool, Any]) -> int:
    val = int(bool(val))
    return await self._redis.setbit(key, offset, val)

  async def SETRANGE(self, key: str, offset: int, val: Any):
    val = self._encoder.encode(val)
    return await self._redis.setrange(key, offset, val)

  async def STRLEN(self, key: str) -> int:
    return await self._redis.strlen(key)

  ################################################################################
  # HASH
  ################################################################################

  async def HDEL(self, key: str, *fields: str) -> int:
    return await self._redis.hdel(key, *fields)

  async def HEXISTS(self, key: str, field: str) -> int:
    return await self._redis.hexists(key, field)

  async def HGET(self, key: str, field: str) -> Any:
    val = await self._redis.hget(key, field)
    val = self._encoder.decode(val)

    return val

  async def HGETALL(self, key: str) -> dict[str, Any]:
    ret = OrderedDict()

    items = await self._redis.hgetall(key)
    if isinstance(items, dict):
      for k, v in items.items():
        ret[k] = self._encoder.decode(v)
    elif isinstance(items, list) and len(items) > 0:
      if len(items[0]) == 1:
        for i in range(0, len(items), 2):
          k = items[i]
          v = self._encoder.decode(items[i + 1])
          ret[k] = v
      elif len(items[0]) == 2:
        for k, v in items:
          ret[k] = self._encoder.decode(v)

    return ret

  async def HINCR(self, key: str, field: str, val: int = 1) -> int:
    return await self._redis.hincrby(key, field, val)

  async def HINCRBY(self, key: str, field: str, val: int = 1) -> int:
    return await self._redis.hincrby(key, field, val)

  async def HINCRBYFLOAT(self, key: str, field: str, val: float = 1.0) -> int:
    return await self._redis.hincrbyfloat(key, field, val)
  
  async def HKEYS(self, key: str) -> list[str]:
    return await self._redis.hkeys(key)

  async def HLEN(self, key: str) -> int:
    return await self._redis.hlen(key)

  async def HMGET(self, key: str, *fields: str) -> list:
    vals = await self._redis.hmget(key, fields)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def HSET(self, key: str, field: Optional[str] = None, val: Any = None, items: Optional[Union[dict, list]] = None) -> int:
    _items = dict()

    if isinstance(items, dict):
      for f, v in items.items():
        _items[f] = self._encoder.encode(v)
    elif isinstance(items, list):
      if len(items) > 0:
        if isinstance(items[0], tuple) and len(items[0]) == 2:
          for f, v in items:
            _items[f] = self._encoder.encode(v)
        elif len(items) % 2 == 0:
          for i in range(0, len(items), 2):
            f = items[i]
            v = self._encoder.encode(items[i + 1])
            _items[f] = v
    else:
      _items[field] = self._encoder.encode(val)

    return await self._redis.hset(key, mapping=_items)

  async def HSETNX(self, key: str, field: str, val: Any) -> int:
    val = self._encoder.encode(val)

    return await self._redis.hsetnx(key, field, val)

  async def HVALS(self, key: str) -> list:
    vals = await self._redis.hvals(key)
    vals = [self._encoder.encode(x) for x in vals]

    return vals

  ################################################################################
  # LIST
  ################################################################################

  async def BLPOP(self, keys: Union[str, list[str]], timeout: int = 0) -> list:
    res = await self._redis.blpop(keys, timeout)

    if isinstance(res, (list, tuple)) and len(res) == 2:
      k, v = res
      res = k, self._encoder.decode(v)

    return res

  async def BRPOP(self, keys: Union[str, list[str]], timeout: int = 0) -> list:
    res = await self._redis.brpop(keys, timeout)

    if isinstance(res, (list, tuple)) and len(res) == 2:
      k, v = res
      res = k, self._encoder.decode(v)

    return res

  async def LINDEX(self, key: str, index: int = 0) -> Any:
    val = await self._redis.lindex(key, index)
    val = self._encoder.decode(val)

    return val

  async def LINSERT(self, key: str, val: Any, where: str, target_key: str) -> int:
    val = self._encoder.encode(val)

    return await self._redis.linsert(
      key,
      where=where,
      refvalue=target_key,
      value=val,
    )

  async def LINSERT_BEFORE(self, key: str, val: Any, target_key: str) -> int:
    return await self.LINSERT(key, val, 'BEFORE', target_key)

  async def LINSERT_AFTER(self, key: str, val: Any, target_key: str) -> int:
    return await self.LINSERT(key, val, 'AFTER', target_key)

  async def LLEN(self, key: str) -> int:
    return await self._redis.llen(key)

  async def LPOP(self, key: str, count: int = 1, as_list: bool = False) -> Union[list, Any]:
    if isinstance(count, int) and count > 1:
      vals = await self._redis.execute_command('LPOP', key, count)

      ret = [self._encoder.decode(x) for x in vals]
    else:
      val = await self._redis.lpop(key)
      if isinstance(val, list) and len(val) == 1:
        val = val[0]

      ret = self._encoder.decode(val)
      if as_list:
        ret = [ret]

    return ret

  async def LPUSH(self, key: str, *vals: Any) -> int:
    vals = [self._encoder.encode(x) for x in vals]

    return await self._redis.lpush(key, *vals)

  async def LRANGE(self, key: str, start: int = 0, end: int = -1) -> list:
    vals = await self._redis.lrange(key, start, end)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def LREM(self, key: str, val: Any, count: int = 0):
    val = self._encoder.encode(val)
    return await self._redis.lrem(key, count, val)

  async def LSET(self, key: str, val: Any, index: int):
    val = self._encoder.encode(val)
    return await self._redis.lset(key, index, val)

  async def LTRIM(self, key: str, start: int = 0, end: int = -1):
    return await self._redis.ltrim(key, start, end)

  async def RPOP(self, key: str, count: int = 1, as_list: bool = False) -> Union[list, Any]:
    if isinstance(count, int) and count > 1:
      vals = await self._redis.execute_command('RPOP', key, count)

      ret = [self._encoder.decode(x) for x in vals]
    else:
      val = await self._redis.rpop(key)
      if isinstance(val, list) and len(val) == 1:
        val = val[0]

      ret = self._encoder.decode(val)
      if as_list:
        ret = [ret]

    return ret

  async def RPUSH(self, key: str, *vals: Any) -> int:
    vals = [self._encoder.encode(x) for x in vals]

    return await self._redis.rpush(key, *vals)

  async def RPUSHX(self, key: str, *vals: Any) -> int:
    vals = [self._encoder.encode(x) for x in vals]

    return await self._redis.execute_command("RPUSH", key, *vals)

  ################################################################################
  # SET
  ################################################################################

  async def SADD(self, key: str, *vals: Any) -> int:
    vals = [self._encoder.encode(x) for x in vals]

    return await self._redis.sadd(key, *vals)

  async def SCARD(self, key: str) -> int:
    return await self._redis.scard(key)

  async def SDIFF(self, *keys: str) -> list:
    vals = await self._redis.sdiff(keys)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def SDIFFSTORE(self, dst: str, *keys: str) -> list:
    vals = await self._redis.sdiffstore(dst, keys)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def SINTER(self, *keys: str) -> list:
    vals = await self._redis.sinter(keys)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def SINTERSTORE(self, dst: str, *keys: str) -> list:
    vals = await self._redis.sinterstore(dst, keys)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def SISMEMBER(self, key: str, val: Any) -> int:
    val = self._encoder.encode(val)
    return await self._redis.sismember(key, val)

  async def SMEMBERS(self, key: str) -> list:
    vals = await self._redis.smembers(key)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def SMOVE(self, from_key: str, to_key: str, val: Any) -> int:
    val = self._encoder.encode(val)

    return await self._redis.smove(from_key, to_key, val)

  async def SPOP(self, key: str, count: int = 1, as_list: bool = False) -> Union[list, Any]:
    vals = await self._redis.spop(key, count)
    if isinstance(vals, (list, set)):
      vals = list(vals)
    else:
      vals = [vals]

    vals = [self._encoder.decode(x) for x in vals]

    if len(vals) == 1 and not as_list:
      vals = vals[0]

    return vals

  async def SRANDMEMBER(self, key: str, count: int = 1, as_list: bool = False) -> Union[list, Any]:
    vals = await self._redis.srandmember(key, count)
    if isinstance(vals, (list, set)):
      vals = list(vals)
    else:
      vals = [vals]

    vals = [self._encoder.decode(x) for x in vals]

    if len(vals) == 1 and not as_list:
      vals = vals[0]

    return vals

  async def SREM(self, key: str, *vals: Any) -> int:
    vals = [self._encoder.encode(x) for x in vals]

    return await self._redis.srem(key, *vals)

  async def SUNION(self, *keys: str) -> list:
    vals = await self._redis.sunion(keys)
    vals = [self._encoder.decode(x) for x in vals]

    return vals

  async def SUNIONSTORE(self, dst: str, *keys: str) -> list:
    vals = await self._redis.sunionstore(dst, keys)
    vals = [self._encoder.decode(x) for x in vals]

    return vals
