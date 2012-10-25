from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from functools import wraps

def professor(function):
  def wrap(request, *args, **kwargs):
      # if Professor.objects.filter(user=request.user).exists():
      if True:
          return function(request, *args, **kwargs)
      else:
          raise Http404

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap
