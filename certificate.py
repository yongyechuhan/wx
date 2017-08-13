import xml.etree.ElementTree as ET
import urllib
import urllib2
import json
import time
import static
import traceback

access_param = "access_token"
jsapi_param = "ticket"
expire_param = "expires_in"

def checkTokenVlaid():
    if static.TOKEN_INIT_TIME is None:
        print False
        return False
    else:
        now = int(time.time())
        print now - static.TOKEN_INIT_TIME
        if not static.TOKEN_EXPIRE_TIME and now - static.TOKEN_INIT_TIME >= static.TOKEN_EXPIRE_TIME:
            return False
        else:
            return True

def setCacheInfo(expire_time, access_token, jsapi_ticket):
    static.TOKEN_INIT_TIME = int(time.time())
    static.TOKEN_EXPIRE_TIME = expire_time
    static.ACCESS_TOKEN = access_token
    static.JSAPI_TICKET = jsapi_ticket

class certificate():
    def __init__(self):
        self.appId = "wxd5b3ccd7e8f8b824"
        self.appSecret = "09bae2c8d09d5a9dd2b5e7f29629b712"
        self.accessToken = ""
        self.jsapi_ticket = ""
        self.setToken()

    def setToken(self):
        try:
            if checkTokenVlaid():
                self.accessToken = static.ACCESS_TOKEN
                self.jsapi_ticket = static.JSAPI_TICKET
                return

            getAccessTokenUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+self.appId+"&secret="+self.appSecret
            tokenInfo = self.sendHttpGet(getAccessTokenUrl)
            access_token = tokenInfo["%s" % access_param]

            print "get access_token:"+access_token
            if access_token is not None:
                self.accessToken = access_token

            getTicketUrl = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token="+access_token+"&type=jsapi"
            tokenInfo = self.sendHttpGet(getTicketUrl);
            jsapi_ticket = tokenInfo["%s" % jsapi_param]
            if jsapi_ticket is not None:
                self.jsapi_ticket = jsapi_ticket

            expire_time = tokenInfo["%s" % expire_param]
            print "get jspai_ticket:"+jsapi_ticket+" expireTime:"+str(expire_time)

            setCacheInfo(expire_time, access_token, jsapi_ticket)

            print "set init_time:"+str(static.TOKEN_INIT_TIME)
        except Exception, Argment:
            print 'traceback.print_exc():'
            traceback.print_exc()
            return Argment

    def sendHttpGet(self, url):
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print res
        return json.loads(res)
