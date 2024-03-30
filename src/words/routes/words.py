from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, Security, Query, UploadFile, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.config.db_config import get_session
from src.words.repository import data
from src.words.schemas import WordDTO, TranslationDTO, CreateWordRequest
from src.auth.dependencies import get_current_user
from src.words.repository import WordRepository
from src.words.services import WordService


router = APIRouter()


# Query


@router.get('/words')
async def words(
    per_page: int = Query(default=30, alias='perPage'),
    page: int = 1,
    session: Session = Depends(get_session)
):
    ''' Returns all words in DB separated by page '''

    service = WordService(session)
    return await service.get_all_words(per_page, page)


@router.get('/words/{word}')
async def get_word(word: str, session: Session = Depends(get_session)):
    service = WordService(session)
    word_obj = await service.get_word_by_name(word)

    if word_obj is not None:
        return word_obj
    return Response({'detail': 'Word not found'}, status_code=status.HTTP_404_NOT_FOUND)


# Commands


@router.post('/words')
async def add_word(word_: CreateWordRequest, session: Session = Depends(get_session)):
    ''' Adds a new word to the storage '''
    service = WordService(session)
    result = await service.add_word(word_)

    match result:
        case 201:
            return Response(status_code=status.HTTP_201_CREATED)
            # return RedirectResponse(f'/words/{word_.word}/ru')
        case 400:
            return JSONResponse({'detail': 'Word already exists'}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/words/{word}/{lang}')
async def add_translation_to_word(
    word: str,
    lang: str,
    translations: list[TranslationDTO],
    session: Session = Depends(get_session),
    # user: dict = Security(get_current_user, scopes=['admin:update'])
):
    '''Adds translation to the word'''

    service = WordService(session)
    try:
        await service.add_translations(word, translations)
        return JSONResponse(status_code=status.HTTP_200_OK)
    except (NoResultFound, IntegrityError):
        # if the word doesn't exist in db or translation already does
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch('/words/{word}')
async def update_word(
    word: str,
    transcription: str,
    session: Session = Depends(get_session),
    # user: dict = Security(get_current_user, scopes=['admin:update'])
):
    ''' Change word or transcription '''
    service = WordService(session)
    await service.change_transcription(word, transcription)
    return 'OK'


@router.delete('/words/{word}/{translationId}')
async def delete_translation(
    word: str,
    translation_id: str = Query(alias='translationId'),
    user: dict = Security(get_current_user, scopes=['admin:update'])
):
    ''' Deletes translation '''

    ...


@router.post('/words/{word}/text')
async def add_text_example(
    example: str,  user: dict = Security(get_current_user, scopes=['admin:update'])
):
    ''' Adds text example of usage for the word '''
    pass


@router.put('/words/{word}/{textUsageId}')
async def update_text_example(
    word: str, text_id: Annotated[UUID, Query(alias='textUsageId')]
):
    '''Updates text example of usage'''

    pass


@router.delete('/words/{word}/{textUsageId}')
async def delete_text_example(
    word: str, text_id: Annotated[UUID, Query(alias='textUsageId')]
):
    '''Deletes text example of usage'''

    pass


# @router.post('/words/{word}/image')
# async def add_img_example(
#     word: str, image: UploadFile,  user: dict = Security(get_current_user, scopes=['admin:update'])
# ):
#     ''' Adds example of usage as image '''
#     pass


# @router.delete('/words/{imgUsageId}')
# async def delete_img_example(
#     image_id: Annotated[UUID, Query(alias='imgUsageId')],
#     user: dict = Security(get_current_user, scopes=['admin:update'])
# ):
#     ''' Deletes example of usage as image '''
#     pass
