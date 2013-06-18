#!/usr/bin/env python
#-*- coding: utf-8 -*-


from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, DateTime, Float, ForeignKey, create_engine


Base = declarative_base()


def get_session():
    engine = create_engine('sqlite:///db.sqlite')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()


class Licitation(Base):
    __tablename__ = "licitations"

    id = Column(Integer(), primary_key=True)
    uuid = Column(Unicode(), unique=True)
    file = Column(Unicode())

    type = Column(Unicode())
    subtype = Column(Unicode())

    uri = Column(Unicode())
    title = Column(Unicode())

    amount = Column(Float())
    payable_amount = Column(Float())

    budget_amount = Column(Float())
    budget_payable_amount = Column(Float())

    issued_at = Column(DateTime())
    awarded_at = Column(DateTime())

    contractor_id = Column(Integer(), ForeignKey('contractors.id'))
    contractor = relationship("Contractor")

    contracted_id = Column(Integer(), ForeignKey('contracted.id'))
    contracted = relationship("Contracted")


class Party(Base):
    __tablename__ = "parties"
    __mapper_args__ = {'polymorphic_identity': 'party'}

    id = Column(Unicode(), primary_key=True)
    nif = Column(Unicode(), unique=True)
    name = Column(Unicode())


class Contractor(Party):
    __tablename__ = "contractors"
    __mapper_args__ = {'polymorphic_identity': 'contractor'}

    id = Column(Integer(), ForeignKey(Party.id), primary_key=True)


class Contracted(Party):
    __tablename__ = "contracted"
    __mapper_args__ = {'polymorphic_identity': 'contractor'}

    id = Column(Integer(), ForeignKey(Party.id), primary_key=True)


if __name__ == "__main__":
    get_session()
