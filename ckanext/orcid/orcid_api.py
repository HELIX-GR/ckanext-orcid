import logging
import urlparse
import requests
import ckan.plugins.toolkit as toolkit

logger = logging.getLogger(__name__)

config = toolkit.config

api_url = "https://{0:s}".format(config.get("ckanext.orcid.orcid_api_host"));
userinfo_url = config.get('ckanext.orcid.orcid_userinfo_url');


def get_user_info(access_token):
    '''Get basic user info (part of OIDC standard)
    '''
    r = requests.get(userinfo_url, headers={
        'accept': 'application/json',
        'authorization': 'Bearer {0:s}'.format(access_token),
    });
    r.raise_for_status();
    return r.json();

def get_person_info(orcid_identifier, access_token):
    '''Get person info using ORCID member API
    '''
    url = urlparse.urljoin(api_url, "/v2.0/{0:s}/person".format(orcid_identifier));
    r = requests.get(url, headers={
        'accept': 'application/json',
        'authorization': 'Bearer {0:s}'.format(access_token),
    });
    r.raise_for_status();
    return r.json();

def check_if_access_token_is_valid(access_token):
    try:
        u = get_user_info(access_token);
    except requests.HTTPError as ex:
        status_code = ex.response.status_code;
        # Note: Using an invalid (revoked or expired) token will return "403 Forbidden"
        logger.info("check_if_access_token_is_valid(access_token=%s): %s", access_token, ex);
        if status_code < 400 or status_code >= 500:
            logger.warning("check_if_access_token_is_valid(access_token=%s): "
                "Failed with an unexpected status: %s", access_token, ex);
        return False;
    return True;
