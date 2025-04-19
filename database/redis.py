import redis
import json
from typing import Optional, Any
from datetime import timedelta
#mettre les type pour tous les fonctions 
class RedisCache:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key: str, value: Any, expiration: Optional[int] = None):
        """
        Stocke une valeur dans le cache
        :param key: Clé de cache
        :param value: Valeur à stocker (sera sérialisée en JSON)
        :param expiration: Durée de vie en secondes (optionnel)
        """
        try:
            serialized_value = json.dumps(value)
            if expiration:
                self.redis_client.setex(key, expiration, serialized_value)
            else:
                self.redis_client.set(key, serialized_value)
            return True
        except Exception as e:
            print(f"Erreur lors du stockage dans Redis: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Récupère une valeur du cache
        :param key: Clé de cache
        :return: Valeur désérialisée ou None si non trouvée
        """
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération depuis Redis: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Supprime une clé du cache
        :param key: Clé à supprimer
        :return: True si supprimé, False sinon
        """
        return bool(self.redis_client.delete(key))

    def set_session(self, session_id: str, user_data: dict):
        """
        Stocke une session utilisateur
        :param session_id: ID de session
        :param user_data: Données utilisateur
        """
        expiration = int(timedelta(hours=24).total_seconds())
        self.set(f"session:{session_id}", user_data, expiration)

    def get_session(self, session_id: str) -> Optional[dict]:
        """
        Récupère une session utilisateur
        :param session_id: ID de session
        :return: Données de session ou None
        """
        return self.get(f"session:{session_id}")

    def cache_etudiant(self, etudiant_id: str, data: dict):
        """
        Met en cache les données d'un étudiant
        :param etudiant_id: ID de l'étudiant
        :param data: Données de l'étudiant
        """
        expiration = int(timedelta(hours=1).total_seconds())
        self.set(f"etudiant:{etudiant_id}", data, expiration)

    def get_etudiant_cache(self, etudiant_id: str) -> Optional[dict]:
        """
        Récupère les données d'un étudiant du cache
        :param etudiant_id: ID de l'étudiant
        :return: Données de l'étudiant ou None
        """
        return self.get(f"etudiant:{etudiant_id}")

    def invalider_cache_etudiant(self, etudiant_id: str):
        """
        Invalide le cache d'un étudiant
        :param etudiant_id: ID de l'étudiant
        """
        self.delete(f"etudiant:{etudiant_id}")

# Exemple d'utilisation :
# cache = RedisCache()
# cache.set_session("123", {"user_id": "456", "role": "admin"})
# session = cache.get_session("123")
