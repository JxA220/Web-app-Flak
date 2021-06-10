from flask import Flask
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

# CRIANDO BASE DE DADOS
db = SQLAlchemy()
DB_NAME = 'database.db'

# INICIANDO FLASK E CRIANDO APP
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'JxAGamer101'
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views ,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Task  

    database_creation(app)

    # VERIFICANDO SE O USUÁRIO ESTÁ LOGADO
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# FUNÇÃO PARA CRIAR A BASE DE DADOS
def database_creation(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)