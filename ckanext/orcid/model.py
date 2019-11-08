import sqlalchemy.orm as orm
import sqlalchemy.types as types
import logging
import ckan.model as model
from ckan.model.domain_object import DomainObject
from ckan.model import meta, extension
import ckan.model.types as _types

from sqlalchemy.schema import Table, Column, ForeignKey, CreateTable, Index

mapper = orm.mapper
log = logging.getLogger(__name__)

user_extra_table = None

def setup():
    if user_extra_table is None:
        define_user_extra_table()
        log.debug('User extra table defined in memory')

    create_table()


class UserExtra(DomainObject):
    '''
    User extra information
    '''

    def __init__(self, username, key, value):
        self.username = username
        self.key = key
        self.value = value

    @classmethod
    def get(self, username, key):
        query = meta.Session.query(UserExtra)
        return query.filter_by(username=username, key=key).first()

    @classmethod
    def get_by_user(self, username):
        query = meta.Session.query(UserExtra).filter_by(username=username)
        result = query.all()
        return result

    @classmethod
    def get_by_key(self, key):
        query = meta.Session.query(UserExtra)
        return query.filter_by(key=key).all()

    @classmethod
    def check_exists(self):
        return user_extra_table.exists()


def define_user_extra_table():
    global user_extra_table
    user_extra_table = Table('user_extra', meta.metadata,
                             Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                             Column('username', types.UnicodeText, ForeignKey('user.name')),
                             Column('key', types.UnicodeText),
                             Column('value', types.UnicodeText),
                             )
    Index('username_key_idx', user_extra_table.c.username, user_extra_table.c.key, unique=True)
    mapper(UserExtra, user_extra_table, extension=[extension.PluginMapperExtension(), ])


def _create_extra(key, value):
    return UserExtra(key=unicode(key), value=value)


def create_table():
    '''
    Create user_extra table
    '''
    if model.user_table.exists() and not user_extra_table.exists():
        user_extra_table.create()
        log.debug('User extra table created')


def delete_table():
    '''
    Delete information from user_extra table
    '''
    print 'User Extra trying to delete table...'
    if user_extra_table.exists():
        print 'User Extra delete table...'
        user_extra_table.delete()
        log.debug('Validation Token table deleted')
        print 'DONE User Extra delete table...'


def drop_table():
    '''
    Drop user_extra table
    '''
    print 'User Extra trying to drop table...'
    if user_extra_table.exists():
        print 'User Extra drop table...'
        user_extra_table.drop()
        log.debug('Validation Token table dropped')
        print 'DONE User Extra drop table...'

def user_extra_create(username, key, value):
    user_extra = UserExtra.get(username=username, key=key)
    if user_extra:
        raise Exception('This user extra already exists')
    user_extra = UserExtra(username=username, key=key, value=value)
    model.Session.add(user_extra)
    model.Session.commit()

