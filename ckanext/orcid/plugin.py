import logging
from flask import Blueprint

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.orcid.logic.auth as ext_auth
import ckanext.orcid.controllers.user as user_controller
import ckanext.orcid.helpers as ext_helpers
import ckanext.orcid.model as ext_model
from ckanext.orcid.orcid_api import check_if_access_token_is_valid
from ckanext.orcid.repo import get_access_token_for_user, delete_orcid_for_user 

logger = logging.getLogger(__name__);


class OrcidPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    plugins.implements(plugins.IAuthenticator, inherit=True) # only to listen for logout events

    _check_if_access_token_is_revoked = False

    #
    # IConfigurable
    #

    def configure(self, config):
        # Setup database table(s)
        ext_model.setup()
        
        # Set class-level configuration
        self._check_if_access_token_is_revoked = toolkit.asbool(
            config.get('ckanext.orcid.check_if_access_token_is_revoked', 'False'));

    #
    # ITemplateHelpers    
    #

    def get_helpers(self):
        return {
            'orcid_user_info': ext_helpers.get_orcid_user_info,
        };

    # 
    # IAuthFunctions 
    #
    
    def get_auth_functions(self):
        '''Define new authorization checks or replace existing ones'''
        funcs = {
            'orcid_callback': ext_auth.orcid_callback_auth,
            'orcid_authorize': ext_auth.orcid_authorize_auth,
        }
        return funcs

    #
    # IBlueprint 
    #

    def get_blueprint(self):
        '''Return a Flask Blueprint object to be registered by the app.'''

        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        # Add plugin url rules to Blueprint object
        rules = [
            (u'/orcid/callback', u'callback', user_controller.callback),
            (u'/orcid/authorize', u'authorize', user_controller.authorize)
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    #
    # IAuthenticator
    #

    def logout(self):
        if self._check_if_access_token_is_revoked:
            user_id = toolkit.c.userobj.id;
            access_token = get_access_token_for_user(user_id);
            if access_token and not check_if_access_token_is_valid(access_token):
                logger.info("The access token %s (for user %s) is no longer valid: "
                    "Removing association to ORCID", access_token, user_id);
                delete_orcid_for_user(user_id);
        pass

