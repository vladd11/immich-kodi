import json
import sys
from datetime import datetime

import xbmc
import xbmcgui
import xbmcplugin

from models import Album, ItemAsset
from utils import (
    API_KEY,
    RAW_SERVER_URL,
    SHARED_ONLY,
    conn,
    get_asset_name,
    get_url,
    getThumbUrl,
)

HANDLE = int(sys.argv[1])


def list_albums():
    headers = {
        "Accept": "application/json",
        "User-agent": xbmc.getUserAgent(),
        "x-api-key": API_KEY,
    }
    conn.request("GET", f"/api/albums?shared={SHARED_ONLY or 'false'}", "", headers)
    res = json.loads(conn.getresponse().read().decode("utf-8"))
    res = [Album(**i) for i in res]

    items = [
        (get_url(action="album", id=album.id), xbmcgui.ListItem(album.albumName), True)
        for album in res
    ]
    for item, album in zip(items, res):
        if album.startDate:
            item[1].setDateTime(
                datetime.fromisoformat(album.startDate).strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        if album.albumThumbnailAssetId:
            item[1].setArt({"thumb": getThumbUrl(album.albumThumbnailAssetId)})
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def album(id):
    xbmcplugin.setContent(HANDLE, "images")

    headers = {
        "Accept": "application/json",
        "User-agent": xbmc.getUserAgent(),
        "x-api-key": API_KEY,
    }
    conn.request("GET", f"/api/albums/{id}", "", headers)
    res = json.loads(conn.getresponse().read().decode("utf-8"))["assets"]
    res = [ItemAsset(**i) for i in res]

    for i in res:
        if not i.exifInfo.dateTimeOriginal:
            i.exifInfo.dateTimeOriginal = datetime.fromisoformat(
                i.fileModifiedAt
            ).strftime("%Y-%m-%dT%H:%M:%S%z")

    items = [
        (
            f"{RAW_SERVER_URL}/api/assets/{album.id}/original|x-api-key={API_KEY}",
            xbmcgui.ListItem(get_asset_name(i)),
            False,
        )
        for album in res
    ]
    for item, album in zip(items, res):
        item[1].setArt({"thumb": getThumbUrl(album.id)})
        item[1].setProperty("MimeType", album.originalMimeType)
        item[1].setDateTime(album.exifInfo.dateTimeOriginal)
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
