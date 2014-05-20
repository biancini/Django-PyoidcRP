from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from djangomako.shortcuts import render_to_response
from mako.lookup import TemplateLookup
from urlparse import parse_qs
from jwkest.jws import alg2keytype
from oic.utils.http_util import Redirect

from oidc import OIDCClients
import logging
import conf
import urllib

LOGGER = logging.getLogger("")
LOGGER.setLevel(logging.DEBUG)

CLIENTS = OIDCClients(conf)

def start_response(status, headers):
  # Empty method
  return

def openid(request):
  request.session["next"] = request.GET["next"]
  return render_to_response("opchoice.mako", { "op_list": conf.CLIENTS.keys() })

def rp(request):
  if "uid" in request.GET.keys():
    client = CLIENTS.dynamic_client(request.GET["uid"])
    request.session["op"] = client.provider_info["issuer"]
    print client.provider_info["issuer"]
  else:
    client = CLIENTS[query["op"][0]]
    request.session["op"] = query["op"][0]

  try:
    oic_resp = client.create_authn_request(request.session)
  except Exception:
    raise
  else:
    oic_resp(request.environ, start_response)
    resp = HttpResponse(content_type=oic_resp._content_type, status=oic_resp._status)
    for key,val in oic_resp.headers:
      resp[key] = val
    return resp

def authz_cb(request):
  request.session['query'] = request.META['QUERY_STRING']
  return redirect(request.session["next"])

def logout(request):
  logout_url = '/'
  if "op" in request.session:
    client = CLIENTS[request.session["op"]]
    logout_url = client.endsession_endpoint

    try:
      # Specify to which URL the OP should return the user after
      # log out. That URL must be registered with the OP at client
      # registration.
      logout_url += "?" + urllib.urlencode({
        "post_logout_redirect_uri": client.registration_response[
        "post_logout_redirect_uris"][0]})
    except KeyError:
      pass
    else:
      # If there is an ID token send it along as a id_token_hint
      _idtoken = get_id_token(client, request.session)
      if _idtoken:
        logout_url += "&" + urllib.urlencode({
          "id_token_hint": id_token_as_signed_jwt(client, _idtoken, "HS256")})

  request.session.clear()
  oic_resp = Redirect(str(logout_url))
  oic_resp(request.environ, start_response)
  resp = HttpResponse(content_type=oic_resp._content_type, status=oic_resp._status)
  for key,val in oic_resp.headers:
    resp[key] = val
  return resp

def get_id_token(client, session):
    return client.grant[session["state"]].get_id_token()

# Produce a JWS, a signed JWT, containing a previously received ID token
def id_token_as_signed_jwt(client, id_token, alg="RS256"):
    ckey = client.keyjar.get_signing_key(alg2keytype(alg), "")
    _signed_jwt = id_token.to_jwt(key=ckey, algorithm=alg)
    return _signed_jwt
