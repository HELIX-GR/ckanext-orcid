from ckan.lib.base import BaseController, c, h,  response, abort 
from ckan.common import _
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
from pylons import config

import logging

request = toolkit.request
_check_access = toolkit.check_access

log = logging.getLogger(__name__)

import ckanext.orcid.model as ue_model

def _make_context(**opts):
    ctx = { 
        'model': model, 
        'session': model.Session, 
        'api_version': 3 
    }
    if opts:
        ctx.update(opts)
    return ctx

def callback():
    try:
        _check_access('callback', _make_context())
    except logic.NotAuthorized as ex:    
        return 'Not authorized to perform this action.'
    
    # assosicate user with the orcid id
    ue_model.user_extra_create('username', 'orcid_id', 'value')
    return

def authorize():
    log.debug('userobj: %s', c.userobj)
    try:
        _check_access('authorize', _make_context())
    except logic.NotAuthorized as ex:
        return 'Not authorized to perform this action.'

    #orcid_get_authorization_url()

    #redirect to orcid to handle authentication

    # get orcid url from config file
    #orcid_url = config.get('ckanext.orcid.orcid_base_url')
    return toolkit.redirect_to(orcid_url)


    