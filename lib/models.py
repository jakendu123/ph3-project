from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime



engine = create_engine('sqlite:///lib/db/donations.db')
Base = declarative_base()

class Donor(Base):
    __tablename__ = 'donors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    donations = relationship("Donation", back_populates="donor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Donor(id={self.id}, name={self.name})>"

    def save(self):
        from seed import session
        session.add(self)
        session.commit()

    def delete(self):
        from seed import session
        session.delete(self)
        session.commit()

    @classmethod
    def get_by_id(cls, donor_id):
        from seed import session
        return session.query(cls).get(donor_id)

    @classmethod
    def get_all(cls):
        from seed import session
        return session.query(cls).all()

    @classmethod
    def get_by_email(cls, email):
        from seed import session
        return session.query(cls).filter(cls.email == email).first()

    @property
    def total_donated(self):
        return sum(d.amount for d in self.donations)

    @property
    def supported_causes(self):
        return list({d.cause for d in self.donations})


class Cause(Base):
    __tablename__ = 'causes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    goal = Column(Float)

    donations = relationship("Donation", back_populates="cause", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cause(id={self.id}, name={self.name})>"

    def save(self):
        from seed import session
        session.add(self)
        session.commit()

    def delete(self):
        from seed import session
        session.delete(self)
        session.commit()

    @classmethod
    def get_by_id(cls, cause_id):
        from seed import session
        return session.query(cls).get(cause_id)

    @classmethod
    def get_all(cls):
        from seed import session
        return session.query(cls).all()

    @property
    def amount_raised(self):
        return sum(d.amount for d in self.donations)

    @property
    def progress_percentage(self):
        if self.goal:
            return (self.amount_raised / self.goal) * 100
        return 0


class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.now)

    donor_id = Column(Integer, ForeignKey('donors.id'))
    cause_id = Column(Integer, ForeignKey('causes.id'))

    donor = relationship("Donor", back_populates="donations")
    cause = relationship("Cause", back_populates="donations")

    def __repr__(self):
        return f"<Donation(amount={self.amount}, donor_id={self.donor_id}, cause_id={self.cause_id})>"

    def save(self):
        from seed import session
        session.add(self)
        session.commit()

    def delete(self):
        from seed import session
        session.delete(self)
        session.commit()

    @classmethod
    def get_by_id(cls, donation_id):
        from seed import session
        return session.query(cls).get(donation_id)

    @classmethod
    def get_all(cls):
        from seed import session
        return session.query(cls).all()

Base.metadata.create_all(engine)
