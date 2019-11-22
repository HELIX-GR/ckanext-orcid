import logging
import urlparse
import urllib
import json
import random
import time
import requests
import flask
from flask import Response
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
from ckan.common import _, c, session

import ckanext.orcid.model as ext_model

config = toolkit.config
request = toolkit.request
check_access = toolkit.check_access

logger = logging.getLogger(__name__)

authorize_url = config.get('ckanext.orcid.orcid_authorize_url');
token_url = config.get('ckanext.orcid.orcid_token_url');
userinfo_url = config.get('ckanext.orcid.orcid_userinfo_url');
client_id = config.get('ckanext.orcid.client_id');
client_secret = config.get('ckanext.orcid.client_secret');

ttl_for_state = 600; # in seconds

def _make_context(**opts):
    ctx = { 
        'model': model, 
        'session': model.Session, 
        'api_version': 3 
    }
    if opts:
        ctx.update(opts)
    return ctx

def _exchange_code_with_token(code):
    p = { 
        'code': code, 
        'grant_type': 'authorization_code', 
        'redirect_uri': toolkit.url_for('orcid.callback', _external=True), 
        'client_id': client_id, 
        'client_secret': client_secret,
    };
    r = requests.post(token_url, data=p, headers={'accept': 'application/json'});
    r.raise_for_status();
    return r.json();

def callback():
    logger.info('callback(): user=%s request.params=%s', c.userobj, request.params)
    try:
        check_access('orcid_callback', _make_context())
    except logic.NotAuthorized as ex:    
        return Response('Not authorized', status=403, content_type='text/plain');
    
    if not ('orcid' in session) or not ('state' in session['orcid']):
        return Response('No ORCID state in session!', status=400, content_type='text/plain');
    
    now = time.time();
    state, expires_on = session['orcid']['state'];
    if expires_on < now:
        return Response('The authorization request has expired!', status=400, content_type='text/plain');
    if request.params.get('state') != state:
        return Response('The request state is invalid', status=400, content_type='text/plain');
    
    authorization_code = request.params.get('code');
    r = _exchange_code_with_token(authorization_code);
    logger.info('Acquired token for user %s: orcid_identifier=%s access_token=%s refresh_token=%s', 
        c.user, r['orcid'], r['access_token'], r['refresh_token']);

    # TODO Assosicate user with the orcid id
    #ext_model.user_extra_create('username', 'orcid_id', 'value')
   
    # Redirect to return page
    
    return_url = None
    try:
        return_url = session.pop('return_to');
    except KeyError as ex:
        return_url = '/'
    
    logger.info("callback(): Redirecting to %s", return_url)
    return toolkit.redirect_to(return_url);

def authorize():
    try:
        check_access('orcid_authorize', _make_context())
    except logic.NotAuthorized as ex:
        return Response('Not authorized', status=403, content_type='text/plain')

    if not ('orcid' in session):
        session['orcid'] = {}

    state = '{0:x}'.format(random.getrandbits(40));
    session['orcid']['state'] = (state, int(time.time()) + ttl_for_state);

    # Build the authorization request for ORCID
    
    p = {
        'response_type': 'code',
        'client_id': client_id,
        'state': state,
        'redirect_uri': toolkit.url_for('orcid.callback', _external=True),
        'scope': '/authenticate',
    };
    redirect_url = urlparse.urljoin(authorize_url, '?' + urllib.urlencode(p))
    
    # Remember where to return (after callback)
    if 'return_to' in request.params: 
        session['return_to'] = request.params.get('return_to');
    
    # Redirect
    logger.info('authorize(): Redirecting to %s', redirect_url);
    return toolkit.redirect_to(redirect_url);
    
