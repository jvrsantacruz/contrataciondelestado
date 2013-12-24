# -*- coding: utf-8 -*-

import os
import zlib
import logging

from simplekv.db.sql import SQLAlchemyStore
from sqlalchemy import create_engine, MetaData


logger = logging.getLogger('store')


class Store(SQLAlchemyStore):
    """Specialized store over SQL for compressed unicode values"""

    def __init__(self, database, table='kvstore'):
        logger.info('Connecting store to "%s"', database)
        engine, metadata = self._create_database(database)
        super(Store, self).__init__(engine, metadata, table)
        self._create_database_schema(database, metadata)

    def _create_database(self, database):
        engine = create_engine('sqlite:///' + database)
        metadata = MetaData(bind=engine)
        return engine, metadata

    def _create_database_schema(self, database, metadata):
        if not os.path.exists(database):
            logger.info('Creating tables')
            metadata.create_all()

    def clean(self, key):
        return key.replace('/', '').replace(':', '')

    def decompress(self, value):
        if value is not None:
            return zlib.decompress(value).decode('utf-8')

    def compress(self, value):
        if value is not None:
            return zlib.compress(value.encode('utf-8'))

    def get(self, key):
        key = self.clean(key)
        value = super(Store, self).get(key)
        return self.decompress(value)

    def put(self, key, value):
        key = self.clean(key)
        value = self.compress(value)
        return super(Store, self).put(key, value)

    def delete(self, key):
        key = self.clean(key)
        return super(Store, self).delete(key)

    def iteritems(self):
        for key in self.iter_keys():
            yield key, self.get(key)

    def __iter__(self):
        return self.iter_keys()

    def __len__(self):
        return sum(1 for i in self.iter_keys())

    def __contains__(self, key):
        return super(Store, self).__contains__(self.clean(key))
