def individual_serial_history(history) -> dict: 
    return {
        "id": str(history["_id"]),
        "user_id": history["user_id"],
        "description": history["description"],
        # "description_embedding": history["description_embedding"]
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

def individual_serial_todo(todo) -> dict: 
    return {
        "id": str(todo["_id"]),
        "user_id": todo["user_id"],
        "taskTitle": todo["taskTitle"],
        "taskColor": todo["taskColor"],
        "startDate": todo["startDate"],
        "endDate": todo["endDate"],
        "startTime": todo["startTime"],
        "endTime": todo["endTime"],
        "reminderTime": todo["reminderTime"],
        "taskType": todo["taskType"],
        "tag": todo["tag"],
        "label": todo["label"],
        "redirectURL": todo["redirectURL"],
        "progress": todo["progress"],
        "priority": todo["priority"]
    }

def list_serial_todo(todos) -> list[dict]:
    return [individual_serial_todo(todo) for todo in todos]