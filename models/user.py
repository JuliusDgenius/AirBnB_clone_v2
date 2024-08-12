#!/usr/bin/python3
"""This module defines a class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
import os
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel):
    """class defines a user"""
    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column('password', String(128),
                           nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place",
                              backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review",
                               backref="user",
                               cascade="all, delete-orphan")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

        def __init__(self, *args, **kwargs):
            """Initializes user"""
            super().__init__(*args, **kwargs)

        @property
        def password(self):
            return self._password

        @password.setter
        def password(self, pwd):
            """hashing password values"""
            self._password = pwd
