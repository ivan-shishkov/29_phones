import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String

Base = declarative_base()

engine = create_engine(os.environ.get('DATABASE_URI'))

db_session = scoped_session(sessionmaker(bind=engine))


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    contact_phone = Column(String(100))
    contact_phone_normalized = Column(String(100), index=True)
