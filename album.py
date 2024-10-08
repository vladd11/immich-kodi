import http.client
import json
import random
import sys

import requests
import xbmcgui
import xbmcplugin

from utils import API_KEY, getThumbUrl, get_url, conn

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


def album():
    requests.get(f'/api/album')
    headers = {
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    conn.request("GET", "/api/albums", '', headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
