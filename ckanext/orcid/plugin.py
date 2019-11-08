import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import model as ue_model
from flask import Blueprint

import ckanext.orcid.logic.auth as ext_auth
import ckanext.orcid.controllers.user as user_controller
import ckanext.orcid.helpers as h_orcid


class OrcidPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions, inherit=True)


    # IConfigurable
    def configure(self, config):
        # setup extra user metadata table
        ue_model.setup()

    # ITemplateHelpers    
    def get_helpers(self):
        return {'get_user_extra': h_orcid.get_user_extra}

     # IAuthFunctions 
    
    def get_auth_functions(self):
        '''Define new authorization checks or replace existing ones
        '''
        funcs = {
            'callback': ext_auth.orcid_callback_auth,
            'authorize': ext_auth.orcid_authorize_auth,
        }
        return funcs

    # IBlueprint 

    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''

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