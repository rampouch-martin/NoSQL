from bson import ObjectId

def clean_mongo_types(doc):
    def convert(value):
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}
        if isinstance(value, list):
            return [convert(v) for v in value]
        return value
    return convert(doc)
