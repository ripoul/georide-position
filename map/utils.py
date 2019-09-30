from google.cloud import firestore
import os


def get_vars(name):
    if os.getenv("GAE_ENV", "").startswith("standard"):
        db = firestore.Client()
        doc_ref = db.collection(u"env_vars").document(u"env_prod")
        doc = doc_ref.get().to_dict()
        return doc[name]
    return os.getenv(name)
