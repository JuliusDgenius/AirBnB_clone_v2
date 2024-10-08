#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """Convert instance into dict format"""
        dct = {}
        dct.update(self.__dict__)
        if "created_at" in dct:
            dct["created_at"] = dct["created_at"].isoformat()
        if "updated_at" in dct:
            dct["updated_at"] = dct["updated_at"].isoformat()
        if '_password' in dct:
            dct['password'] = dct['_password']
            dct.pop('_password', None)
        if 'amenities' in dct:
            dct.pop('amenities', None)
        if 'reviews' in dct:
            dct.pop('reviews', None)
        dct["__class__"] = self.__class__.__name__
        dct.pop('_sa_instance_state', None)
        if not save_to_disk:
            dct.pop('password', None)
        return dct

    def delete(self):
        """
        Public instance method that deletes an instance by
        calling its instance method
        """
        models.storage.delete(self)
