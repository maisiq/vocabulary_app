from datetime import datetime, timedelta, timezone
datetime.



from passlib.context import CryptContext
from jose import jwt

from src.words.repository import fake_users_db
from src.auth.config import SECRET_KEY, ALGORITM


def create_access_token(data: dict, expire_after: timedelta):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + expire_after
    payload.update({'exp': expire})

    token = jwt.encode(payload, SECRET_KEY, ALGORITM)

    return token


crypto_context = CryptContext(schemes=['md5_crypt'])


def authenticate(username: str, password: str):
    try:
        user = fake_users_db.get(username)
        if user:
            return crypto_context.verify(password, user.get('hashed_password'))
        return None
    except Exception as e:
        return None
