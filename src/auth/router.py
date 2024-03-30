from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.config import ACCES_TOKEN_EXPIRE_MINUTES
from src.auth.utils.core import authenticate, create_access_token


router = APIRouter(prefix='/login')


@router.get('/authorization')
def authorization(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    scope: str | None = None
):
    code = 'rngstr'
    url = redirect_uri + f'?code={code}' + f'&state={state}'

    return RedirectResponse(url)


@router.post('/token')
def login_for_access_token(request: Request, 
                           grant_type: str = Form(...),
                           client_id: str = Form(...),
                           client_secret: str = Form(...),
                           code: str = Form(...),
                           redirect_uri: str = Form(...),
                           ):
    # grant_type: str, client_id, client_secret, code, redirect_uri
    print(grant_type)
    print(request.form.__dict__)

    # username = form_data.username
    # password = form_data.password

    # if authenticate(username, password):
    #     data = {
    #         'sub': username,
    #         'scopes': form_data.scopes
    #     }

    #     token = create_access_token(
    #         data,
    #         expire_after=timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    #     )

    #     return {
    #         'access_token': token,
    #         'token_type': 'bearer'
    #     }
    # raise HTTPException(401, 'Incorrect username or password')
