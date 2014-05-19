from django.shortcuts import render
from mako.lookup import TemplateLookup
from djangomako.shortcuts import render_to_response
from django.http import HttpResponse
from urlparse import parse_qs
from jwkest.jws import alg2keytype
from oic.utils.http_util import Redirect

import urllib
import oidc
import conf

CLIENTS = oidc.OIDCClients(conf)

def start_response(status, headers):
  # Empty method
  return

def home(request):
  return render(request, "home.html")

def openid(request):
  return render_to_response("opchoice.mako", { "op_list": conf.CLIENTS.keys() })

def rp(request):
  if "uid" in request.GET.keys():
    client = CLIENTS.dynamic_client(request.GET["uid"])
    request.session["op"] = client.provider_info["issuer"]
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
  client = CLIENTS[request.session["op"]]
  try:
    query = parse_qs(request.META['QUERY_STRING'])
    userinfo = client.callback(query)
  except oidc.OIDCError as err:
    return render_to_response("operror.mako", { "error": "%s" % error })
  except Exception:
    raise
  else:
    return render_to_response("opresult.mako", { "userinfo": userinfo })

def logout(request):
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
