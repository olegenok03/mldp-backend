"""Скачать N URL-ов двумя способами: async + threads. См. README.md."""

import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests
from aiohttp import ClientSession

N_WORKERS = 32


async def async_fetch(session: ClientSession, url: str) -> str:
    async with await session.get(url) as response:
        return await response.text()


async def async_requests(urls: list[str]) -> list[str]:
    async with ClientSession() as session:
        coros = [async_fetch(session, url) for url in urls]
        return await asyncio.gather(*coros)


def sync_fetch(session: requests.Session, url: str) -> str:
    response = session.get(url)
    return response.text


def threaded_requests(urls: list[str]) -> list[str]:
    with requests.Session() as s, ThreadPoolExecutor(max_workers=N_WORKERS) as pool:
        return list(pool.map(lambda url: sync_fetch(s, url), urls))
