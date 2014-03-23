# Standard libs
import urlparse

# Third party libs
import flask
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user

# Our libs
from fitactivists.models import User

blueprint = Blueprint('root',
                      __name__,
                      static_folder='../static',
                      template_folder='../../client/templates')

@blueprint.route('/')
@login_required
def index():
    return render_template('index.html')

@blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@blueprint.route('/login')
def login():
    if current_user.is_active():
        return redirect(url_for('root.index'))
    return render_template('login.html')

@blueprint.route('/do-login', methods=['post'])
def do_login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    user = User.get_by_id(username)

    if not user:
        flash('The username or password you entered is incorrect.')
        return redirect(url_for('root.login'))

    is_valid_password = user.verify_password(password)

    if not is_valid_password:
        flash('The username or password you entered is incorrect.')
        return redirect(url_for('root.login'))

    login_user(user)

    redirect_url = url_for('root.index')
    referrer = request.headers.get('Referer', '')
    if referrer:
        url = urlparse.urlparse(referrer)
        params = urlparse.parse_qs(url.query)
        next_url_list = params.get('next', [])
        if next_url_list:
            redirect_url = next_url_list[0]
    return redirect(redirect_url)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('root.login'))

@blueprint.route('/do-signup', methods=['post'])
def do_signup():
    user_data = {
        'email':         request.form.get('email', ''),
        'password':      request.form.get('password', ''),
        'first_name':    request.form.get('first_name', ''),
        'last_name':     request.form.get('last_name', ''),
        'date_of_birth': request.form.get('date_of_birth', ''),
        'company_name':  request.form.get('company_name', ''),
        'team_name':     request.form.get('team_name', ''),
    }

    user = User(user_data)

    if not user.is_valid():
        return redirect(url_for('root.signup'))

    user.create()

    return redirect(url_for('root.index'))

