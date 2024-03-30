import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from .repository import WordRepository
from .schemas import TranslationDTO, WordDTO, CreateWordRequest
from .utils import Status

from fastapi import status



class WordService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = WordRepository(self._session)

    # async def _commit(self,):
    #     try:
    #         await self.session.commit()
    #     except IntegrityError as e:
    #         logging.error(e)
    #         await self.session.rollback()

    async def get_all_words(self, per_page: int = 10, page: int = 1):
        words_db = await self._repo.list()

        words = [
            WordDTO.model_validate(word, from_attributes=True)
            for word in words_db
        ]

        return words
    
    async def get_word_by_name(self, word: str):
        word_db = await self._repo.retrieve_word_by_name(word)

        if word_db is not None:
            return WordDTO.model_validate(word_db, from_attributes=True)
        # explicit return
        return None

    async def add_word(self, word: CreateWordRequest):
        word_dict = word.model_dump(exclude=['translations'])
        translations = [w.model_dump(by_alias=True) for w in word.translations]

        await self._repo.add(word_dict, translations)

        try:
            await self._session.commit()
            return status.HTTP_201_CREATED
        except IntegrityError as e:
            logging.error(e)
            return status.HTTP_400_BAD_REQUEST
    
    async def add_translations(self, word_: str, translations: list[TranslationDTO]) -> Status:
        # word = await self._repo.retrieve_word_by_name(word_)
        translations: dict = [w.model_dump(by_alias=True) for w in translations]
        
        await self._repo.add_translations(word_, translations)
        await self._session.commit()

    async def change_transcription(self, word: str, transcription: str):
        try:
            await self._repo.update_word(word, transcription=transcription)
            return True
        except NoResultFound as e:
            logging.error(e)
            return False

