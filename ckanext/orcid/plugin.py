from flask import Blueprint

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.orcid.logic.auth as ext_auth
import ckanext.orcid.controllers.user as user_controller
import ckanext.orcid.helpers as ext_helpers
import ckanext.orcid.model as ext_model


class OrcidPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions, inherit=True)

    # IConfigurable

    def configure(self, config):
        # Setup database table(s)
        ext_model.setup()

    # ITemplateHelpers    
    
    def get_helpers(self):
        return {
            'orcid_user_info': ext_helpers.get_orcid_user_info,
        };

     # IAuthFunctions 
    
    def get_auth_functions(self):
        '''Define new authorization checks or replace existing ones'''
        funcs = {
            'orcid_callback': ext_auth.orcid_callback_auth,
            'orcid_authorize': ext_auth.orcid_authorize_auth,
        }
        return funcs

    # IBlueprint 

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
