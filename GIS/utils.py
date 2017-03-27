import redis


def save_location_to_redis(location):
    redis_db = redis.StrictRedis()

    lat, long = location.lat, location.long
    lat, long = float(lat), float(long)

    # redis uses the order (long, lat)
    redis_db.geoadd(location.category.name, long, lat, str(location.id))


def delete_redis_location(location):
    redis_db = redis.StrictRedis()
    redis_db.zrem(location.category.name, str(location.id))


def find_locations_in_radius(category_name, lat, long, radius):
    '''
    Given a category id, lat, long, and radius,
    return a list of location ids that falls within that vicinity.
    Redis is used to calculate distances.
    '''
    redis_db = redis.StrictRedis()

    results = redis_db.georadius(name=category_name,
                                 latitude=lat,
                                 longitude=long,
                                 radius=radius,
                                 unit="km")
    return results
