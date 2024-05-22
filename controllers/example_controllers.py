from flask import Blueprint, request
from services.example_services import login_user, logout_user, fetch_workers_by_boss, get_user_profile,add_worker, delete_alba, get_schedule

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    id = request.json.get('id')
    password = request.json.get('password')
    return login_user(id, password)

@bp.route('/logout')
def logout():
    return logout_user()


@bp.route('/workers', methods=['GET'])
def get_workers():
    bossno = request.args.get('bossno')
    return fetch_workers_by_boss(bossno)

@bp.route('/profile', methods=['GET'])
def profile():
    return get_user_profile(request)

@bp.route('/create', methods=['POST'])
def create():
    return add_worker()

@bp.route('/delete/<int:albano>', methods=['DELETE'])
def delete(albano):
    return delete_alba(albano)


@bp.route('/schedule/<int:bossno>', methods=['GET'])
def schedule(bossno):
    return get_schedule(bossno)