import re
from typing import *

import os
import copy
from xml.dom import minidom


class FaXml(object):
  def __init__(self, xml: Optional[Union[minidom.Document, str]] = None):
    if not isinstance(xml, (minidom.Document, str)):
      self._doc = minidom.Document()
    elif isinstance(xml, minidom.Document):
      self._doc = copy.deepcopy(xml)
    elif xml[-4:].lower() == '.xml':
      assert os.path.isfile(xml)
      self._doc = minidom.parse(xml)
    elif xml.lstrip().startswith('<') and xml.rstrip().endswith('>'):
      self._doc = minidom.parseString(xml)
    else:
      self._doc = minidom.Document()
      self._doc.appendChild(self._doc.createElement(xml))
    assert isinstance(self._doc, minidom.Document)

  @property
  def document(self) -> minidom.Document:
    return self._doc

  @property
  def root(self) -> minidom.Element:
    return self._doc.documentElement

  def create_element(
    self,
    el: Union[str, minidom.Element],
    v: Union[minidom.Element, List, Dict, int, float, bool, str]
  ) -> minidom.Element:
    if isinstance(el, str):
      el = self._doc.createElement(el)

    if isinstance(v, minidom.Element):
      el.appendChild(v)
    elif isinstance(v, list):
      for vv in v:
        self.create_element(el, vv)
    elif isinstance(v, dict):
      for kk, vv in v.items():
        assert isinstance(kk, str)
        if kk in ('#TEXT', '#text', ''):
          el.appendChild(self._doc.createTextNode(str(vv)))
        elif kk.startswith('@'):
          el.setAttribute(kk[1:], str(vv))
        else:
          el.appendChild(self.create_element(kk, vv))
    else:
      el.appendChild(self._doc.createTextNode(str(v)))

    return el

  def get_element_text(
    self,
    el: Optional[Union[minidom.Document, minidom.Element, minidom.Text]],
    default: Optional[str] = ''
  ) -> str:
    if isinstance(el, minidom.Text):
      s = str(el.data)
    elif isinstance(el, minidom.Document):
      s = self.get_element_text(el.documentElement)
    elif isinstance(el, (minidom.Element, minidom.Node)):
      s = ''
      for child in el.childNodes:
        s += self.get_element_text(child)
    else:
      s = default

    return s

  def get_elements(
    self,
    el: minidom.Element,
    name: Optional[Union[str, re.Pattern]] = None,
    attrs: Optional[Dict[str, Union[bool, str]]] = None,
    text: Optional[Union[str, re.Pattern]] = None,
    level: Optional[int] = 1,
    limit: Optional[int] = -1
  ):
    def match(v: str, p: Optional[Union[str, re.Pattern]] = None) -> bool:
      if isinstance(p, re.Pattern):
        is_matched = bool(p.match(v))
      elif isinstance(p, str):
        is_matched = ((p == v) or re.match(p, v))
      else:
        is_matched = True
      return is_matched

    items = list()

    for child in el.childNodes:  # type: minidom.Element
      if not match(child.nodeName, name):
        continue

      if isinstance(attrs, dict):
        is_ok = True

        for kk, vv in attrs.values():
          if isinstance(vv, bool):
            if el.hasAttribute(kk) != vv:
              is_ok = False
              break
          elif isinstance(vv, str):
            if not match(el.getAttribute(kk), vv):
              is_ok = False
              break

        if not is_ok:
          continue

      if not match(self.get_element_text(el), text):
        continue

      items.append(child)

      if isinstance(limit, int) and limit > 0:
        limit -= 1

      if limit == 0:
        break

      if isinstance(level, int) and level > 0:
        level -= 1

      if level != 0:
        items_t = self.get_elements(child, name, attrs, text, level, limit)

        if isinstance(limit, int) and limit > 0:
          if limit >= len(items_t):
            limit -= len(items_t)
          elif 0 < limit < len(items_t):
            items_t = items_t[:limit]
            limit = 0

        items += items_t

        if limit == 0:
          break

    return items

  def get_element(
    self,
    el: minidom.Element,
    name: Optional[Union[str, re.Pattern]] = None,
    attrs: Optional[Dict[str, Union[bool, str]]] = None,
    text: Optional[Union[str, re.Pattern]] = None,
    level: Optional[int] = 1,
    default: Optional[minidom.Element] = None
  ):
    items = self.get_elements(el, name, attrs, text, level, 1)
    ret = items[0] if len(items) else default
    return ret

  def pretty(self):
    el_blank_list = list()

    el_list = list()
    el_list.append(self._doc.documentElement)

    i, j = 0, 1
    while i < j:
      el = el_list.pop(0)
      i += 1

      for child in el.childNodes:
        if isinstance(child, minidom.Text):
          if not str(child.data).strip():
            el_blank_list.append((el, child))
        elif isinstance(child, minidom.Element):
          el_list.append(child)
          j += 1

    for el, child in el_blank_list:
      el.removeChild(child)

  def __str__(self):
    assert isinstance(self._doc, minidom.Document)
    return self._doc.toprettyxml()
