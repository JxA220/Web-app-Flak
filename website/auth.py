from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# CRIANDO ROUT PARA AUTH
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # VERIFICANDO SE O USUÁRIO EXISTE NA BASE DE DADOS
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        
        # CONFERINDO INFORMAÇÕES
        if user:
            if check_password_hash(user.password, password):
                flash('Sua sessão foi iniciada com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente', category='error')
        else:
            flash('O usuário não existe. Cadastre-se para acessar.', category='error')
    
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password-confirmation')

        # VERIFICANDO SE O USUÁRIO NÃO EXISTE
        user = User.query.filter_by(email=email).first()
        if user:
            flash('O usuário já existe. Faça login para entrar.', category='error')

        if len(password) < 4:
            flash('A senha deve ter mais de 4 caracteres', category='error')
        elif len(firstname) < 2:
            flash('O nome deve ter pelo menos 2 caracteres', category='error')
        elif password != password_confirmation:
            flash('As senhas não são iguais', category='error')
        else:
            # ADICIONANDO O NOVO USUÁRIO NA BASE DE DADOS
            new_user = User(email=email, first_name=firstname, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Sua conta foi criada com sucesso!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user)