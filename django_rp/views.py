from djangomako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
  args = {
   "userinfo": request.session['userinfo']
  }
  return render_to_response("opresult.mako", args)
