from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

IntColumn = Union[Column, int]
StrColumn = Union[Column, str]
JSONColumn = Union[Column, dict, list]
DateColumn = Union[Column, datetime]
BoolColumn = Union[Column, bool]
BinaryColumn = Union[Column, bytes]
# UUIDColumn = Union[Column, uuid.UUID]
FloatColumn = Union[Column, float]



class Music(Base):
    __tablename__ = "music"

    id: IntColumn = Column(Integer, primary_key=True, autoincrement=True)
    name: StrColumn = Column(String, nullable=False)
    lyrics: StrColumn = Column(String, nullable=False)
    language: StrColumn = Column(String, nullable=False)
    clip: BinaryColumn = Column(LargeBinary, nullable=False)

    # artist = relationship("Artist", lazy="joined")
    # genre = relationship("Genre", lazy="joined")
    # album" = relationship("Album,", lazy="joined")


class Artist(Base):
    __tablename__ = "artist"

    id: IntColumn = Column(Integer, primary_key=True, autoincrement=True)
    name: StrColumn = Column(String, nullable=False)
    birth_date: DateColumn = Column(DateTime, nullable=False, default=datetime.utcnow)
    photo: BinaryColumn = Column(LargeBinary, nullable=False)
    
class Artist(Base):
    __tablename__ = "genres"

    id: IntColumn = Column(Integer, primary_key=True, autoincrement=True)
    name: StrColumn = Column(String, nullable=False)
    description: StrColumn = Column(String, nullable=False)