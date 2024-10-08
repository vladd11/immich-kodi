import http.client
import sys
from datetime import datetime
from urllib.parse import urlencode, urlparse

import xbmc
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath

HANDLE = int(sys.argv[1])

RAW_SERVER_URL = xbmcplugin.getSetting(HANDLE, "immich_url")
SERVER_URL = urlparse(RAW_SERVER_URL)
API_KEY = xbmcplugin.getSetting(HANDLE, "api_key")
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
conn = http.client.HTTPSConnection(SERVER_URL.netloc) if SERVER_URL.scheme == 'https' \
    else http.client.HTTPConnection(SERVER_URL.netloc)
datelong = xbmc.getRegion('datelong')


months = ["Январь", "Февраль",
          "Март", "Апрель", "Май",
          "Июнь", "Июль", "Август",
          "Сентябрь", "Октябрь", "Ноябрь",
          "Декабрь"]


def toReadableDate(date: str):
    dt = datetime.fromisoformat(date)
    return f'{months[dt.month]} {dt.year}'


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(sys.argv[0], urlencode(kwargs))


def getThumbUrl(id):
    return f'{SERVER_URL}/api/asset/thumbnail/{id}?format=WEBP|x-api-key={API_KEY}'
