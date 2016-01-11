from flask import Blueprint, flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user
from flask_login import logout_user

from daimaduan.bootstrap import login_manager
from daimaduan.forms.signin import SigninForm
from daimaduan.forms.signup import SignupForm
from daimaduan.models.base import Code
from daimaduan.models.base import Paste
from daimaduan.models.base import User
from daimaduan.models.tag import Tag
from daimaduan.utils.pagination import get_page
from daimaduan.utils.pagination import paginate


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get_or_404(id=user_id)


site_app = Blueprint("site_app", __name__, template_folder="templates")


@site_app.route('/', methods=['GET'])
def index():
    page = get_page()
    pastes = Paste.objects(is_private=False).order_by('-updated_at')
    pastes, summary = paginate(pastes, page)

    return render_template('index.html',
                           pastes=pastes,
                           page_summary=summary,
                           tags=Tag.objects().order_by('-popularity')[:10])


@site_app.route('/status', methods=['GET'])
def status():
    return {'pastes_count': Paste.objects().count(),
            'codes_count': Code.objects().count(),
            'users_count': User.objects().count()}


@site_app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if request.method == 'GET':
        return render_template('user/signin.html',
                               form=SigninForm())
    else:
        if form.validate_on_submit():
            user = User.objects.get_or_404(email=form.email.data)
            login_user(user)

        flash('Logged in successfully.')

        return redirect(url_for('site_app.index'))


@site_app.route('/signout', methods=['DELETE'])
def signout_delete():
    logout_user()
    return redirect(url_for('site_app.index'))


@site_app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('user/signup.html',
                               form=form)
    else:
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            user.save()
            login_user(user)
            # send_confirm_email(app.config, user.email)
            return redirect(url_for('site_app.index'))
        return render_template('user/signup.html',
                               form=form)
