def individual_serial_history(history) -> dict: 
    return {
        "id": str(history["_id"]),
        "user_id": history["user_id"],
        "description": history["description"],
        "description_embedding": history["description_embedding"]
    }

def list_serial_history(histories) -> list[dict]:
    return [individual_serial_history(history) for history in histories]


def individual_serial_user(user) -> dict: 
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "description": user["description"],
        "description_embedding": user["description_embedding"]  
    }

def list_serial_user(users) -> list[dict]:
    return [individual_serial_user(user) for user in users]