import json
import os
import sys
from datetime import datetime, timedelta

import xbmc
import xbmcgui
import xbmcplugin

from utils import conn, API_KEY, get_url, getThumbUrl, RAW_SERVER_URL, datelong

HANDLE = int(sys.argv[1])


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def time(id):
    xbmcplugin.setContent(HANDLE, 'images')

    headers = {
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    conn.request("GET", "/api/timeline/bucket?size=MONTH&timeBucket=" + id, '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))

    items = [
        (f'http://localhost:6819/api/assets/{i["id"]}/original{os.path.splitext(i["originalFileName"])[1]}|x-api-key={API_KEY}',
         xbmcgui.ListItem(datetime.fromisoformat(i['fileCreatedAt'][:-5]).strftime(datelong)), False) for i in res]
    for i in range(len(res)):
        items[i][1].setArt({'thumb': f'{RAW_SERVER_URL}/api/assets/{res[i]["id"]}/thumbnail|x-api-key={API_KEY}'})
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def timeline():
    headers = {
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    conn.request("GET", "/api/timeline/buckets?size=MONTH", '', headers)
    res = json.loads(conn.getresponse().read().decode('utf-8'))

    xbmcplugin.setContent(HANDLE, 'files')

    datelong = xbmc.getRegion('datelong')
    items = [(get_url(action='time', id=i['timeBucket']),
              xbmcgui.ListItem(datetime.fromisoformat(i['timeBucket'][:-5]).strftime(datelong)),
              True) for i
             in res]
    for i in range(len(res)):
        items[i][1].setDateTime(
            last_day_of_month(datetime.fromisoformat(res[i]['timeBucket'][:-5])).strftime('%Y-%m-%dT00:00:00Z'))
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
