from flask import Flask
from models.example_models import db
from controllers.example_controllers import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/albatime_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = "123"

    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

if __name__ == '__main__':
    app = create_app()
    db.create_all(app)
    app.run(host='0.0.0.0',port="5000",debug=False)
