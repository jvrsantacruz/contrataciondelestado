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


def create_licitation(session, data):
    try:
        if licitation_exists(session, data['uuid']):
            return False

        data['contractor'] = get_or_create_party(session, data['contractor'])
        data['contracted'] = get_or_create_party(session, data['contracted'])

        session.add(Licitation(**data))
        session.commit()
    except Exception as error:
        session.rollback()
        print error
    else:
        return True


def get_or_create_party(session, party):
    return (session.query(Party).filter_by(nif=party['nif']).first()
            or Party(**party))


def licitation_exists(session, uuid):
    by_uuid = session.query(Licitation).filter_by(uuid=uuid)
    return session.query(by_uuid.exists()).scalar()


class Licitation(Base):
    __tablename__ = "licitations"

    id = Column(Integer(), primary_key=True)
    uuid = Column(Unicode(), unique=True)
    file = Column(Unicode())

    type = Column(Unicode())
    subtype = Column(Unicode())
    result_code = Column(Unicode())

    uri = Column(Unicode())
    title = Column(Unicode())

    amount = Column(Float())
    payable_amount = Column(Float())

    budget_amount = Column(Float())
    budget_payable_amount = Column(Float())

    issued_at = Column(DateTime())
    awarded_at = Column(DateTime())

    contractor_id = Column(Integer(), ForeignKey('parties.id'))
    contractor = relationship("Party",
                              primaryjoin="Licitation.contractor_id==Party.id")

    contracted_id = Column(Integer(), ForeignKey('parties.id'))
    contracted = relationship("Party",
                              primaryjoin="Licitation.contracted_id==Party.id")


class Party(Base):
    __tablename__ = "parties"
    __mapper_args__ = {'polymorphic_identity': 'party'}

    id = Column(Integer(), primary_key=True)
    nif = Column(Unicode(), unique=True)
    name = Column(Unicode())
    uri = Column(Unicode())


if __name__ == "__main__":
    get_session()
