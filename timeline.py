import json
import sys
from datetime import datetime, timedelta

import xbmc
import xbmcgui
import xbmcplugin

from utils import conn, API_KEY, get_url, getThumbUrl, datelong, timestamp, get_playback, \
    strftime_polyfill

HANDLE = int(sys.argv[1])


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def time(id, video):
    xbmcplugin.setContent(HANDLE, 'images')

    headers = {
        'Accept': 'application/json',
        'User-agent': xbmc.getUserAgent(),
        'x-api-key': API_KEY,
    }
    conn.request("GET", "/api/timeline/bucket?size=MONTH&timeBucket=" + id, '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))

    items = []
    itemsR = []
    for i in res:
        if video and i['type'] == 'IMAGE':
            continue
        items.append((get_playback(i),
                      xbmcgui.ListItem(
                          strftime_polyfill(datetime.fromisoformat(i['localDateTime'][:-5]),
                                            datelong + " " + timestamp)), False))
        itemsR.append(i)
    for i in range(len(items)):
        items[i][1].setArt({'thumb': getThumbUrl(itemsR[i]["id"])})
        items[i][1].setProperty('MimeType', itemsR[i]["originalMimeType"])
        items[i][1].setDateTime(
            strftime_polyfill(datetime.fromisoformat(itemsR[i]['localDateTime'][:-5]), '%Y-%m-%dT00:00:00Z'))
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def timeline(video):
    video = '1' if video else ''

    headers = {
        'Accept': 'application/json',
        'User-agent': xbmc.getUserAgent(),
        'x-api-key': API_KEY
    }
    conn.request("GET", "/api/timeline/buckets?size=MONTH", '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))

    xbmcplugin.setContent(HANDLE, 'files')

    items = [(get_url(action='time', id=i['timeBucket'], video=video),
              xbmcgui.ListItem(strftime_polyfill(datetime.fromisoformat(i['timeBucket'][:-5]), datelong)), True)
             for i in res]
    for i in range(len(res)):
        items[i][1].setDateTime(
            last_day_of_month(datetime.fromisoformat(res[i]['timeBucket'][:-5])).strftime('%Y-%m-%dT00:00:00Z'))

    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
