from functools import wraps
from flask import request, jsonify
from sierra_madre_core.errors import HTTPError
from sierra_madre_core.schemas import ValidationError

def handle_endpoint(custom_error=400):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request.id_user = None
                response = func(*args, **kwargs)
                return response
            except HTTPError as http_ex:
                return jsonify({"error": http_ex.message}), http_ex.status_code
            except ValidationError as e:
                custom_errors = []
                for err in e.errors():
                    field_name = ".".join(str(loc) for loc in err["loc"]) or "input"
                    if err["type"] == "missing":
                        custom_errors.append(f"{field_name} is missing")
                    else:
                        custom_errors.append(f"{field_name}: {err['msg']}")
                error = " ,".join(custom_errors)
                return jsonify({"error": error}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), custom_error
        return wrapper
    return decorator
