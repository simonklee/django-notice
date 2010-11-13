import redis

r = redis.Redis("localhost")

def add_user(user):
    if r.sadd("users", user.pk):
        return True
    return False

def push_message(user, message, expire=True):
    if not message or not hasattr(user, 'pk'):
        return False

    key = 'user:%s:messages' % user.pk

    if r.rpush(key, message):
        if expire:
            r.expire(key, 15)
        return True
    return False

def get_messages(user):
    if not hasattr(user, 'pk'):
        return (False, None)

    key = 'user:%s:messages' % user.pk
    llen = r.llen(key)
    if llen == 0:
        return (False, None)

    data = r.lrange(key, 0, llen - 1)
    r.ltrim(key, llen, -1)
    return (True, data)