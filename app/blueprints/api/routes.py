from . import api
from app import db
from app.models import Contact
from flask import request
from .auth import basic_auth, token_auth

@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': auth_user,
            'token_exp': auth_user.token_expiration}

