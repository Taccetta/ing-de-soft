from user import User
from flask import Flask, render_template, request, redirect, url_for, flash
from typing import Optional

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  

users = []


class Registry:
    _instance = None
    #single
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Registry, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def create_user(data) -> Optional[User]:
        # Validation
        if not all([data.get('username'), data.get('email'), data.get('password'), data.get('confirm_password'), data.get('terms')]):
            return None

        # Email validation
        if '@' not in data.get('email', '') or len(data.get('password', '')) < 6:
            return None

        # Password match validation
        if data.get('password') != data.get('confirm_password'):
            return None

        # Username uniqueness validation
        if any(user.username == data.get('username') for user in users):
            return None

        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            terms_accepted=True
        )
        users.append(user)
        return user

    @staticmethod
    def register_post(request):
        # datos del formulario
        user_data = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm_password'),
            'terms': request.form.get('terms') == 'on'
        }

        # Validacion y creacion
        user = Registry.create_user(user_data)

        if user:
            # curso normal
            flash('Registration successful!', 'success')
            # Redireccion
            return redirect(url_for('register_post'))
        else:
            # Error
            if not all([user_data.get('username'), user_data.get('email'), user_data.get('password'), user_data.get('confirm_password'), user_data.get('terms')]):
                flash('All fields are required.', 'error')
            elif '@' not in user_data.get('email', '') or len(user_data.get('password', '')) < 6:
                flash('Invalid email or password. Password must be at least 6 characters long.', 'error')
            elif user_data.get('password') != user_data.get('confirm_password'):
                flash('Passwords do not match.', 'error')
            elif any(user.username == user_data.get('username') for user in users):
                flash('User already exists. Please choose a different username.', 'error')
            return redirect(url_for('show_registration_form'))


#endpoints
@app.route('/')
def show_registration_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])#
def register_post():
    return Registry.register_post(request)

@app.route('/register')
def register_get():
    return render_template('register.html')

@app.route('/users')
def show_users():
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)