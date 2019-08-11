# -*- coding: utf-8 -*-

import re
import time
from request import Request


class Wechat:

    def __init__(self):
        self.request = Request()
        self.index = r'https://wx.qq.com/'

        self.appid = None
        self.uuid = None

    def login(self):
        response, err = self.request.get(self.index)
        if err is not None:
            print(err)
            return False

        pattern = re.compile(r'src="(.*?\.js)"')
        allJs = pattern.findall(response.text)
        if len(allJs) <= 0:
            print('Did not load js')
            return False

        for js in allJs[::-1]:
            url = js.replace('//', 'https://')
            response, err = self.request.get(url)
            if err is not None:
                print(err)
                continue

            text = response.text
            pattern = re.compile(r'appid=(.*?)&redirect_uri')
            appid = pattern.findall(text)
            if len(appid) <= 0:
                print('Could not find appid:[%s]' % url)
                continue
            else:
                self.appid = appid[0]
                break

        redirect_uri = r'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage'
        url = 'https://login.wx.qq.com/jslogin?appid={}&redirect_uri={}&fun=new&lang=zh_CN&_={}'
        url = url.format(self.appid, redirect_uri, int(time.time() * 1000))
        response, err = self.request.get(url=url)
        if err is not None:
            print(err)
            return False

        text = response.text.replace(' ', '')
        pattern = re.compile(r'window.QRLogin.uuid="(.*)?"')
        uuid = pattern.findall(text)
        if len(uuid) <= 0:
            print('Could not find uuid:[%s]' % text)
            print(url)
            return False
        self.uuid = uuid[0]

        url = 'https://login.weixin.qq.com/qrcode/{}'.format(self.uuid)
        response, err = self.request.get(url=url)
        if err is not None:
            return False
        img = response.content
        with open('a.jpg', 'wb') as f:
            f.write(img)
        return True

if __name__ == '__main__':
    wc = Wechat()
    r = wc.login()
    print(r)
