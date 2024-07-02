from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise InvalidToken("Authentication credentials were not provided.")

        jwt_value = auth_header.split(" ")[1]

        jwt_auth = JWTAuthentication()
        try:
            user, token = jwt_auth.authenticate(request)
            if user is None:
                raise InvalidToken("User not authenticated")
            request.user = user
        except (InvalidToken, TokenError) as e:
            raise InvalidToken("Invalid token.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
