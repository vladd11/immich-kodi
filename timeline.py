import json
import sys
from datetime import datetime, timedelta

import xbmc
import xbmcgui
import xbmcplugin

from models import ItemAsset, TimeBucket, TimelineBucket
from utils import (
    API_KEY,
    conn,
    datelong,
    get_asset_name,
    get_playback,
    get_url,
    getThumbUrl,
    strftime_polyfill,
)

HANDLE = int(sys.argv[1])


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def get_asset_info(id):
    headers = {
        "Accept": "application/json",
        "User-agent": xbmc.getUserAgent(),
        "x-api-key": API_KEY,
    }
    conn.request("GET", "/api/assets/" + id, "", headers)
    return json.loads(conn.getresponse().read().decode("utf-8"))


def time(id, video):
    xbmcplugin.setContent(HANDLE, "images")

    headers = {
        "Accept": "application/json",
        "User-agent": xbmc.getUserAgent(),
        "x-api-key": API_KEY,
    }
    conn.request(
        "GET",
        "/api/timeline/bucket?size=MONTH&timeBucket=" + id,
        "",
        headers,
    )
    res = json.loads(conn.getresponse().read().decode("utf-8"))
    res = TimeBucket(**res)

    items = []

    for id in res.id:
        item = get_asset_info(id)
        item = ItemAsset(**item)
        if video and item.type == "IMAGE":
            continue
        if not item.exifInfo.dateTimeOriginal:
            item.exifInfo.dateTimeOriginal = datetime.fromisoformat(
                item.fileModifiedAt
            ).strftime("%Y-%m-%dT%H:%M:%S%z")

        items.append(
            (
                get_playback(item.id, item.type),
                xbmcgui.ListItem(get_asset_name(item)),
                False,
            )
        )
        items[-1][1].setArt({"thumb": getThumbUrl(item.id)})
        items[-1][1].setProperty("MimeType", item.originalMimeType)
        items[-1][1].setDateTime(item.exifInfo.dateTimeOriginal.replace("Z", "+00:00"))
        # itemsR.append(i)

    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def timeline(video):
    video = "1" if video else ""

    headers = {
        "Accept": "application/json",
        "User-agent": xbmc.getUserAgent(),
        "x-api-key": API_KEY,
    }
    conn.request("GET", "/api/timeline/buckets?size=MONTH", "", headers)
    res = json.loads(conn.getresponse().read().decode("utf-8"))
    res = [TimelineBucket(**i) for i in res]

    xbmcplugin.setContent(HANDLE, "files")

    items = [
        (
            get_url(action="time", id=i.timeBucket, video=video),
            xbmcgui.ListItem(
                strftime_polyfill(datetime.fromisoformat(i.timeBucket), datelong)
            ),
            True,
        )
        for i in res
    ]
    for item, timeline in zip(items, res):
        item[1].setDateTime(
            last_day_of_month(datetime.fromisoformat(timeline.timeBucket)).strftime(
                "%Y-%m-%dT00:00:00Z"
            )
        )

    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
