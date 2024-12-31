
from channels.middleware import BaseMiddleware


from jwt import decode as jwt_decode
from django.conf import settings

import traceback



class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        try:
            token = self.get_token(scope)
            if token:
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_data.get('user_id')
                user = await self.get_user(user_id)
                scope['user'] = user
            else:
                scope['user'] = AnonymousUser()
        except Exception:
            traceback.print_exc()
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

    @staticmethod
    def get_token(scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode()
            if auth_header.startswith('Bearer '):
                return auth_header.split('Bearer ')[1]
        return None

    @staticmethod
    async def get_user(user_id):
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return await User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
