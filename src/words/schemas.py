from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


class PartOfSpeech(Enum):
    verb = "verb"
    prep = "prep"
    noun = "noun"
    adj = "adj"
    pronoun = "pronoun"
    adverb = "adverb"
    conjuction = "conjuction"
    interjection = "interjection"


class Language(str, Enum):
    Russian = 'RU'


class TranslationDTO(BaseModel):
    # id: UUID
    partOfSpeech: PartOfSpeech = Field(alias='part_of_speech') # speach заменить...
    translation: str
    language: Language = Language.Russian


class CreateWordRequest(BaseModel):
    word: str
    transcription: str
    translations: list[TranslationDTO] = []


class WordDTO(BaseModel):
    word: str
    transcription: str
    translations: list[TranslationDTO]
    # text_usage: list[str]
    image_usage: list[str] | None = None
    pronunciation_br: str | None = None
    pronunciation_am: str | None = None