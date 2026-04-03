from flask import request

def get_json_or_error():
    data = request.get_json(silent=True)
    if not data:
        return None, {"error": "Invalid or missing JSON"}, 400
    return data, None, None