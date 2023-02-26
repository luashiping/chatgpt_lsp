from django_redis import get_redis_connection


class Cache:
    """
    redis常用操作
    """
    CHAT_USER_KEY = "USER_{}_KEY"

    def __init__(self):
        self.conn = get_redis_connection("default")

    def push(self, cache_id, data):
        self.conn.rpush(self.CHAT_USER_KEY.format(cache_id), data)

    def pop(self, cache_id):
        return self.conn.rpop(self.CHAT_USER_KEY.format(cache_id))

redis_cache = Cache()
