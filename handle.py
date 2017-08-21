# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import receive
import reply
import certificate
import sign
import traceback
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt
def handle(request):
    if request.method == 'GET':
        return wx_get(request)
    elif request.method == 'POST':
        return wx_post(request)
    else:
        return HttpResponse("request method error!")

def wx_get(request):
    try:
        data = request.GET
        if len(data) == 0:
            return HttpResponse("hello, this is handle view")
        signature = data['signature']
        timestamp = data['timestamp']
        nonce = data['nonce']
        echostr = data['echostr']
        token = "youxiu13717891108"

        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        print "handle/GET func: hashcode, signature: ", hashcode, signature
        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("")
    except Exception, Argument:
        print 'traceback.print_exc():'
        traceback.print_exc()
        return HttpResponse(Argument)

def wx_post(request):
    try:
        webData = request.body
        print "Handle Post webdata is ", webData  # 后台打日志

        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg):
            if recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "你好，欢迎进入智绘演意公众号。"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return HttpResponse(replyMsg.send())
            elif recMsg.MsgType == 'image':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "感谢你的上传"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return HttpResponse(replyMsg.send())
            elif recMsg.MsgType == 'event' and recMsg.Event == "CLICK":
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "即将上线！"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return HttpResponse(replyMsg.send())
        else:
            print "暂不处理"
            return HttpResponse("success")
    except Exception, Argment:
        print 'traceback.print_exc():'
        traceback.print_exc()
        return HttpResponse(Argment)
