import sys
from urllib.parse import parse_qsl

import sys
from urllib.parse import parse_qsl

import xbmcgui
import xbmcplugin

from album import list_albums, album
from timeline import timeline, time
from utils import get_url

DEBUG = False
if DEBUG:
    pass

URL = sys.argv[0]
HANDLE = int(sys.argv[1])
if __name__ == '__main__':
    params = dict(parse_qsl(sys.argv[2][1:]))

    if not params.get('action'):
        xbmcplugin.addDirectoryItem(HANDLE, get_url(action='timeline'),
                                    xbmcgui.ListItem("Timeline"), True)
        xbmcplugin.addDirectoryItem(HANDLE, get_url(action='albums'),
                                    xbmcgui.ListItem("Albums"), True)

        xbmcplugin.endOfDirectory(HANDLE)
    elif params['action'] == 'timeline':
        timeline()
    elif params['action'] == 'albums':
        list_albums()
    elif params['action'] == 'album':
        album(params['id'])
    elif params['action'] == 'time':
        time(params['id'])

if DEBUG:
    import pydevd
    pydevd.stoptrace()
