import jwt

SECRET_KEY = 'secreto'

async def decrypt_jwt(token_jwt: str = None):
    if token_jwt is not None:
        try:
            return jwt.decode(token_jwt, SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            return None
    else:
        return None