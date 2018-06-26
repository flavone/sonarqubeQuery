import requests


class HttpUtil:
    session = None

    def __init__(self, url, username, password):
        session = requests.session()
        resp = session.request(method='POST', url=url, params={'login': username, 'password': password})
        if resp.status_code != 200:
            self.session = None
        else:
            self.session = session

    def get_json(self, url, para=None):
        if self.session is None:
            return None
        resp = self.session.request(method='GET', url=url, params=para)
        if resp.status_code != 200:
            return None
        return resp.json()
