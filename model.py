from sqlalchemy import String, Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

import settings

Base = declarative_base()


class LogModel(Base):
    __tablename__ = settings.DB_TABLE_NAME

    id = Column(Integer, primary_key=True)
    request_ip = Column(String)
    request_date = Column(DateTime)
    request_url = Column(String)
    response_code = Column(Integer)
    response_size = Column(Integer)

    def __init__(self, ip, date, url, code, size):
        self.request_ip = ip
        self.request_date = date
        self.request_url = url
        self.response_code = code
        self.response_size = size
