from django.contrib import auth
from django.contrib.auth import load_backend
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

from django.shortcuts import render
from mako.lookup import TemplateLookup
from djangomako.shortcuts import render_to_response
from django.http import HttpResponse
from urlparse import parse_qs
from jwkest.jws import alg2keytype
from oic.utils.http_util import Redirect
from backends import OpenIdUserBackend

from oidc_django import oidc, conf

import urllib
import threading

class OpenIdMiddleware(object):
    """
    Middleware for utilizing OpenId authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username with OpenId connect.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.
    """

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the OpenIdUserMiddleware class.")

        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
	    return

        try:
            userinfo = request.session['userinfo']
        except Exception, e:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, OpenIdUserBackend):
                        auth.logout(request)
                except ImproperlyConfigured as e:
                    # backend failed to load
                    auth.logout(request)
        else:
            # We are seeing this user for the first time in this session, attempt
            # to authenticate the user.
            user = auth.authenticate(userinfo=userinfo)
            if user:
                # User is valid.  Set request.user and persist user in the session
                # by logging the user in.
                request.user = user
                auth.login(request, user)

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username
