import json
from datetime import datetime
from time import strftime

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from utils import conn, API_KEY, HANDLE, get_url, RAW_SERVER_URL, datelong, timestamp, strftime_polyfill

addon = xbmcaddon.Addon()


def slideshow():
    a = xbmcgui.Dialog().input(heading=addon.getLocalizedString(30012), type=xbmcgui.INPUT_DATE)
    b = xbmcgui.Dialog().input(heading=addon.getLocalizedString(30013), type=xbmcgui.INPUT_DATE)
    if not a or not b:
        xbmcplugin.endOfDirectory(HANDLE)
        return

    a = datetime.strptime(a.replace(' ', '0'), "%d/%m/%Y")
    b = datetime.strptime(b.replace(' ', '0'), "%d/%m/%Y")
    if a > b:
        a, b = b, a

    headers = {
        'Accept': 'application/json',
        'User-agent': xbmc.getUserAgent(),
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }
    conn.request('POST', '/api/search/metadata', body=json.dumps({
        'takenBefore': b.strftime("%Y-%m-%dT23:59:59.000Z"),
        'takenAfter': a.strftime("%Y-%m-%dT00:00:00.000Z"),
        'page': 1,
        'withExif': True
    }), headers=headers)
    resp = json.loads(conn.getresponse().read().decode('utf-8'))

    playlist = xbmc.PlayList(1)
    for i in resp:
        playlist.add(f'{RAW_SERVER_URL}/api/assets/{i["id"]}/video/playback|x-api-key={API_KEY}',
                     xbmcgui.ListItem(
                         strftime_polyfill(datetime.fromisoformat(i['localDateTime'][:-5]),
                                           datelong + " " + timestamp)), False)
