from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey

from base import Base


class MystromResult(Base):

    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)

    device_id = Column(Integer, ForeignKey('devices.id'))

    power = Column(Float)
    ws = Column(Float)
    relay = Column(Integer)
    temperature = Column(Float)
    date = Column(DateTime(timezone=True), default=datetime.now)
    source = Column(Integer, default=1)

    # Lets us print out a user object conveniently.
    def __repr__(self):
        return "<Result(deivce_id='%s', power='%s', ws='%s', relay='%s', " \
               "temperature='%s', date='%s', source='%s')>" % (
            self.device_id, self.power, self.ws, self.relay, self.temperature,
            self.date, self.source)
