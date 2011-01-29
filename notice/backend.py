import redis

from django.conf import settings

conf = getattr(settings, 'REDIS', {'default': {'DB': 0, 'HOST': 'localhost','PORT': 6380}})
r = redis.Redis(
    conf['default']['HOST'],
    conf['default']['PORT'],
    conf['default']['DB'])

def add_notice(user, message, expire=True):
    if not message or not hasattr(user, 'pk'):
        return False

    key = 'user:%s:notices' % user.pk
    try:
        if r.rpush(key, message):
            if expire:
                r.expire(key, 15)
            return True
    except redis.ConnectionError:
        pass
    return False

def get_notices(user):
    if not hasattr(user, 'pk'):
        return

    key = 'user:%s:notices' % user.pk
    try:
        llen = r.llen(key)
        if llen == 0:
            return
        data = r.lrange(key, 0, llen - 1)
        r.ltrim(key, llen, -1)
        return data
    except redis.ConnectionError:
        return
