import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    full_name = Column(String(250))
    password = Column(String(250), nullable=False)
    followers = relationship('User', secondary='followers')
    posts = relationship('Post', back_populates='user')


followers = Table('followers', Base.metadata,
                  Column('follower_id', Integer, ForeignKey('users.id'), CheckConstraint(
                      'follower_id <> following_id'), primary_key=True),
                  Column('following_id', Integer, ForeignKey(
                      'users.id'), primary_key=True),
                  Column('created_at', DateTime(timezone=True)))


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='posts')
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True))
    comments = relationship('Comment', back_populates='post')
    likes = relationship('User', secondary='posts_likes')
    media = relationship('Media', back_populates='post')


followers = Table('posts_likes', Base.metadata,
                  Column('user_id', Integer, ForeignKey(
                      'users.id'), primary_key=True),
                  Column('post_id', Integer, ForeignKey(
                      'posts.id'), primary_key=True),
                  Column('created_at', DateTime(timezone=True)))

class Media(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    post = relationship('Post', back_populates='media')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    message = Column(String(250), nullable=False)
    created_at = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user = relationship('User')
    post = relationship('Post', back_populates='comments')
    likes = relationship('User', secondary='comments_likes')

followers = Table('comments_likes', Base.metadata,
                  Column('user_id', Integer, ForeignKey(
                      'users.id'), primary_key=True),
                  Column('comment_id', Integer, ForeignKey(
                      'comments.id'), primary_key=True),
                  Column('created_at', DateTime(timezone=True)))


# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
