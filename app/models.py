from sqlalchemy import Column, TEXT, INT, BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import (
   Column, Integer, String, DateTime, Text, LargeBinary,
   ForeignKey, func
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
   __tablename__ = 'User'

   id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(String(255), nullable=False)
   pw = Column(String(255), nullable=False)
   created_at = Column(DateTime, default=func.current_timestamp())
   updated_at = Column(
      DateTime,
      default=func.current_timestamp(),
      onupdate=func.current_timestamp()
   )

   # Relationships
   user_games = relationship("UserGame", back_populates="user", cascade="all, delete-orphan")
   sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Guide(Base):
   __tablename__ = 'Guide'

   id = Column(Integer, primary_key=True, autoincrement=True)
   screenshot = Column(LargeBinary)
   game_guide = Column(Text)
   created_at = Column(DateTime, default=func.current_timestamp())
   updated_at = Column(
      DateTime,
      default=func.current_timestamp(),
      onupdate=func.current_timestamp()
   )

   # Relationships
   user_games = relationship("UserGame", back_populates="guide", cascade="all, delete-orphan")
   sessions = relationship("Session", back_populates="guide", cascade="all, delete-orphan")


class UserGame(Base):
   __tablename__ = 'UserGame'

   id = Column(Integer, primary_key=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)
   game_path = Column(String(255), nullable=False)
   game_name = Column(String(255), nullable=False)
   guide_id = Column(Integer, ForeignKey('Guide.id', ondelete="CASCADE"), nullable=False)
   created_at = Column(DateTime, default=func.current_timestamp())
   updated_at = Column(
      DateTime,
      default=func.current_timestamp(),
      onupdate=func.current_timestamp()
   )

   # Relationships
   user = relationship("User", back_populates="user_games")
   guide = relationship("Guide", back_populates="user_games")


class GameSession(Base):
   __tablename__ = 'GameSession'

   id = Column(Integer, primary_key=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)
   guide_id = Column(Integer, ForeignKey('Guide.id', ondelete="CASCADE"), nullable=False)
   finished_time = Column(DateTime)
   created_at = Column(DateTime, default=func.current_timestamp())
   updated_at = Column(
      DateTime,
      default=func.current_timestamp(),
      onupdate=func.current_timestamp()
   )

   # Relationships
   user = relationship("User", back_populates="sessions")
   guide = relationship("Guide", back_populates="sessions")


class Emotion(Base):
   __tablename__ = 'Emotion'

   id = Column(Integer, primary_key=True, autoincrement=True)
   screenshot = Column(LargeBinary)
   emotion_label = Column(String(255), nullable=False)
   created_at = Column(DateTime, default=func.current_timestamp())
   updated_at = Column(
      DateTime,
      default=func.current_timestamp(),
      onupdate=func.current_timestamp()
   )
