from cgitb import text
from urllib import response
import os
import aiohttp
from asyncio import sleep

TORRENT_CLIENT = os.environ["TORRENT_CLIENT_URL"]
COOKIE = os.environ["COOKIE"]


async def send_magnet(magnet: str) -> bool:

    api_url = TORRENT_CLIENT + "torrents/add"
    cookies = {"SID": COOKIE}
    data = {"urls": magnet}

    async with aiohttp.ClientSession() as session:
        async with session.post(url=api_url, cookies=cookies, data=data) as response:
            if not (response.ok):
                print(f"send_magnet: {response.status}")
                return False
            else:
                return True
    # try:
    #     response = requests.post(api_url, cookies=cookies, data=data)
    # except:
    #     print(f"send_magnet: {response.status_code}")
    #     return False

    # print(f"send_magnet: {response.status_code}")

    # if response.status_code == 200:
    #     return True
    # else:
    #     return False


async def request_info():

    api_url = TORRENT_CLIENT + "torrents/info"
    cookies = {"SID": COOKIE}

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, cookies=cookies) as response:
            if not (response.ok):
                await sleep(10)
                print(f"request_info: {response.status}")
                return
            print(f"request_info: {response.status}")

            return await response.json()

    # try:
    #     response = requests.get(url=api_url, cookies=cookies)
    # except:
    #     print(f"request_info: {response.status_code}")
    #     return

    # print(f"request_info: {response.status_code}")
    # return response.json()


async def request_torrent_info(hash: str):
    api_url = TORRENT_CLIENT + f"torrents/files?hash={hash}"
    cookies = {"SID": COOKIE}

    async with aiohttp.ClientSession() as session:
        async with session.get(url=api_url, cookies=cookies) as response:
            if not (response.ok):
                print(f"request_torrent_info: {response.status}")
                return "404"
            else:
                print(f"request_torrent_info: {response.status}")
                return await response.json()

    # try:
    #     response = requests.get(url=api_url, cookies=cookies)
    # except:
    #     print(f"request_torrent_info: {response.status_code}")

    # if response.status_code == 404:
    #     return "404"

    # print(f"request_torrent_info: {response.status_code}")
    # return response.json


async def delete_magnet(hash: str) -> bool:

    api_url = TORRENT_CLIENT + "torrents/delete"
    cookies = {"SID": COOKIE}
    data = {"hashes": hash, "deleteFiles": "false"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=api_url, cookies=cookies, data=data) as response:
            if not (response.ok):
                print(f"delete_magnet: {response.status}")
                return False
            else:
                return True
            