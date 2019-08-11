# -*- coding: utf-8 -*-
from requests import Session, adapters
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout

HEADERS = {
    'Accept': ('text/html,application/xhtml+xml,application/xml;'
               'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed\-exchange;v=b3'),
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.'
                   '36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'),
    'Referer': 'https://wx.qq.com/',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',

}


class Request:

    def __init__(self, max_retries=3):
        self.session = Session()
        adapter = adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.keep_alive = False
        self.cookies = {}

    def threw(self, url, method='get', timeout=3):
        try:
            request = self.session.get(url, headers=HEADERS, timeout=timeout, cookies=self.cookies, allow_redirects=False) \
                if method == 'get' else self.session.post(url, headers=HEADERS, timeout=timeout, cookies=self.cookies)
        except ConnectTimeout:
            return None, 'Connect to %s timeout' % url
        except ConnectionError:
            return None, 'Connection to %s error' % url
        except ReadTimeout:
            return None, 'Read timetou from %s' % url
        except Exception as e:
            return None, '%s from %s' % (repr(e), url)
        self.cookies.update(request.cookies.get_dict())
        return request, None

    def get(self, url, timeout=3):
        return self.threw(url=url, method='get', timeout=timeout)

    def post(self, url, timeout=3):
        return self.threw(url=url, method='post', timeout=timeout)
