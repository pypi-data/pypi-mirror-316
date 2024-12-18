from typing import Self, Any
from urllib.parse import urljoin

import httpx
from dotwiz import DotWiz


type Response = List | Object | None


class Path:
    def __init__(self, client: "Client", path: str):
        self.client = client
        self.path = path

    async def __call__(self, method: str = "GET", **kwargs) -> Response:
        return await self.client._request(method, self.path, **kwargs)

    def __getitem__(self, key: Any) -> Self:
        return Path(self.client, urljoin(self.path + "/", str(key)))

    def __getattr__(self, name: str) -> Self:
        return self[name]

    async def get(self, **kwargs) -> Response:
        return await self(**kwargs)

    async def post(self, data, **kwargs) -> Response:
        return await self.client._request("POST", self.path, json=data, **kwargs)


class List(list):
    def __init__(self, items: list):
        self.extend(items)


class Object(DotWiz):
    def __init__(self, data: dict):
        self.update(data)


class Client:

    def __init__(self, base_url):
        self.base_url = base_url

    async def _request(self, method, path, **kwargs) -> Response:
        url = urljoin(self.base_url, path)

        async with httpx.AsyncClient() as client:
            resp = await client.request(method, url, params=kwargs)
            return await self._new_response(resp)

    async def _new_response(self, resp: httpx.Response) -> Response:
        data = resp.json()
        match resp.status_code:
            case 200:
                data = self._parse(data)
                return data
            case 204:
                return None
            case 400:
                raise ValueError(data)
            case 404:
                raise ValueError(data)
            case _:
                raise ValueError(resp.status_code)

    def _parse(self, data: Any) -> Response:
        if isinstance(data, list):
            return List([self._parse(i) for i in data])
        elif isinstance(data, dict):
            return Object({k: self._parse(v) for k, v in data.items()})
        else:
            return data

    def __getitem__(self, key: Any) -> Path:
        return Path(self, key)

    def __getattr__(self, name: str) -> Path:
        return self[name]
