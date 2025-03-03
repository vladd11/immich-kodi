import json
import os
import sys
from datetime import datetime

import xbmc
import xbmcgui
import xbmcplugin

from utils import API_KEY, getThumbUrl, get_url, conn, RAW_SERVER_URL, datelong, timestamp, SHARED_ONLY, \
    strftime_polyfill, get_asset_name

HANDLE = int(sys.argv[1])


def list_albums():
    headers = {
        'Accept': 'application/json',
        'User-agent': xbmc.getUserAgent(),
        'x-api-key': API_KEY
    }
    conn.request("GET", f"/api/albums?shared={SHARED_ONLY or 'false'}", '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))

    items = [(get_url(action='album', id=i['id']), xbmcgui.ListItem(i['albumName']), True) for i in res]
    for i in range(len(res)):
        if 'startDate' in res[i]:
            items[i][1].setDateTime(
                datetime.fromisoformat(res[i]['startDate'][:-5]).strftime('%Y-%m-%dT%H:%M:%SZ'))
        if 'albumThumbnailAssetId' in res[i]:
            items[i][1].setArt({'thumb': getThumbUrl(res[i]['albumThumbnailAssetId'])})
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def album(id):
    xbmcplugin.setContent(HANDLE, 'images')

    headers = {
        'Accept': 'application/json',
        'User-agent': xbmc.getUserAgent(),
        'x-api-key': API_KEY
    }
    conn.request("GET", f"/api/albums/{id}", '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))['assets']

    for i in res:
        if not ('dateTimeOriginal' in i['exifInfo']):
            i['exifInfo']['dateTimeOriginal'] = (
                datetime.fromisoformat(i['fileModifiedAt'].replace('Z', '+00:00')).strftime('%Y-%m-%dT%H:%M:%S%z'))

    items = [
        (
            f'{RAW_SERVER_URL}/api/assets/{i["id"]}/original|x-api-key={API_KEY}',
            xbmcgui.ListItem(get_asset_name(i)), False)
        for i in res]
    for i in range(len(res)):
        items[i][1].setArt({'thumb': getThumbUrl(res[i]["id"])})
        items[i][1].setProperty('MimeType', res[i]["originalMimeType"])
        items[i][1].setDateTime(res[i]['exifInfo']['dateTimeOriginal'].replace('Z', '+00:00'))
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
