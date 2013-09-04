'''
Created on 2013-8-8

@author: hgq
'''
from django.http.response import HttpResponse, Http404
import datetime
from django.shortcuts import render_to_response

def index(request):
      return HttpResponse("Hello, Django.")
  
def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    assert False
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)