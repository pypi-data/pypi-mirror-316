from types import TracebackType
from typing import Any

import requests
from aiohttp import ClientSession
from requests import Session


class HttpMethod:
    GET: str = 'GET'
    POST: str = 'POST'
    OPTIONS: str = 'OPTIONS'
    PUT: str = 'PUT'
    DELETE: str = 'DELETE'


class Requester:
    def __init__(self, timeout: int = 30):
        self.__session: Session | None = None
        self.__timeout: int = timeout

    def __enter__(self):
        self.__session = requests.session()
        return self

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: TracebackType | None):
        if (self.__session):
            self.__session.close()

    def request(self,
                method: str,
                url: str,
                params: dict | None = None,
                data: dict | None = None,
                json: dict | None = None,
                headers: dict | None = None,
                **kwargs) -> requests.Response | None:
        if not self.__session:
            return None
        return self.__session.request(method,
                                      url,
                                      params=params,
                                      data=data,
                                      json=json,
                                      headers=headers,
                                      timeout=self.__timeout,
                                      **kwargs)

    def get(self,
            url: str,
            params: dict | None = None,
            data: dict | None = None,
            json: dict | None = None,
            headers: dict | None = None,
            **kwargs) -> requests.Response | None:
        return self.request(HttpMethod.GET,
                            url,
                            params=params,
                            data=data,
                            json=json,
                            headers=headers,
                            **kwargs)

    def post(self,
             url: str,
             params: dict | None = None,
             data: dict | None = None,
             json: dict | None = None,
             headers: dict | None = None,
             **kwargs) -> requests.Response | None:
        return self.request(HttpMethod.POST,
                            url,
                            params=params,
                            data=data,
                            json=json,
                            headers=headers,
                            **kwargs)


class RequesterAsync:
    def __init__(self, session: ClientSession, proxy: str | None = None):
        self.__session: ClientSession = session
        self.__proxy: str | None = proxy

    async def get(self,
                  url: str,
                  params: dict | None = None,
                  data: dict | None = None,
                  json: dict | None = None,
                  headers: dict | None = None,
                  **kwargs) -> tuple[Any, int]:
        if not self.__session:
            return None, -1
        async with self.__session.get(url,
                                      params=params,
                                      data=data,
                                      json=json,
                                      headers=headers,
                                      proxy=self.__proxy,
                                      **kwargs) as response:
            return await response.json(), response.status

    async def post(self,
                   url: str,
                   params: dict | None = None,
                   data: dict | None = None,
                   json: dict | None = None,
                   headers: dict | None = None,
                   **kwargs) -> tuple[Any, int]:
        if not self.__session:
            return None, -1
        async with self.__session.post(url,
                                       params=params,
                                       data=data,
                                       json=json,
                                       headers=headers,
                                       proxy=self.__proxy,
                                       **kwargs) as response:
            return await response.json(), response.status
