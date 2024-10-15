import requests,os

TORRENT_CLIENT = os.environ["TORRENT_CLIENT_URL"]
COOKIE = os.environ["COOKIE"]

def handle_magnet(magnet: str) -> str:

    api_url = TORRENT_CLIENT+"torrents/add"
    cookies = {"SID": COOKIE}
    data = {"urls": magnet}
    
    response = requests.post(api_url, cookies=cookies,data=data)

    print(f'LOG: {response.text}')

    if response.status_code == 200:
        return "Agregado Correctamente"
    else: return "Error al Agregar"