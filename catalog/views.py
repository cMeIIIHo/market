from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template import RequestContext, loader
from django.views import generic
from django.utils import timezone

# Create your views here.

def index(request):
    context = {
        'img_paths': ['catalog/index_lens_1.jpg',
                      'catalog/index_lens_2.jpg',
                      'catalog/index_lens_3.jpg',
                      'catalog/index_lens_4.jpg',]
    }
    return render_to_response("catalog/index.html", context)