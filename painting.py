import urllib
import urllib2
import time
import traceback
import static
import json

class painting():
    def __init__(self, openId, shareImage, paintingName, paintingDesc):
        self.openId = openId
        self.shareImage = shareImage
        self.shareTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.paintingName = paintingName
        self.paintingDesc = paintingDesc
        self.nickname = ""
        self.headImg = ""
        self.init_fansInf()

    def init_fansInf(self):
        getFansUrl = "https://api.weixin.qq.com/cgi-bin/user/info?access_token="+static.ACCESS_TOKEN+"&openid="+self.openId+"&lang=zh_CN"
        fansInf = self.sendHttpGet(getFansUrl)
        self.nickname = fansInf['nickname']
        self.headImg = fansInf['headimgurl']

    def sendHttpGet(self, url):
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return json.loads(res)


