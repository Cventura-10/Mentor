from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/user')
def user():
    return 'User Page'