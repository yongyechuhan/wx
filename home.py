from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def homePage(request):
    return render_to_response('home.html')