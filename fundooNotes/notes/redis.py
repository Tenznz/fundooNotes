import redis


class RedisCode:

    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        """
        for getting the cache
        :param key: getting the key as user_id
        """
        return self.cache.get(key)

    def set(self, key, value):
        """
        for inserting in the cache
        :param key: key as user_id
        :param value: value will be note data
        """
        return self.cache.set(key, value)

    def put(self, key, value):
        """
        for updating in the cache
        :param key: key as user_id
        :param value: value will be note data
        """
        return self.cache.set(key, value)

    def delete(self, key):
        """
        for deleting in cache
        :param key
        :return
        """
        return self.cache.delete(key)
