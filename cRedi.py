import motionless
import redis
import webbrowser

redis_db = redis.StrictRedis()

def load_testdata():
    redis_db.geoadd("shops", 13.361389, 38.115556, "Palermo")
    redis_db.geoadd("shops", 15.087269, 37.502669, "Catania")

def test_testdata():
    dist = redis_db.geodist("shops", "Palermo", "Catania", "km")
    print(dist)

    shops = redis_db.georadius("shops", 15, 37, 1000, "km")
    print(shops)

    url = motionless.CenterMap(lat=37.502669, lon=15.087269).generate_url()
    webbrowser.open(url)

    map = motionless.DecoratedMap(lat=37.502669, lon=15.087269)
    map.add_marker(motionless.LatLonMarker(37.502669, 15.087269))
    map.add_marker(motionless.LatLonMarker(13.361389, 38.115556))
    webbrowser.open(map.generate_url())