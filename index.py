import certificate
import receive
import static
import sign
import json
import painting
import urllib
import urllib2
import traceback
import os
import sys
import logging
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from wxmodel.models import PaintingInfo
from wxmodel.models import NoticerInfo

log = logging.getLogger('wxweb')

@csrf_exempt
def paintingShow(request):
    try:
        openId = "oDjv61BEZrRF7j0sz7Qr4OiTkl2g"
        painting_list = PaintingInfo.objects.all()
        return render_to_response( 'painting_show.html', {'openId':json.dumps(openId), 'paintingList':painting_list})
    except Exception, Argument:
        traceback.print_exc()

@csrf_exempt
def shareImage(request):
    try:
        openId = ""
        if 'openId' in request.GET and request.GET['openId']:
            openId = request.GET['openId']
        token_info = certificate.certificate()
        appId = token_info.appId
        sigurate = sign.Sign(token_info.jsapi_ticket, "http://"+request.get_host()+request.get_full_path())
        sigurate_ret = sigurate.sign()
        data = "{'timestamp':'%s','nonceStr':'%s','signature':'%s'}" % (sigurate_ret['timestamp'], sigurate_ret['nonceStr'], sigurate_ret['signature'])
        return render_to_response( 'upload_image.html', {'sigurate_inf':json.dumps(data), 'appId':json.dumps(appId), 'openId':json.dumps(openId)})
    except Exception, Argument:
        traceback.print_exc()

@csrf_exempt
def showHisChat(request):
    return render_to_response('painting_chat.html')

@csrf_exempt
def uploadImage(request):
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
        filepath = os.path.dirname(__file__)
        filepath+="/media/shareImg/"
        postDict = json.loads(request.body)
        mediaId = postDict['mediaId']
        picname = postDict['picname'] + ".jpg"
        saveRes = saveImage(filepath, picname, mediaId)
        if not saveRes:
            return HttpResponse("fail")

        openId = postDict['openId']
        content = ""
        if 'content' in postDict:
            content = postDict['content']
        painInf = painting.painting(openId, "../media/shareImg/"+picname, picname, content)
        storePaintingInfo(painInf)
        return HttpResponse("success")
    except Exception, Argument:
        print 'traceback.print_exc():'
        traceback.print_exc()
        return HttpResponse(Argument)

def saveImage(filepath, imgName, mediaId):
    accessToken = static.ACCESS_TOKEN
    getServImgUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (accessToken, mediaId)
    urlResp = urllib2.urlopen(getServImgUrl)
    headers = urlResp.info().__dict__['headers']
    if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
        jsonDict = json.loads(urlResp.read())
        return False
    else:
        try:
            buffer = urlResp.read()
            mediaFile = open(filepath+imgName, "wb")
            mediaFile.write(buffer)
            return True
        except Exception, Argument:
            traceback.print_exc()
            return False

def storePaintingInfo(painInf):
    try:
        noticerInf = NoticerInfo.objects.get(open_id=painInf.openId)
    except ObjectDoesNotExist:
        noticerInf = NoticerInfo(open_id=painInf.openId,nick_name=painInf.nickname,user_head_img=painInf.headImg)
        noticerInf.save()

    paintingInf = PaintingInfo(open_id=noticerInf,pic_name=painInf.paintingName,pic_src=painInf.shareImage,share_time=painInf.shareTime)
    paintingInf.save()

def sendHttpGet(url):
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return json.loads(res)