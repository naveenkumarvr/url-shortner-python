import redis
# Handling Redis 

# Connecting to redis Server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def check_redis_cache(short_key):
    """
    Check the reids cache and return if the url present in redis
    INPUT:
        short_key(str): Short key / short code representing url
    RETURNS:
        cached_url(str): Returns Original full URL 
    """
    cache_key = f"short_url:{short_key}"
    cached_url = redis_client.get(cache_key)
    if cached_url:
        print(f"Reading from redis cache {short_key}")
        return cached_url

def update_cache(short_key, original_url):
    """
    Updating the redis cache with short_url and the associated original url
    INPUTS:
        short_key(str): Short code 
        original_url(str): Original url associated with the short code
    RETURNS: None
    """
    redis_client.setex(short_key, 17200, original_url)