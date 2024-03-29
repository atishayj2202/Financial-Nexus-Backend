from src.client.cockroach import CockroachDBClient
from src.client.firebase import FirebaseClient

cockroachClient = None
firebaseClient = None


def getCockroachClient() -> CockroachDBClient:
    global cockroachClient
    if cockroachClient is None:
        cockroachClient = CockroachDBClient()
    return cockroachClient


def getFirebaseClient() -> FirebaseClient:
    global firebaseClient
    if firebaseClient is None:
        firebaseClient = FirebaseClient()
    return firebaseClient
