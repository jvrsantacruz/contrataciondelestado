#-*- coding: utf-8 -*-

import logging
from functools import partial

from dateutil.parser import parse as parse_date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, Integer, Unicode, DateTime, Float, ForeignKey, create_engine


Base = declarative_base()
logger = logging.getLogger('models')


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer(), primary_key=True)
    nif = Column(Unicode(), unique=True)
    name = Column(Unicode())
    uri = Column(Unicode())

    @staticmethod
    def get_by_id(session, id):
        return session.query(Party).get(id)

    @staticmethod
    def get_by_nif(session, nif):
        return session.query(Party).filter_by(nif=nif).first()

    @staticmethod
    def get_or_create(session, party):
        return Party.get_by_nif(session, party['nif']) or Party(**party)

    @staticmethod
    def contractors(session):
        return session.query(Party).join(Licitation,
            Licitation.contractor_id == Party.id)

    @staticmethod
    def contracteds(session):
        return session.query(Party).join(Licitation,
            Licitation.contracted_id == Party.id)

    def to_dict(self):
        return {
            'id': self.id,
            'nif': self.nif,
            'name': self.name,
            'uri': self.uri
        }


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
                              backref='licitations',
                              primaryjoin="Licitation.contractor_id==Party.id")

    contracted_id = Column(Integer(), ForeignKey('parties.id'))
    contracted = relationship("Party",
                              backref='licitations',
                              primaryjoin="Licitation.contracted_id==Party.id")

    @staticmethod
    def count(session):
        return session.query(Licitation).count()

    @staticmethod
    def get_by_uuid(session, uuid):
        return session.query(Licitation).filter_by(uuid=uuid).first()

    @staticmethod
    def exists(session, uuid):
        by_uuid = session.query(Licitation).filter_by(uuid=uuid)
        return session.query(by_uuid.exists()).scalar()

    @staticmethod
    def create(session, data):
        if Licitation.exists(session, data.get('uuid')):
            return False

        try:
            data['issued_at'] = parse_date(data['issued_at'])
            data['awarded_at'] = parse_date(data['awarded_at'])
            data['contractor'] = Party.get_or_create(session, data['contractor'])
            data['contracted'] = Party.get_or_create(session, data['contracted'])

            licitation = Licitation(**data)
            session.add(licitation)
            session.commit()

            return licitation
        except Exception as error:
            logger.error(error)
            session.rollback()
        else:
            return True

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'file': self.file,
            'result_code': self.result_code,
            'uri': self.uri,
            'title': self.title,
            'amount': self.amount,
            'payable_amount': self.payable_amount,
            'issued_at': self.issued_at.isoformat('T')
            if self.issued_at is not None else None,
            'awarded_at': self.awarded_at.isoformat('T')
            if self.issued_at is not None else None,
            'contractor': self.contractor.to_dict()
            if self.contractor is not None else None,
            'contracted': self.contracted.to_dict()
            if self.contractor is not None else None,
        }


def get_session(database):
    engine = create_engine('sqlite:///' + database)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()


def get_scoped_session(database):
    return scoped_session(partial(get_session, database))
