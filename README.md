pyoidc_rp_django
================

Django module that includes pyoidc relying party code into a Django application.
To install this example:
 * copy the ``django_rp`` folder into ``/var/www``
 * configure apache adding the following line to the default webserver
   ```
   WSGIPassAuthorization On
   WSGIScriptAlias / /var/www/django_rp/wsgi.py

   <Directory /var/www/django_rp>
       <Files wsgi.py>
           Order allow,deny
           Allow from all
       </Files>
   </Directory>
   ```
 * configure the pyoidc rp renaming the ``conf.py.example`` to ``conf.py`` and configure
   accordingly (as described inside the [PyOIDC Project](https://github.com/rohe/pyoidc).
 * access the client in Django!
