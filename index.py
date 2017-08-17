import certificate
import sign
import json
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

@csrf_exempt
def uploadImage(request):
    token_info = certificate.certificate()
    appId = token_info.appId
    sigurate = sign.Sign(token_info.jsapi_ticket, "http://"+request.getHost()+request.get_full_path())
    sigurate_ret = sigurate.sign()
    print "signature:" + sigurate_ret['signature']
    data = "{'timestamp':'%s','nonceStr':'%s','signature':'%s'}" % (sigurate_ret['timestamp'], sigurate_ret['nonceStr'], sigurate_ret['signature'])
    return render_to_response( 'index.html', {'sigurate_inf':json.dumps(data), 'appId':json.dumps(appId)})

@csrf_exempt
def shareImage(request):
    token_info = certificate.certificate()
    appId = token_info.appId
    sigurate = sign.Sign(token_info.jsapi_ticket, "http://"+request.get_host()+request.get_full_path())
    sigurate_ret = sigurate.sign()
    print "signature:" + sigurate_ret['signature']
    data = "{'timestamp':'%s','nonceStr':'%s','signature':'%s'}" % (sigurate_ret['timestamp'], sigurate_ret['nonceStr'], sigurate_ret['signature'])
    return render_to_response( 'image_viewer.html', {'sigurate_inf':json.dumps(data), 'appId':json.dumps(appId)})