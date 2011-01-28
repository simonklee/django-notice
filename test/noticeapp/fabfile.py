import os
import tempfile

from fabric.api import run, sudo, hosts, env
from fabric.context_managers import cd, settings, hide
from fabric.operations import put

# helpers
def on_path(path):
    def deco(func):
        def _wrapper(*args, **kwargs):
            with cd(path):
                return func(*args, **kwargs)
        return _wrapper
    return deco

def proj_path():
    return os.path.realpath(os.path.dirname(__file__))

def render_to_string(template_name, context):
    from django.conf import settings
    from django.template import Template, loader, Context
    template_dir = os.path.join(proj_path(), 'templates')
    try:
        settings.configure(
            TEMPLATE_DIRS=(template_dir,),
            TEMPLATE_LOADERS=('django.template.loaders.filesystem.Loader',))
    except RuntimeError:
        pass

    c = Context(context)
    return loader.get_template(template_name=template_name).render(c)

def create_file(template_name, name, context={}):
    run('mkdir -p ~/build/')
    template = render_to_string(template_name, context)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as fp:
        fp.write(template)
        path = fp.name
    put(path, '~/build/%s' % name)

def add_init_script(template_name, init_name, context={}):
    create_file(template_name, init_name, context)
    sudo('mv ~/build/%s /etc/init.d/%s' % (init_name, init_name))
    sudo('chmod +x /etc/init.d/%s' % init_name)

def silent(func):
    def _wrapper(*args, **kwargs):
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True):
            return func(*args, **kwargs)
    return _wrapper

@silent
def add_anonymus_user(name):
    sudo('adduser --system --no-create-home \
          --disabled-login --disabled-password \
          --group %s' % name)

@silent
def stop_init_d(name):
    sudo('/etc/init.d/%s stop' % name)

def start_init_d(name):
    sudo('/etc/init.d/%s start' % name)

@on_path('/opt')
def update_uwsgi(python='python', init='uwsginotice'):
    stop_init_d(init)
    version = 'uwsgi-0.9.6.6'
    ini_path = os.path.abspath(os.path.join(proj_path(), 'genuwsgi.ini'))

    sudo('wget http://projects.unbit.it/downloads/%s.tar.gz' % version)
    sudo('tar -xvzf %s.tar.gz' % version)

    with settings(warn_only=True):
        sudo('rm -r uwsginotice/')
    sudo('mv %s uwsginotice/' % version)

    with cd('uwsginotice/'):
        sudo('%s uwsgiconfig.py --build' % python)

    add_anonymus_user('uwsgi')
    sudo('chown -R uwsgi:uwsgi uwsginotice/')
    sudo('touch /var/log/uwsginotice.log')
    sudo('chown uwsgi:uwsgi /var/log/uwsginotice.log')

    add_init_script('uwsgid', init, context={'ini_path': ini_path})
    context={
        'proj_path': proj_path(),
        'python_path': os.path.abspath(os.path.join(proj_path(), '..')),
        've_path': os.path.join(proj_path(), 've/')}

    with open(ini_path, 'w') as fp:
        template = render_to_string('uwsgi.ini', context)
        fp.write(template)
    sudo('chown uwsgi %s' % ini_path)
    start_init_d(init)

@on_path('/opt')
def update_redis():
    port = '6380'
    init = 'redis%s' % port
    conf_name = '%s.conf' % port

    stop_init_d(init)
    with settings(warn_only=True):
        sudo('rm -r redisnotice/')

    sudo('git clone git://github.com/antirez/redis.git redisnotice')
    with cd('redisnotice/'):
        sudo('make PREFIX=/opt/redisnotice install')

    add_init_script('redisd', init, context={'port': port})
    add_anonymus_user('redis')

    create_file('redis.conf', conf_name, context={'port': port})
    sudo('mv ~/build/%s /opt/redisnotice/%s' % (conf_name, conf_name))
    sudo('chown -R redis:redis redisnotice/')
    sudo('touch /var/log/redisnotice.log')
    sudo('chown redis /var/log/redisnotice.log')
    start_init_d(init)

def deploy():
    update_redis()
    update_uwsgi()

def reload():
    stop_init_d('uwsginotice')
    start_init_d('uwsginotice')
