from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Security, Query

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.config.db_config import get_session
from src.words.repository import data
from src.words.schemas import WordDTO, TranslationDTO
from src.auth.dependencies import get_current_user


router = APIRouter()


@router.get('/vocabulary')
def user_vocabulary(user: dict = Security(get_current_user, scopes=['me'])):
    ''' Returns user's dictionary '''

    return data[0]


@router.post('/vocabulary/{word}/{lang}')
async def add_word_to_vocabulary(
    word: str, lang: str, user: dict = Security(get_current_user, scopes=['me'])
):
    ''' Adds the word to user's dict '''

    word = data.get(word)
    if word:
        user['vocabulary'].append(word)
        return 'ok'
    return 'error'


@router.patch('/vocabulary/{word}/{lang}')
async def update_word_status_in_user_dict(
    word: str, lang: str, user: dict = Security(get_current_user, scopes=['me'])
):
    ''' Updates status for the word in user's dict '''
    ...


@router.delete('/vocabulary/{word}/{lang}')
async def delete_word_from_user_dict(
    word: str, lang: str, user: dict = Security(get_current_user, scopes=['me'])
):
    ''' Deletes the word from user's dict '''

    ...


