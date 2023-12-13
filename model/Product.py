from sqlalchemy import Column, Integer, String, Text, Double, DateTime, Enum, func

from constant.Enums import Currency, Platform
from model.ModelBase import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    platform = Column(Enum(Platform))
    title = Column(String(1024))
    currency = Column(Enum(Currency))
    price = Column(Double())
    url = Column(Text())
    posting_time = Column(DateTime(timezone=True))
    record_creation_time = Column(DateTime(timezone=True), default=func.now())
    record_update_time = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.title!r}, price={self.price!r}, posting_time={self.posting_time!r})"