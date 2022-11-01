# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import TextIOWrapper
import json
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union

import aiohttp

import requests

from .errors import (BadRequest, Forbidden, HTTPException, InternalServerError,
                     NotFound, PayloadTooLarge, QuotaExceeded,
                     ServiceUnavailable, TooManyRequests, URITooLong)

__all__ = ['Adapter', 'RequestsAdapter', 'AiohttpAdapter']


class Adapter(metaclass=ABCMeta):
  def __init__(self, id: int) -> None:
    self.base_url = 'https://api.iachara.com/api/char/{id}?id={id}'
    self.id = id

  @abstractmethod
  def request(self, id: int) -> Optional[dict]:
    raise NotImplementedError()

  @abstractmethod
  def get_usage(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_data(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_result_id(self) -> int:
    raise NotImplementedError()

  @abstractmethod
  def get_result_name(self) -> str:
    raise NotImplementedError()

  @abstractmethod
  def get_result_tags(self) -> str:
    raise NotImplementedError()

  @abstractmethod
  def get_result_data(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_parsonal_data(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_ability_value(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_san(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_skill(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_battle_skill(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_search_skill(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_action_skill(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_negotiation_skill(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_knowledge_skill(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_battle(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_money(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_memo(self) -> str:
    raise NotImplementedError()

  @abstractmethod
  def get_backstory(self) -> dict:
    raise NotImplementedError()

  @abstractmethod
  def get_icon_url(self) -> str:
    raise NotImplementedError()







  def _check_status(self, status_code, response, data) -> Union[dict, list]:
    if 200 <= status_code < 300:
      return data
    message = data.get('message', '') if data else ''
    if status_code == 400:
      raise BadRequest(response, message)
    elif status_code == 403:
      raise Forbidden(response, message)
    elif status_code == 404:
      raise NotFound(response, message)
    elif status_code == 413:
      raise PayloadTooLarge(response, message)
    elif status_code == 414:
      raise URITooLong(response, message)
    elif status_code == 429:
      raise TooManyRequests(response, message)
    elif status_code == 456:
      raise QuotaExceeded(response, message)
    elif status_code == 503:
      raise ServiceUnavailable(response, message)
    elif 500 <= status_code < 600:
      raise InternalServerError(response, message)
    else:
      raise HTTPException(response, message)



class RequestsAdapter(Adapter):
  def request(self, id: int) -> Optional[dict]:

    url = self.base_url.format(id=id)
    resp = requests.get(url)
    try:
      data = resp.json()
    except json.JSONDecodeError:
      data = resp.content
    return self._check_status(resp.status_code, resp, data)

  def get_data(self)-> dict:
    data = self.request(self.id)
    return data

  def get_result_status(self) -> bool:
    data = self.request(self.id)
    return data['success']

  def get_result_id(self) -> int:
    data = self.request(self.id)
    return data['result']['id']

  def get_result_name(self) -> str:
    data = self.request(self.id)
    return data['result']['name']

  def get_result_tags(self) -> str:
    data = self.request(self.id)
    return data['result']['tags']

  def get_result_data(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])

  def get_parsonal_data(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['parsonal_data']

  def get_ability_value(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['ability_value']

  def get_san(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['san']

  def get_skill(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['skill']

  def get_battle_skill(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['battle_skill']

  def get_search_skill(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['search_skill']

  def get_action_skill(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['action_skill']

  def get_negotiation_skill(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['negotiation_skill']

  def get_knowledge_skill(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['knowledge_skill']

  def get_battle(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['battle']

  def get_money(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['money']

  def get_memo(self) -> str:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['memo']

  def get_backstory(self) -> dict:
    data = self.request(self.id)
    return json.loads(data['result']['data'])['backstory']


  def get_icon_url(self) -> str:
    data = self.request(self.id)
    return data['result']['icon']

  def get_usage(self) -> dict:
    data = self.request(self.id)
    return data


class AiohttpAdapter(Adapter):

  async def request(self, id: int) -> Optional[dict]:
    url = self.base_url.format(id=id)
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        try:
          data = await resp.json(content_type=None)
        except json.JSONDecodeError:
          data = await resp.read()
        status_code = resp.status
      return self._check_status(status_code, resp, data)


  async def get_data(self)-> dict:
    data = await self.request(self.id)
    return data


  async def get_result_status(self) -> str:
    data = await self.request(self.id)
    return data['success']


  async def get_result_id(self) -> int:
    data = await self.request(self.id)
    return data['result']['id']

  async def get_result_name(self) -> str:
    data = await self.request(self.id)
    return data['result']['name']

  async def get_result_tags(self) -> str:
    data = await self.request(self.id)
    return data['result']['tags']

  async def get_result_data(self) -> dict:
    data = await self.request(self.id)
    return json.loads(data['result']['data'])

  async def get_parsonal_data(self) -> dict:
    data = await self.request(self.id)
    return json.loads(data['result']['data'])['parsonal_data']

  async def get_ability_value(self) -> dict:
    data = await self.request(self.id)
    return json.loads(data['result']['data'])['ability_value']


  async def get_san(self) -> dict:
    data =  await  self.request(self.id)
    return json.loads(data['result']['data'])['san']

  async def get_skill(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['skill']

  async def get_battle_skill(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['battle_skill']

  async def get_search_skill(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['search_skill']

  async def get_action_skill(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['action_skill']

  async def get_negotiation_skill(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['negotiation_skill']

  async def get_knowledge_skill(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['knowledge_skill']

  async def get_battle(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['battle']

  async def get_money(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['money']

  async def get_memo(self) -> str:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['memo']

  async def get_backstory(self) -> dict:
    data = await  self.request(self.id)
    return json.loads(data['result']['data'])['backstory']

  async def get_icon_url(self) -> str:
    data = await self.request(self.id)
    return data['result']['icon']

  async def get_usage(self) -> dict:
    data = await self.request(self.id)
    return data


def main():
  transfer = RequestsAdapter(2975824)
  print(transfer.get_result_data())

async def aiomain():
  transfer = AiohttpAdapter(2975824)
  print(await transfer.get_backstory())


if __name__ == "__main__":
  import asyncio
  main()
  loop = asyncio.get_event_loop()
  loop.run_until_complete(aiomain())
