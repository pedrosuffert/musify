from datetime import datetime
from typing import Union, List

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
Base.__allow_unmapped__ = True

IntColumn = Union[Column, int]
StrColumn = Union[Column, str]
DateColumn = Union[Column, datetime]
BinaryColumn = Union[Column, bytes]


class Music(Base):
    __tablename__ = "musics"

    id: IntColumn = Column(Integer, primary_key=True, autoincrement=True)
    name: StrColumn = Column(String, nullable=False)
    lyrics: StrColumn = Column(String)
    language: StrColumn = Column(String)
    clip: BinaryColumn = Column(LargeBinary)
    artist_id: IntColumn = Column(
        Integer, ForeignKey("artists.id", ondelete="CASCADE"), nullable=False
    )
    album_id: IntColumn = Column(
        Integer, ForeignKey("albums.id", ondelete="CASCADE"), nullable=False
    )

    artist: "Artist" = relationship("Artist", back_populates="musics")
    album: "Album" = relationship("Album", back_populates="musics")

    def as_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "lyrics": self.lyrics,
            "language": self.language,
            "clip": self.clip,
            "artist_id": self.artist_id,
            "album_id": self.album_id,
        }


class Artist(Base):
    __tablename__ = "artists"

    id: IntColumn = Column(Integer, primary_key=True, autoincrement=True)
    name: StrColumn = Column(String, nullable=False)
    birth_date: DateColumn = Column(
        DateTime, nullable=False, default=datetime.isoformat(datetime.utcnow())
    )
    photo: StrColumn = Column(String)

    albums: List["Album"] = relationship(
        "Album", back_populates="artist", cascade="all, delete-orphan"
    )
    musics: List["Music"] = relationship(
        "Music", back_populates="artist", cascade="all, delete-orphan"
    )

    def as_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": self.birth_date,
            "photo": self.photo.title() if self.photo else None,
        }


class Album(Base):
    __tablename__ = "albums"

    id: IntColumn = Column(Integer, primary_key=True, autoincrement=True)
    name: StrColumn = Column(String)
    release_date: DateColumn = Column(
        DateTime, nullable=False, default=datetime.isoformat(datetime.utcnow())
    )
    cover: BinaryColumn = Column(LargeBinary)
    artist_id = Column(
        Integer, ForeignKey("artists.id", ondelete="CASCADE"), nullable=False
    )

    artist: "Artist" = relationship("Artist", back_populates="albums")
    musics: List["Music"] = relationship(
        "Music", back_populates="album", cascade="all, delete-orphan"
    )

    def as_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "release_date": self.release_date,
            "cover": self.cover,
            "artist_id": self.artist_id,
        }
