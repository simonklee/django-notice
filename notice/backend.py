import redis

r = redis.Redis("localhost")

def add_user(user):
    if r.sadd("users", user.pk):
        return True
    return False

def push_notice(user, message, expire=True):
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
        return (False, None)

    key = 'user:%s:notices' % user.pk
    try:
        llen = r.llen(key)
        if llen == 0:
            return (False, None)

        data = r.lrange(key, 0, llen - 1)
        r.ltrim(key, llen, -1)
        return (True, data)
    except redis.ConnectionError:
        return (False, None)
