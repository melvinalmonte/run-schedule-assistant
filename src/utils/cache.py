import redis
from redis.exceptions import RedisError

from src.settings import settings

config = settings.get_settings()


class RedisAccess:
    """
    A class to handle connections and operations to a Redis datastore.

    Attributes:
        host (str): The hostname of the Redis server.
        port (int): The port on which the Redis server is listening.
        password (str): The password for authentication if required.
        connection (redis.Redis): A Redis connection object.
    """

    def __init__(self, host=config.REDISHOST, port=config.REDISPORT, password=config.REDISPASSWORD):
        """
        Initializes the RedisAccess object and establishes a connection to the Redis server.

        Parameters:
            host (str): The hostname of the Redis server. Defaults to 'localhost'.
            port (int): The port on which the Redis server is listening. Defaults to 6379.
            password (str): The password for authentication if required. Defaults to None.
        """
        self.host = host
        self.port = port
        self.password = password
        self.connection = self.connect_to_redis()

    def connect_to_redis(self):
        """
        Establishes a connection to the Redis server.

        Returns:
            redis.Redis: A Redis connection object, or None if the connection fails.
        """
        try:
            print(f"Connecting to Redis at {self.host}:{self.port}")
            return redis.Redis(host=self.host, port=self.port, password=self.password)
        except RedisError as e:
            print(f"Failed to connect to Redis: {e}")
            return None

    def get_value(self, key):
        """
        Retrieves a value from Redis by key.

        Parameters:
            key (str): The key of the value to retrieve.

        Returns:
            str: The value associated with the key, or None if the operation fails or the key does not exist.
        """
        try:
            print(f"Getting value for key '{key}'")
            return self.connection.get(key)
        except RedisError as e:
            print(f"Failed to get value for key '{key}': {e}")
            return None

    def set_value(self, key, value, expiry=21600):
        """
        Sets a value in Redis by key.

        Parameters:
            key (str): The key of the value to set.
            value (str): The value to set.
            expiry (int): The expiry time in seconds. Defaults to 21600 (6 hours).

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            print(f"Setting value for key '{key}'")
            return self.connection.setex(key, expiry, value)
        except RedisError as e:
            print(f"Failed to set value for key '{key}': {e}")
            return False
