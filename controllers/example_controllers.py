from flask import Blueprint, request
from server.services.example_services import login_user, logout_user

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    id = request.json.get('id')
    password = request.json.get('password')
    return login_user(id, password)

@bp.route('/logout')
def logout():
    return logout_user()
