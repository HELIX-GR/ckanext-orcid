import ckan.authz as authz

def orcid_callback_auth(context, data):
    if not authz.auth_is_loggedin_user():
           return {'success': False,
                'msg': _('Not authorized to see this page')}
    return

def orcid_authorize_auth(context, username):
    if not authz.auth_is_loggedin_user():
           return {'success': False,
                'msg': _('Not authorized to see this page')}
    return