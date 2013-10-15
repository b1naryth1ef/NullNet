import uuid

def get_hash(source=None):
    """
    Generate a 32bit hash from a source, or randomized.
    """
    if source:
        return str(uuid.uuid(source)).replace("-", "")
    return str(uuid.uuid4()).replace("-", "")
