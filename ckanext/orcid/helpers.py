import logging
import ckan.plugins.toolkit as toolkit

from ckanext.orcid.repo import get_orcid_for_user

logger = logging.getLogger(__name__)

config = toolkit.config;

orcid_host = config.get('ckanext.orcid.orcid_host');

def get_orcid_user_info(user_id):
    orcid_user = get_orcid_for_user(user_id);
    if orcid_user:
        return {
            'id': orcid_user.orcid_identifier,
            'url': 'http://{0:s}/{1:s}'.format(orcid_host, orcid_user.orcid_identifier),
        };
    else:
        return None
