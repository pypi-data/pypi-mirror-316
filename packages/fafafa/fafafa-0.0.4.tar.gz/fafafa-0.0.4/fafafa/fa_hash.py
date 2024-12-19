from typing import *

import os
import hashlib
import aiofiles


class FaHash(object):
  MD5 = 'md5'
  SHA1 = 'sha1'
  SHA224 = 'sha224'
  SHA256 = 'sha256'
  SHA384 = 'sha384'
  SHA512 = 'sha512'
  BLAKE2B = 'blake2b'
  BLAKE2S = 'blake2s'
  SHA3_224 = 'sha3_224'
  SHA3_256 = 'sha3_256'
  SHA3_384 = 'sha3_384'
  SHA3_512 = 'sha3_512'
  SHAKE_128 = 'shake_128'
  SHAKE_256 = 'shake_256'

  def __init__(self, algorithm: str = SHA1):
    self._algorithm = algorithm
    self._hashlib = getattr(hashlib, algorithm)

  async def hash_str(self, s: Union[str, bytes]) -> str:
    h = self._hashlib()

    if isinstance(s, str):
      s = s.encode('utf-8')
    h.update(s)

    return h.hexdigest()

  async def hash_file(self, f: str, buf_size: Optional[int] = 1024 * 1024 * 10) -> str:
    h = self._hashlib()

    if os.path.isfile(f):
      async with aiofiles.open(f, 'rb') as fo:
        if isinstance(buf_size, int) and buf_size > 0:
          while True:
            buf = await fo.read(buf_size)
            if not buf:
              break
            h.update(buf)
        else:
          buf = await fo.read()
          h.update(buf)

    return h.hexdigest()


################################################################################
# HASH STRING
################################################################################


async def md5_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.MD5).hash_str(s)


async def sha1_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA1).hash_str(s)


async def sha224_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA224).hash_str(s)


async def sha256_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA256).hash_str(s)


async def sha384_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA384).hash_str(s)


async def sha512_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA512).hash_str(s)


async def blake2b_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.BLAKE2B).hash_str(s)


async def blake2s_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.BLAKE2S).hash_str(s)


async def sha3_224_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA3_224).hash_str(s)


async def sha3_256_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA3_256).hash_str(s)


async def sha3_384_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA3_384).hash_str(s)


async def sha3_512_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHA3_512).hash_str(s)


async def shake_128_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHAKE_128).hash_str(s)


async def shake_256_str(s: Union[str, bytes]) -> str:
  return await FaHash(FaHash.SHAKE_256).hash_str(s)


################################################################################
# HASH FILE
################################################################################


async def md5_file(f: str) -> str:
  return await FaHash(FaHash.MD5).hash_file(f)


async def sha1_file(f: str) -> str:
  return await FaHash(FaHash.SHA1).hash_file(f)


async def sha224_file(f: str) -> str:
  return await FaHash(FaHash.SHA224).hash_file(f)


async def sha256_file(f: str) -> str:
  return await FaHash(FaHash.SHA256).hash_file(f)


async def sha384_file(f: str) -> str:
  return await FaHash(FaHash.SHA384).hash_file(f)


async def sha512_file(f: str) -> str:
  return await FaHash(FaHash.SHA512).hash_file(f)


async def blake2b_file(f: str) -> str:
  return await FaHash(FaHash.BLAKE2B).hash_file(f)


async def blake2s_file(f: str) -> str:
  return await FaHash(FaHash.BLAKE2S).hash_file(f)


async def sha3_224_file(f: str) -> str:
  return await FaHash(FaHash.SHA3_224).hash_file(f)


async def sha3_256_file(f: str) -> str:
  return await FaHash(FaHash.SHA3_256).hash_file(f)


async def sha3_384_file(f: str) -> str:
  return await FaHash(FaHash.SHA3_384).hash_file(f)


async def sha3_512_file(f: str) -> str:
  return await FaHash(FaHash.SHA3_512).hash_file(f)


async def shake_128_file(f: str) -> str:
  return await FaHash(FaHash.SHAKE_128).hash_file(f)


async def shake_256_file(f: str) -> str:
  return await FaHash(FaHash.SHAKE_256).hash_file(f)
