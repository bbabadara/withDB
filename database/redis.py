import redis
import json

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

    def mettre_en_cache(self, cle, valeur, duree=300):
        self.client.setex(cle, duree, json.dumps(valeur))

    def recuperer_du_cache(self, cle):
        data = self.client.get(cle)
        return json.loads(data) if data else None
