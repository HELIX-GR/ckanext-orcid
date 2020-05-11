import logging
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckanext.orcid.model as ext_model

logger = logging.getLogger(__name__)

config = toolkit.config;

orcid_host = config.get('ckanext.orcid.orcid_host');

def save_orcid_for_user(user_id, orcid_identifier, access_token, refresh_token, associated_at, expires_at):
    orcid_user = model.Session.query(ext_model.OrcidUser).filter_by(user_id=user_id).one_or_none();
    if orcid_user:
        # Update record
        orcid_user.orcid_identifier = orcid_identifier; # Q: is this supposed to be updated?
    else:
        # Add record
        orcid_user = ext_model.OrcidUser(user_id, orcid_identifier);
        model.Session.add(orcid_user);
    
    orcid_user.access_token = access_token;
    orcid_user.refresh_token = refresh_token;
    orcid_user.associated_at = associated_at;
    orcid_user.expires_at = expires_at;
    
    model.Session.commit();

def get_orcid_for_user(user_id):
    q = model.Session.query(ext_model.OrcidUser).filter_by(user_id=user_id);
    return q.one_or_none(); 

def get_access_token_for_user(user_id):
    r = get_orcid_for_user(user_id);
    return None if r is None else r.access_token;

def delete_orcid_for_user(user_id):
    q = model.Session.query(ext_model.OrcidUser).filter_by(user_id=user_id);
    q.delete();
    model.Session.commit();
    
