import certificate
import receive
import static
import sign
import json
import painting
import urllib
import urllib2
import traceback
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse


serv_img_path = "/usr/local/proc/wxweb/wxweb/static/images/shareImg/"

@csrf_exempt
def paintingShow(request):
    print request.body
    oauth_code = request.GET['code']
    getOAuthTokenUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % ('wxd5b3ccd7e8f8b824','09bae2c8d09d5a9dd2b5e7f29629b712',oauth_code)
    tokenInf = sendHttpGet(getOAuthTokenUrl)
    openId = tokenInf['openid']
    return render_to_response( 'painting_show.html', {'openId':json.dumps(openId)})

@csrf_exempt
def shareImage(request):
    openId = ""
    if 'openId' in request.GET and request.GET['openId']:
        openId = request.GET['openId']
    token_info = certificate.certificate()
    appId = token_info.appId
    sigurate = sign.Sign(token_info.jsapi_ticket, "http://"+request.get_host()+request.get_full_path())
    sigurate_ret = sigurate.sign()
    print "signature:" + sigurate_ret['signature']
    data = "{'timestamp':'%s','nonceStr':'%s','signature':'%s'}" % (sigurate_ret['timestamp'], sigurate_ret['nonceStr'], sigurate_ret['signature'])
    return render_to_response( 'upload_image.html', {'sigurate_inf':json.dumps(data), 'appId':json.dumps(appId), 'openId':json.dumps(openId)})

@csrf_exempt
def uploadImage(request):
    try:
        postDict = json.loads(request.body)
        mediaId = postDict['mediaId']
        picname = postDict['picname']
        saveRes = saveImage(picname, mediaId)
        if not saveRes:
            return HttpResponse("fail")

        openId = postDict['openId']
        print "openId:"+openId
        content = ""
        if 'content' in postDict:
            content = postDict['content']
        print content
        painInf = painting.painting(openId, serv_img_path+picname, picname, content)
        print painInf.headImg+"   "+painInf.nickname
        return HttpResponse("success")
    except Exception, Argument:
        print 'traceback.print_exc():'
        traceback.print_exc()
        return HttpResponse(Argument)

def saveImage(imgName, mediaId):
    accessToken = static.ACCESS_TOKEN
    getServImgUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (accessToken, mediaId)
    urlResp = urllib2.urlopen(getServImgUrl)
    print urlResp
    headers = urlResp.info().__dict__['headers']
    if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
        jsonDict = json.loads(urlResp.read())
        print jsonDict
        return False
    else:
        buffer = urlResp.read()
        mediaFile = file(serv_img_path+imgName+'.jpg', "wb")
        mediaFile.write(buffer)
        print "get successful"
        return True

def sendHttpGet(url):
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return json.loads(res)