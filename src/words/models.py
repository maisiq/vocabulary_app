from typing import Annotated
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, UniqueConstraint

from src.config.db_config import Base
from src.words.schemas import PartOfSpeech, Language


uuid_pk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]





class Translation(Base):
    __tablename__ = 'translation'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    translation: Mapped[str]
    part_of_speech: Mapped['PartOfSpeech']
    wordname: Mapped[str] = mapped_column(ForeignKey('words.word', ondelete='CASCADE'))
    word: Mapped['Word'] = relationship(back_populates='translations')
    language: Mapped[Language]

    __table_args__ = (
        UniqueConstraint('wordname', 'translation'),
    )


class Word(Base):
    __tablename__= 'words'

    id: Mapped[uuid_pk]
    word: Mapped[str] = mapped_column(unique=True)
    translations: Mapped[list['Translation']] = relationship(back_populates='word')
    transcription: Mapped[str] = mapped_column(String(length=156))
