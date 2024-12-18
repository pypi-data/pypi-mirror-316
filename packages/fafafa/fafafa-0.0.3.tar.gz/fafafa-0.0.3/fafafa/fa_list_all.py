from typing import *


class FaListAll(object):
  def __init__(
    self,
    func: Callable,
    page_name: str = 'page',
    page_size_name: str = 'page_size',
    page: int = 1,
    page_size: Optional[int] = None,
    params: Optional[dict] = None,
    ignore_page_size: bool = False
  ):
    self.func = func
    self.page_name = page_name
    self.page_size_name = page_size_name
    self.page = page
    self.page_size = page_size
    self.params = params.copy() if isinstance(params, dict) else dict()
    self.ignore_page_size = ignore_page_size

    self.index = -1
    self.items = None
    self.last_page_size = 0

  def _make_params(self, page: int):
    ret = self.params.copy()

    ret[self.page_name] = page
    ret[self.page_size_name] = self.page_size

    return ret

  async def _fetch_new_page(self):
    kw = self._make_params(self.page)

    res = self.func(**kw)
    if isinstance(res, Awaitable):
      res = await res
    items = list(res)

    self.page += 1
    self.last_page_size = len(items)

    if isinstance(self.items, list):
      self.items.extend(items)
    else:
      self.items = list(items)

  async def _fetch_next_page(self):
    if not isinstance(self.items, list):
      await self._fetch_new_page()
    elif self.index + 1 >= len(self.items):
      if self.ignore_page_size or not self.page_size:
        if self.last_page_size > 0:
          await self._fetch_new_page()
      elif self.last_page_size >= self.page_size:
        await self._fetch_new_page()

    if (self.index + 1) < len(self.items):
      self.index += 1
      return self.items[self.index]
    else:
      raise StopIteration()

  def __aiter__(self):
    return self

  async def __anext__(self):
    await self._fetch_next_page()
