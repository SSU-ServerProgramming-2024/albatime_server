from toy.models.example_models import db, User, Boss
from flask import session, jsonify
from sqlalchemy.exc import SQLAlchemyError

def login_user(id, password):
    try:
        user = User.query.filter_by(id=id).first()
        if user and user.password == password:
            session['user_id'] = user.user_id
            boss_info = Boss.query.filter_by(user_id=user.user_id).first()
            bossno = boss_info.bossno if boss_info else None
            return jsonify({
                'message': 'Login successful',
                'isemployer': user.isemployer,
                'bossno': bossno,
                'user_id': user.user_id
            }), 200
        else:
            return jsonify({'message': 'Invalid login credentials'}), 401
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

def logout_user():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

