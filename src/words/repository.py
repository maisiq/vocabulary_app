
import logging
from math import ceil
from uuid import uuid4
from typing import List

from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from .models import Word, Translation
from .schemas import WordDTO, TranslationDTO

data = [
    {
        "word": "title",
        "transcription": "ˈtaɪtl",
        "translation_ru": [
            {
            "id": uuid4(),
            "partOfSpeech": "noun",
            "translation": "название"
            }, 
            {
            "id": uuid4(),
            "partOfSpeech": "noun",
            "translation": "титул"
            },
        ],
        "text_usage": [{
            "example": "the title song on the CD",
            "translation": "заглавная композиция компакт-диска"
        }]
    },
    {
        "word": "molest",
        "transcription": "məˈlest",
        "translation_ru": [
            {
            "id": uuid4(),
            "partOfSpeech": "verb",
            "translation": "приставать"
            }, 
            {
            "id": uuid4(),
            "partOfSpeech": "verb",
            "translation": "досаждать"
            },
        ],
        "text_usage": [{
            "example": "molest a child",
            "translation": "покушаться на растление малолетнего"
    }]
}
]



fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$1$xB3HQDB7$isCipeWEAJm4ulkbMmrtg/", #102030
        "disabled": False,
        "vocabulary": []
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$1$L3du3ROV$jgy.w4yThHLELMGjqTbC80", #112233
        "disabled": True,
        "vocabulary": []
    },
}

class WordRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, per_page: int = 10, page: int = 1) -> List[Word]:
        query = select(Word).options(selectinload(Word.translations))
        result = await self.session.execute(query)

        return result.scalars().all()

    async def add(self, word: dict, translations: List[dict] = []):
        try:
            new_word = Word(**word)

            if translations:
                translations_orm = [Translation(**t) for t in translations]
                new_word.translations.extend(translations_orm)

            self.session.add(new_word)

        except (SQLAlchemyError, AttributeError, IntegrityError) as e:
            logging.error(e)

    async def retrieve_word_by_name(self, word: str) -> Word | None:
        query = (select(Word)
                 .options(selectinload(Word.translations))
                 .filter_by(word=word))
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def add_translations(self, word: str, translations: List[dict]):
        translations_db = [Translation(**t) for t in translations]

        word_db: Word = await self.retrieve_word_by_name(word)
        if word_db is None:
            raise NoResultFound

        word_db.translations.extend(translations_db)
        self.session.add(word_db)
        
    async def update_word(self, word_: str, transcription: str | None = None):
        word_db = await self.retrieve_word_by_name(word_)
        if word_db is None:
            raise NoResultFound
        print(transcription)
        if transcription is not None:
            word_db.transcription = transcription
        
        self.session.add(word_db)
        await self.session.commit()
        
