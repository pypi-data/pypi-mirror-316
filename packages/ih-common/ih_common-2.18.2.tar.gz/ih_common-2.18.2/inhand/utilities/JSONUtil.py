import json

from datetime import datetime
from bson import ObjectId

def bson_objectId_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

custom_encoder={
    ObjectId: bson_objectId_encoder,
}

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super(JSONEncoder, self).default(obj)