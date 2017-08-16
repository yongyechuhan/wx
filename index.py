import certificate
import sign
import json
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

@csrf_exempt
def index(request):
    token_info = certificate.certificate()
    sigurate = sign.Sign(token_info.jsapi_ticket, request.path)
    sigurate_ret = sigurate.sign()
    print "signature:" + sigurate_ret['signature']
    data = "{'timestamp':%s,'nonceStr':%s,'signature':%s}" % (sigurate_ret['timestamp'], sigurate_ret['nonceStr'], sigurate_ret['signature'])
    return render_to_response( 'index.html', {'sigurate_inf':json.dumps(data)})