from sqlalchemy import Column, Integer, String, Text, Double, DateTime, Enum, func

from constant.Enums import Currency, Platform
from model.ModelBase import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    platform = Column(Enum(Platform), index=True)
    search_keyword = Column(String(1024), index=True)
    product_unique_id = Column(String(1024), index=True)
    title = Column(String(1024))
    currency = Column(Enum(Currency))
    price = Column(Double(), index=True)
    url = Column(Text())
    approx_posting_time = Column(DateTime(timezone=True), index=True)
    record_creation_time = Column(DateTime(timezone=True), default=func.now())
    record_update_time = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f'Product(platform={self.platform!r}, search_keyword={self.search_keyword!r}, product_unique_id={self.product_unique_id!r}, ' \
               f'currency={self.currency!r}, price={self.price!r}, approx_posting_time={self.approx_posting_time.strftime("%Y-%m-%d %H:%M:%S")!r})'
