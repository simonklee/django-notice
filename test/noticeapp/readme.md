The examples tries to show a full setup for a django-project using uWSGI with
green-threads enabled. Hence the uWSGI and Redis config files as well as setup
scripts.

See `fabric.py` for a overview of the setup-process. For Fabric to work you need
to bootstrap the virtual-envirnoment as well as the python dependencies. 

    `$ ./bootstrap.py` 

Now building Redis and uWsgi can be done with Fabric.

    `$ fab -H name@host:22 deploy`

The uWSGI server will listen on `/tmp/uwsgi_notice.sock` so point your server 
to that, or change the `template/uwsgi.ini`-file to listen on a IP:port if you
prefer that.
