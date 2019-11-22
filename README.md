# ckanext-orcid

A ckan extension to associate a user with an ORCID identity.

## Setup

This extension provides a single CKAN plugin: `orcid`.

Edit CKAN configuration and add plugin-specific settings. For example:

```
## ckanext-orcid settings

ckanext.orcid.orcid_host = sandbox.orcid.org
ckanext.orcid.orcid_authorize_url = https://sandbox.orcid.org/oauth/authorize
ckanext.orcid.orcid_token_url = https://sandbox.orcid.org/oauth/token
ckanext.orcid.orcid_userinfo_url = https://sandbox.orcid.org/oauth/userinfo
ckanext.orcid.client_id = APP-123
ckanext.orcid.client_secret = secret
```
