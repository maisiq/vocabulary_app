from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, OAuth2AuthorizationCodeBearer

from src.words.repository import fake_users_db
from .exceptions import CredentialsException

from .config import SECRET_KEY, ALGORITM


SCOPES = {
    'admin:read': 'Read-only role',
    'admin:write': 'role with',
    'word:add': 'role with',
    'word:update': 'role with',
}


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login/token', scopes=SCOPES)

codeflow_schema = OAuth2AuthorizationCodeBearer(
    authorizationUrl='/login/authorization',
    tokenUrl='/login/token'
)


def get_current_user(security_scopes: SecurityScopes, token: str = Depends(codeflow_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITM])
        username = payload.get('sub')
        user_scopes = payload.get('scopes')

        if username is None:
            raise CredentialsException
        for scope in security_scopes.scopes:
            if scope not in user_scopes:
                raise CredentialsException
        return fake_users_db[username]

    except JWTError:
        raise CredentialsException
