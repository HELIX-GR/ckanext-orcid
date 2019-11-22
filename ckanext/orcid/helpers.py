import logging
import ckan.logic as logic
import ckan.model as model
from ckan.common import _, c
import ckan.plugins.toolkit as toolkit
import ckanext.orcid.model as ext_model

logger = logging.getLogger(__name__)

config = toolkit.config;

orcid_host = config.get('ckanext.orcid.orcid_host');

def get_orcid_user_info(user_id):
    orcid_user = model.Session.query(ext_model.OrcidUser).filter_by(user_id=user_id).one_or_none();
    if orcid_user:
        return {
            'id': orcid_user.orcid_identifier,
            'url': 'http://{0:s}/{1:s}'.format(orcid_host, orcid_user.orcid_identifier),
        };
    else:
        return None
