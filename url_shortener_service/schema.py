from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class URLShortener(Base):
    __tablename__ = 'url_shorteners'
    id = Column(Integer, primary_key=True)
    long_url = Column(String, unique=True, nullable=False)
    short_url = Column(String, unique=True, nullable=False)