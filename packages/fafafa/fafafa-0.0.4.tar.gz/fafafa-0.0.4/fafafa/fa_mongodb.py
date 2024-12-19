from typing import *

import re
import uuid
import random
import motor
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime


class FaMongoDB(object):
  def __init__(self, mongo: AsyncIOMotorClient, database: str, now: Optional[datetime] = None):
    self._mongo = mongo
    self._db = mongo.get_database(database)
    self._now = now if isinstance(now, datetime) else datetime.now()

  @property
  def mongo(self) -> AsyncIOMotorClient:
    return self._mongo

  @property
  def db(self) -> motor.MotorDatabase:
    return self._db

  @property
  def now(self) -> datetime:
    return self._now

  @staticmethod
  def from_url(url: str, database: str, now: Optional[datetime] = None, **kw) -> 'FaMongoDB':
    return FaMongoDB(AsyncIOMotorClient(url, **kw), database, now)

  @staticmethod
  def _preprocess_sort(sort: Optional[Union[Tuple, List, OrderedDict]]):
    items = []
    if isinstance(sort, (tuple, list)):
      if len(sort) == 2 and isinstance(sort[0], str) and sort[1] in [1, -1]:
        items = [tuple(sort)]
      else:
        for item in sort:
          if isinstance(item, (tuple, list)) and len(item) == 2 and isinstance(item[0], str) and item[1] in [1, -1]:
            items.append(tuple(item))
    elif isinstance(sort, OrderedDict):
      for (k, v) in sort.items():
        if isinstance(k, str) and v in [1, -1]:
          items.append((k, v))

    items = items if len(items) else None
    return items

  @staticmethod
  def is_object_id(object_id: Union[ObjectId, str, uuid.UUID], strict: bool = False):
    ret = False
    if isinstance(object_id, ObjectId) or (isinstance(object_id, str) and re.match(r'[0-9a-f]{24}', object_id)):
      ret = True
    elif not strict and (isinstance(str, uuid.UUID) or (
      isinstance(object_id, str) and re.match(r'[0-9a-f]{24}', object_id.replace('-', '')))):
      ret = True
    return ret

  @staticmethod
  def make_object_id(object_id: Union[ObjectId, str, uuid.UUID]):
    if not isinstance(object_id, ObjectId):
      object_id = ObjectId(str(object_id).replace('-', ''))
    return object_id

  def get_collection(self, collection_name: str) -> motor.MotorCollection:
    return self._db.get_collection(collection_name)

  async def count(self, collection_name: str, filter: Optional[dict] = None) -> int:
    return await self.get_collection(collection_name).count_documents(filter)

  async def exists(self, collection_name: str, filter: Optional[Dict] = None) -> bool:
    return bool(await self.get_collection(collection_name).find_one(filter))

  async def find_one(
    self,
    collection_name: str,
    filter: Optional[Dict] = None,
    sort: Optional[Union[Tuple, List, OrderedDict]] = None,
    projection: Optional[Dict] = None,
    fn_process_item: Optional[Callable] = None
  ) -> Optional[Dict]:
    sort = self._preprocess_sort(sort)

    item = await self.get_collection(collection_name).find_one(filter, sort=sort, projection=projection)
    if callable(fn_process_item) and item:
      item = fn_process_item(item)

    return item

  async def find_many(
    self,
    collection_name: str,
    filter: Optional[Dict] = None,
    sort: Optional[Union[Tuple, List, OrderedDict]] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    projection: Optional[Dict] = None,
    fn_process_item: Optional[Callable] = None
  ) -> List[Dict]:
    sort = self._preprocess_sort(sort)

    items = list()
    if (isinstance(limit, int) and limit > 0) or limit is None:
      kw = dict()
      if sort:
        kw['sort'] = sort
      if isinstance(skip, int):
        kw['skip'] = skip
      if isinstance(limit, int):
        kw['limit'] = limit
      if projection:
        kw['projection'] = projection
      cursor = await self.get_collection(collection_name).find(filter, **kw)
      if callable(fn_process_item):
        items = [fn_process_item(item) for item in cursor]
      else:
        items = [item for item in cursor]

    return items

  async def find_one_random(
    self,
    collection_name: str,
    filter: Optional[Dict] = None,
    projection: Optional[Dict] = None,
    fn_process_item: Optional[Callable] = None
  ) -> Optional[Dict]:
    kw = dict()
    if projection:
      kw['projection'] = projection

    cursor = await self.get_collection(collection_name).find(filter, **kw)

    item = None

    total = cursor.count()
    if total > 0:
      index = random.randint(0, max(total, 999999)) % total
      cursor.skip(index)
      item = cursor.next()

      if callable(fn_process_item) and item:
        item = fn_process_item(item)

    return item

  async def insert_one(self, collection_name: str, document: Dict):
    return await self.get_collection(collection_name).insert_one(document)

  async def insert_many(self, collection_name: str, documents: List[Dict]):
    return await self.get_collection(collection_name).insert_many(documents)

  async def delete_one(self, collection_name: str, filter: Optional[Dict]):
    return await self.get_collection(collection_name).delete_one(filter)

  async def delete_many(self, collection_name: str, filter: Optional[Dict]):
    return await self.get_collection(collection_name).delete_many(filter)

  async def update_one(self, collection_name: str, filter: Optional[Dict], update: Dict, upsert: bool = False):
    return await self.get_collection(collection_name).update_one(filter, update, upsert)

  async def update_one_and_return_it(
    self,
    collection_name: str,
    filter: Optional[Dict],
    update: Dict,
    upsert: bool = False
  ) -> Optional[Dict]:
    result = await self.update_one(collection_name, filter, update, upsert)
    if upsert and result.upserted_id:
      return await self.find_one(collection_name, {
        '_id': result.upserted_id
      })
    return await self.find_one(collection_name, filter)

  async def update_many(self, collection_name: str, filter: Optional[Dict], update: Dict, upsert: bool = False):
    return await self.get_collection(collection_name).update_many(filter, update, upsert)

  async def find_one_and_delete(
    self,
    collection_name: str,
    filter: Optional[Dict],
    projection: Optional[Dict] = None,
    sort: Optional[Union[Tuple, List, OrderedDict]] = None,
    fn_process_item: Optional[Callable] = None
  ) -> Optional[Dict]:
    sort = self._preprocess_sort(sort)

    item = self.get_collection(collection_name).find_one_and_delete(filter, projection, sort)
    if callable(fn_process_item) and item:
      item = fn_process_item(item)
    return item

  async def find_one_and_replace(
    self,
    collection_name: str,
    filter: Optional[Dict],
    replacement: Dict,
    projection: Optional[Dict] = None,
    sort: Optional[Union[Tuple, List, OrderedDict]] = None,
    upsert: bool = False, return_document: bool = False,
    fn_process_item: Optional[Callable] = None
  ) -> Optional[Dict]:
    sort = self._preprocess_sort(sort)

    item = await self.db.get_collection(collection_name).find_one_and_replace(
      filter,
      replacement,
      projection,
      sort,
      upsert,
      return_document
    )

    if callable(fn_process_item) and item:
      item = fn_process_item(item)
    return item

  async def find_one_and_update(
    self,
    collection_name: str,
    filter: Optional[Dict], update: Dict,
    projection: Optional[Dict] = None,
    sort: Optional[Union[Tuple, List, OrderedDict]] = None,
    upsert: bool = False, return_document: bool = False,
    fn_process_item: Optional[Callable] = None
  ) -> Optional[Dict]:
    sort = self._preprocess_sort(sort)

    item = await self.db.get_collection(collection_name).find_one_and_update(
      filter,
      update,
      projection,
      sort,
      upsert,
      return_document
    )

    if callable(fn_process_item) and item:
      item = fn_process_item(item)
    return item

  async def find_many_with_page_info(
    self,
    collection_name: str,
    filter=None,
    sort=None,
    skip=None,
    limit=None,
    projection=None,
    page_info=None,
    fn_process_item=None,
    fn_process_sort=None
  ) -> Tuple[List[Dict], Dict]:
    filter = dict() if filter is None else filter
    sort = self._preprocess_sort(sort)

    page_info = page_info if isinstance(page_info, dict) else dict()

    total = page_info.get('total', None)
    page_num = page_info.get('page_num', None)
    next_index = page_info.get('next_index', 0)
    cut_off_time = page_info.get('cut_off_time', self.now)

    filter = filter.copy()
    if '_id' in filter:
      filter['_id'] = {
        '$and': [
          {'$lte': ObjectId.from_datetime(cut_off_time)},
          filter['_id'],
        ]
      }
    else:
      filter['_id'] = {'$lte': ObjectId.from_datetime(cut_off_time)}

    if total is None:
      total = await self.count(collection_name, filter=filter)

    if sort and callable(fn_process_sort):
      sort_t = fn_process_sort(sort)
    else:
      sort_t = sort

    if not isinstance(skip, int):
      skip = 0

    items = await self.find_many(
      collection_name,
      filter=filter,
      sort=sort_t,
      skip=next_index + skip,
      limit=limit,
      projection=projection
    )

    page_num = page_num + 1 if isinstance(page_num, int) else 0
    from_index = next_index + skip
    next_index = next_index + skip + len(items)
    has_more = next_index < total

    page_info = dict(
      total=total,
      limit=limit,
      page_num=page_num,
      from_index=from_index,
      next_index=next_index,
      cut_off_time=cut_off_time,
      has_more=has_more,
    )

    if callable(fn_process_item) and items:
      for i in range(len(items)):
        items[i] = fn_process_item(items[i])

    return items, page_info

  async def collection_names(self, include_system_collections: bool = True) -> List[str]:
    return await self.db.collection_names(include_system_collections)

  async def create_collection(self, name: str):
    return await self.db.create_collection(name)

  async def exists_collection(self, name: str) -> bool:
    return name in (await self.collection_names(False))

  async def create_index(self, collection_name: str, index_name: str, keys: List[Dict], **kw):
    return await self.get_collection(collection_name).create_index(keys, name=index_name, **kw)

  async def delete_index(self, collection_name: str, index_name: str):
    return await self.get_collection(collection_name).drop_index(index_or_name=index_name)
