# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply
import certificate
import sign
import traceback

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "youxiu13717891108"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData   #后台打日志
            token_info = certificate.certificate()
            sigurate = sign.Sign(token_info.jsapi_ticket, web.ctx.home)
            sigurate_ret = sigurate.sign()
            print "signature:"+sigurate_ret['signature']

            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                if recMsg.MsgType == 'text':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = "你好，欢迎进入智绘演意公众号。"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                elif recMsg.MsgType == 'image':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = "感谢你的上传"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                elif recMsg.MsgType == 'event' and recMsg.Event == "CLICK":
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = "即将上线！"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            print 'traceback.print_exc():'
            traceback.print_exc()
            return Argment