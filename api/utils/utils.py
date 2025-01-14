from functools import wraps
from flask import request, abort
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from config.config import Config
from flask import g, jsonify
import jwt
from operator import itemgetter
from urllib.parse import parse_qs

def pagination(data, results):
    response = {}

    if data.get('page_size'):
        page = max(int(data.get('page')), 1)
        page_size = int(data.get('page_size'))

        total_items = len(results)
        total_pages = max((total_items + page_size - 1) // page_size, 1)

        response['count'] = total_pages
        response['page_count'] = min(page, total_pages)
        response['page_size'] = page_size

        start = (response['page_count'] - 1) * page_size
        response['results'] = results[start:start + page_size]

    else:
        response['count'] = 1
        response['page_size'] = None
        response['page_count'] = 1
        response['results'] = results

    return response


def ordering(data, keys, results):
    ordering_param = data.get('ordering')
    if ordering_param:
        ordering_param = ordering_param.strip()

        # Heater üçün product-a uyğunluğu təmin edirik
        if ordering_param == "heater":
            ordering_param = "product"
        elif ordering_param == "-heater":
            ordering_param = "-product"

        if ordering_param in keys or (ordering_param[0] == '-' and ordering_param[1:] in keys):
            reverse = ordering_param[0] == '-'
            key_name = ordering_param[1:] if reverse else ordering_param

            # None dəyərlərini idarə edirik
            for result in results:
                if result.get(key_name) is None:
                    result[key_name] = ""

            # Sıralama aparılır
            results = sorted(
                results,
                key=itemgetter(key_name),
                reverse=reverse
            )
    return results

# CSRF check decorator
def csrf_protected(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        csrf_token = request.headers.get('X-CSRFToken')  # Token should be in X-CSRFToken header
        lang = request.headers.get('Accept-Language', 'en')  # Default language is English ('en')

        # Message definitions
        messages = {
            'refresh_page': {
                'ru': "Обновите пожалуйста страницу",
                'en': "Please refresh the page"
            }
        }

        # If CSRF token is missing or invalid
        if not csrf_token:
            abort(403, {'message': messages['refresh_page'].get(lang, "Please refresh the page")})

        try:
            # Validate the CSRF token
            serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
            serializer.loads(csrf_token, salt=Config.SALT)
        except (BadSignature, SignatureExpired):
            abort(403, {'message': messages['refresh_page'].get(lang, "Please refresh the page")})

        return func(*args, **kwargs)

    return decorated_function

# JWT token required decorator
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return False  # No token, returns False

        try:
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token['sub']['user_id']
            g.user_id = user_id

        except jwt.ExpiredSignatureError:
            return False  # Token expired, returns False
        except jwt.InvalidTokenError:
            return False  # Invalid token, returns False

        return f(*args, **kwargs)

    return decorated_function

def parse_request_body():

    body = request.get_data().decode('utf-8')
    data_dict = parse_qs(body)
    data = {key: value_list[0] for key, value_list in data_dict.items()}
    return data