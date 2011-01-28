from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.http import HttpResponse, Http404

def index(request, template_name):
    return render(template_name, {}, RequestContext(request))
