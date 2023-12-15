from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from model.ModelBase import Base


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    record_creation_time = Column(DateTime(timezone=True), default=func.now())
    record_update_time = Column(DateTime(timezone=True), default=func.now())

    product = relationship("Product", backref="notifications")
