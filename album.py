import json
import os
import sys
from datetime import datetime

import xbmcgui
import xbmcplugin

from utils import API_KEY, getThumbUrl, get_url, conn, RAW_SERVER_URL, datelong

HANDLE = int(sys.argv[1])


def list_albums():
    headers = {
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    conn.request("GET", "/api/albums", '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))

    items = [(get_url(action='album', id=i['id']), xbmcgui.ListItem(i['albumName']), True) for i in res]
    for i in range(len(res)):
        if res[i]['albumThumbnailAssetId'] is not None:
            items[i][1].setArt({
                'thumb': getThumbUrl(res[i]['albumThumbnailAssetId'])
            })
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def album(id):
    xbmcplugin.setContent(HANDLE, 'images')

    headers = {
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    conn.request("GET", f"/api/albums/{id}", '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))['assets']

    items = [
        (
        f'http://localhost:6819/api/assets/{i["id"]}/original{os.path.splitext(i["originalFileName"])[1]}|x-api-key={API_KEY}',
        xbmcgui.ListItem(datetime.fromisoformat(i['fileCreatedAt'][:-5]).strftime(datelong)), False) for i in res]
    for i in range(len(res)):
        items[i][1].setArt({'thumb': f'{RAW_SERVER_URL}/api/assets/{res[i]["id"]}/thumbnail|x-api-key={API_KEY}'})
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
