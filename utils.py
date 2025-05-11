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
SHARED_ONLY = xbmcplugin.getSetting(HANDLE, "shared_only")
ASSET_NAMETYPE = int(xbmcplugin.getSetting(HANDLE, "asset_name"))
SERVER_URL = urlparse(RAW_SERVER_URL)
API_KEY = xbmcplugin.getSetting(HANDLE, "api_key")
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
conn = http.client.HTTPSConnection(SERVER_URL.netloc) if SERVER_URL.scheme == 'https' \
    else http.client.HTTPConnection(SERVER_URL.netloc)
datelong = xbmc.getRegion('datelong')
timestamp = xbmc.getRegion('time')


# Thanks
# https://github.com/add-ons/plugin.video.vrt.nu/blob/15c545d16a26c9d601c424cc29e4ff8e0f7b25df/resources/lib/kodiutils.py#L388
def kodi_version():
    """Returns full Kodi version as string"""
    return xbmc.getInfoLabel('System.BuildVersion').split(' ')[0]


def kodi_version_major():
    """Returns major Kodi version as integer"""
    return int(kodi_version().split('.')[0])


workaround = xbmc.getCondVisibility('System.Platform.Android') and kodi_version_major() > 20


def strftime_polyfill(dt: datetime, fmt: str):
    if workaround and "%-d" in fmt:
        fmt = fmt.replace('%-d', dt.strftime('%d').lstrip('0'))
    return dt.strftime(fmt)


def get_asset_name(asset):
    if ASSET_NAMETYPE == 0:
        return strftime_polyfill(datetime.fromisoformat(asset['localDateTime'][:-6]), datelong + " " + timestamp)
    elif ASSET_NAMETYPE == 1:
        return asset['originalFileName']
    else:
        return strftime_polyfill(datetime.fromisoformat(asset['localDateTime'][:-6]), datelong + " " + timestamp)


def jsonrpc(*args, **kwargs):
    """Perform JSONRPC calls"""
    from json import dumps, loads

    # We do not accept both args and kwargs
    if args and kwargs:
        return None

    # Process a list of actions
    if args:
        for (idx, cmd) in enumerate(args):
            if cmd.get('id') is None:
                cmd.update(id=idx)
            if cmd.get('jsonrpc') is None:
                cmd.update(jsonrpc='2.0')
        return loads(xbmc.executeJSONRPC(dumps(args)))

    # Process a single action
    if kwargs.get('id') is None:
        kwargs.update(id=0)
    if kwargs.get('jsonrpc') is None:
        kwargs.update(jsonrpc='2.0')
    return loads(xbmc.executeJSONRPC(dumps(kwargs)))


def get_global_setting(key):
    """Get a Kodi setting"""
    result = jsonrpc(method='Settings.GetSettingValue', params={'setting': key})
    return result.get('result', {}).get('value')


def set_locale():
    """Load the proper locale for date strings, only once"""
    if hasattr(set_locale, 'cached'):
        return getattr(set_locale, 'cached')
    from locale import Error, LC_ALL, setlocale
    locale_lang = get_global_setting('locale.language').split('.')[-1]
    locale_lang = locale_lang[:-2] + locale_lang[-2:].upper()
    # NOTE: setlocale() only works if the platform supports the Kodi configured locale
    try:
        setlocale(LC_ALL, locale_lang)
    except (Error, ValueError) as exc:
        if locale_lang != 'en_GB':
            set_locale.cached = False
            return False
    set_locale.cached = True
    return True


def get_playback(item):
    if item['type'] == 'IMAGE':
        return f'{RAW_SERVER_URL}/api/assets/{item["id"]}/thumbnail?size=preview|x-api-key={API_KEY}'
    else:
        return f'{RAW_SERVER_URL}/api/assets/{item["id"]}/video/playback|x-api-key={API_KEY}'

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(sys.argv[0], urlencode(kwargs))


def getThumbUrl(id):
    return f'{RAW_SERVER_URL}/api/assets/{id}/thumbnail|x-api-key={API_KEY}'
