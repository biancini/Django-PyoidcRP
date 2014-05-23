pyoidc_rp_django
================

Django module that includes pyoidc relying party code into a Django application.
To install this example:
 * Install an OpenID Provider with YAIS:
   ```
   sudo apt-get install apache2 vim ntp git libapache2-mod-wsgi mysql-server-5.5 python-mysqldb

   cd /opt ; git clone https://github.com/its-dirg/yais

   cd /opt/yais ; python setup.py install

   mkdir /opt/projects ; yaisLinux.sh /opt/projects

	- Do you want to install IdProxy (Y/n):		n 
	- Do you want to install Social2Saml (Y/n):	n
	- Do you want to install verify_entcat (Y/n):	n 
	- Do you want to install dirg-web (Y/n):	n 
	- Do you want to install saml2test (Y/n):	n 
	- Do you want to install pyoidc (Y/n):		Y 
	- Do you want to install pysaml2 (Y/n):		n 
	- Do you want to install oictest (Y/n):		n 
	- Do you want to install oictestGui (Y/n):	n

  sudo pip install pycrypto==2.6.1 ; easy_install pycrypto

  cd /opt/projects/pyoidc/oidc_example/op2
	
  cp config.py.example config.py
	
  vim config.py:

  ---------------------------------------------------------------
  ...
  baseurl = "https://<YOUR.VM.FQDN>"
  # Use the default key or change with another one.
  keys = { 
    	"RSA": {
  	  "key": "cp_keys/key.pem",
	  "usage": ["enc", "sig"]			
	}
  }

  # Modify this if you want host your OpenID Provider on HTTPS 
  SERVER_CERT = "certs/server.crt" 
  SERVER_KEY = "certs/server.key"
	
  ---------------------------------------------------------------
```

 * Start the OpenID Provider by executing the command:
   ```
   cd /opt/projects/pyoidc/oidc_example/op2 ; sudo ./server.py -p 8092 config
   ```

 * Install Django with pip installler:
   ```
   sudo pip install --upgrade Django
   sudo pip install django-mako
   ```

 * Create a New DB and a New User:
   ```
   mysql -u root -p
   mysql> CREATE DATABASE oidc_users;
   mysql> GRANT ALL ON oidc_users.* to openid@'localhost' identified by 'openidpassword';
   
   mysql> quit
   ```

* Retrieve the code of django_rp from the GitHub Repository:
  ```
  cd /tmp ; git clone https://github.com/biancini/pyoidc_rp_django.git
  ```

* Copy the directory “django_rp” into “/var/www”:
  ```
  cp -Rf /tmp/pyoidc_rp_django/django_rp /var/www/
  ```

* Copy and modify the “conf.py” file:
  ```
  cd /var/www/django_rp/oidc_django

  cp conf.py.example conf.py

  vim conf.py:

  ----------------------------------------------------------------------
  BASE = "https://<YOUR.VM.FQDN>:" + str(PORT) + "/"
	
  SERVER_KEY = ''
  SERVER_CERT = ''

  ....

  CLIENTS = {
   	# The ones that support webfinger, OP discovery and client registration
	# This is the default, any client that is not listed here is expected to
        # support dynamic discovery and registration.
	"": {
       		"client_info": ME,
       		"behaviour": BEHAVIOUR
	},
	#### REMOVE ANY OTHER CLIENTS ####
  }
  ----------------------------------------------------------------------
  ```

* Modify the ``/var/www/django_rp/settings.py`` file by inserting the right values of the DB and User created:
  ```
  'NAME': 'oidc_users',                 # Or path to database file if using sqlite3.
  'USER': 'openid',                     # Not used with sqlite3.
  'PASSWORD': 'openidpassword',         # Not used with sqlite3.
  ```

* Move on ``/var/www/django_rp/`` and execute the command:
  ```
  cd /var/www/django_rp ; python manage.py syncdb
  ```
  this will synchronize the database structures and create the Django Auth System surperuser.

* Activate the ``default-ssl`` site and ``ssl`` module of Apache2:
  ```
  cd /etc/apache2/sites-available ; a2ensite default-ssl
	
  cd /etc/apache2/mods-available ; a2enmod ssl
  ```

* Modify the ``default-ssl`` site by adding to the tail (but after the closure of Virtualhost) this piece of code:
  ```
  ## Added for django_rp ##

  WSGIPassAuthorization On
  WSGIScriptAlias / /var/www/django_rp/wsgi.py

  <Directory /var/www/django_rp>
     <Files wsgi.py>
        Order allow,deny
        Allow from all
     </Files>
  </Directory>
  ```

* Restart Apache2 service:
  ```
  service apache2 restart
  ```

* Connect to ``https://<YOUR.VM.FQDN>`` and access with ``test@<YOUR.VM.FQDN>:8092``.

* Insert as username ``diana`` and as password ``krall`` and enjoy.
