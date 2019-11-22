import ckan.logic as logic
import ckan.model as model
from ckan.common import _, c
import ckanext.orcid.model as ext_model

NotFound = logic.NotFound
import logging
log1 = logging.getLogger(__name__)

def get_user_extra(username, key):

    user_extra = ext_model.UserExtra.get(username, key)
    if user_extra :
        return user_extra.value
    else:
        return None
