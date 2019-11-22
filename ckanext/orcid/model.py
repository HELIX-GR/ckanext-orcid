import sqlalchemy.orm as orm
import sqlalchemy.types as types
import logging
import ckan.model as model
from ckan.model.domain_object import DomainObject
from ckan.model import meta, extension

from sqlalchemy.schema import Table, Column, ForeignKey, CreateTable, Index

logger = logging.getLogger(__name__)

orcid_user_table = None

def setup():
    '''Define and create table (if needed)'''
    if orcid_user_table is None:
        define_table()
        logger.debug('Table `orcid_user` is defined in ORM mapper')
    create_table()

class OrcidUser(DomainObject):
    '''The ORM entity that represents a user's ORCID association'''

    def __init__(self, user_id, orcid_identifier):
        self.user_id = user_id
        self.orcid_identifier = orcid_identifier

def define_table():
    global orcid_user_table;
    orcid_user_table = Table('orcid_user', meta.metadata,
        Column('user_id', types.UnicodeText, ForeignKey('user.id'), primary_key=True),
        Column('orcid_identifier', types.String, unique=True, nullable=False),
        Column('access_token', types.String, nullable=False), 
        Column('refresh_token', types.String), 
        Column('associated_at', types.BigInteger, nullable=False), # association timestamp
        Column('expires_at', types.BigInteger, nullable=False), # expiry timestamp for the access token
    );
    orm.mapper(OrcidUser, orcid_user_table, extension=[extension.PluginMapperExtension(), ]);

def create_table():
    '''Create orcid_user table'''
    if model.user_table.exists() and not orcid_user_table.exists():
        orcid_user_table.create()
        logger.info('Table `orcid_user` created')

def truncate_table():
    '''Truncate orcid_user table'''
    if orcid_user_table.exists():
        orcid_user_table.delete()
        logger.info('Table `orcid_user` is truncated')

def drop_table():
    '''Drop orcid_user table'''
    if orcid_user_table.exists():
        orcid_user_table.drop()
        logger.info('Table `orcid_user` is dropped')

