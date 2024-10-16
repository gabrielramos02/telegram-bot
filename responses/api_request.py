import requests, os

TORRENT_CLIENT = os.environ["TORRENT_CLIENT_URL"]
COOKIE = os.environ["COOKIE"]


def send_magnet(magnet: str) -> bool:

    api_url = TORRENT_CLIENT + "torrents/add"
    cookies = {"SID": COOKIE}
    data = {"urls": magnet}
    try:
        response = requests.post(api_url, cookies=cookies, data=data)
    except:
        print(f"send_magnet: {response.status_code}")
        return False
    
    print(f"send_magnet: {response.status_code}")
    
    if response.status_code == 200:
        return True
    else:
        return False


def request_info():

    api_url = TORRENT_CLIENT + "torrents/info"
    cookies = {"SID": COOKIE}

    try:
        response = requests.get(url=api_url, cookies=cookies)
    except:
        print(f"request_info: {response.status_code}")
        return
    
    print(f"request_info: {response.status_code}")
    return response.json()


def request_torrent_info(hash: str):
    api_url = TORRENT_CLIENT + f"torrents/files?hash={hash}"
    cookies = {"SID": COOKIE}
    try:
        response = requests.get(url=api_url, cookies=cookies)
    except:
        print(f"request_torrent_info: {response.status_code}")
    
    if response.status_code == 404:
        return "404"
    
    print(f"request_torrent_info: {response.status_code}")
    return response.json()
