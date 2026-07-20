from bson import ObjectId

from app.core.exceptions import AppException


def validate_object_id(object_id: str) -> ObjectId:
    if not ObjectId.is_valid(object_id):
        raise AppException("Invalid ObjectId.", status_code=400)
    return ObjectId(object_id)


def object_id_to_str(document: dict | None) -> dict | None:
    if not document:
        return None

    document["_id"] = str(document["_id"])
    return document


def documents_to_str(documents: list[dict]) -> list[dict]:
    return [object_id_to_str(doc) for doc in documents]