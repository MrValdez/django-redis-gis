import redis
redis_db = redis.StrictRedis()

def load_testdata():
    redis_db.geoadd("shops", 13.361389, 38.115556, "Palermo")
    redis_db.geoadd("shops", 15.087269, 37.502669, "Catania")

def test_testdata():
    dist = redis_db.geodist("shops", "Palermo", "Catania", "km")
    print(dist)
    
    shops = redis_db.georadius("shops", 15, 37, 1000, "km")
    print(shops)