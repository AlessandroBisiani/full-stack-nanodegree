#! /usr/bin/env python3
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return serializable restaurant data
        """
        return {
            'id'    : self.id,
            'name'  : self.name
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        """ return serializable menu item data
        """
        return {
            'course'        : self.course,
            'description'   : self.description,
            'id'            : self.id,
            'name'          : self.name,
            'price'         : self.price
        }

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
