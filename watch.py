"""
Watch torrent files in folder and auto add to download list
"""
import os
import requests


PASSWORD = os.environ.get('WEBAPI_PASSWORD', 'deluge')


class TorrentApi:
    def __init__(self, host='localhost', port=8112):
        self.session = requests.Session()
        self.url = f'http://{host}:{port}/json'
        self.__request_id = 0

    @property
    def REQUEST_ID(self):
        self.__request_id += 1
        return self.__request_id

    def request(self, method: str, data: list = None):
        try:
            response = self.session.post(self.url, json={'id': self.REQUEST_ID, 'method': method, 'params': data or []})
        except requests.exceptions.ConnectionError:
            raise Exception('WebUI seems to be unavailable. '
                            'Run deluge-web or enable WebUI plugin using other thin client.')
        data = response.json()
        error = data.get('error')
        if error:
            msg = error['message']
            if msg == 'Unknown method':
                msg += '. Check WebAPI is enabled.'
            raise Exception('API response: %s' % msg)
        return data['result']

    def login(self, password: str):
        self.request('auth.login', [password])

    def api_version(self):
        return self.request('webapi.get_api_version')

    def get_torrents(self):
        return self.request('webapi.get_torrents')

    def add_torrent(self, file: str, download_location=None):
        pass

    def remove_torrent(self, torrent_id, remove_data=False):
        ...

#
# t = TorrentApi('192.168.0.173')
# t.login('deluge')
# t.api_version()
# t.request('webapi.get_torrents')


print('Watch not implemented. Use fake app.')
os.system('sleep infinity')
