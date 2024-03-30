from fastapi import HTTPException


CredentialsException = HTTPException(
    status_code=401,
    detail='Not valid credentials',
    headers={
        'WWW-Authenticate': 'Bearer'
    }
)