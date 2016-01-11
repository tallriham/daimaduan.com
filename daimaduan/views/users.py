# coding: utf-8
from flask import Blueprint

# from daimaduan.bootstrap import login
# from daimaduan.bootstrap import oauth_services
# from daimaduan.forms.email import EmailForm
# from daimaduan.forms.password import PasswordForm
# from daimaduan.forms.signin import SigninForm
# from daimaduan.forms.signup import SignupForm
# from daimaduan.forms.userinfo import UserInfoForm
# from daimaduan.models.tag import Tag
# from daimaduan.models.base import User
# from daimaduan.models.user_oauth import UserOauth
# from daimaduan.utils.commons import get_session
# from daimaduan.utils.email_confirmation import send_confirm_email
# from daimaduan.utils.email_confirmation import send_reset_password_email
# from daimaduan.utils.email_confirmation import validate_token
# from daimaduan.utils.oauth import user_bind_oauth
# from daimaduan.utils.pagination import get_page, paginate


user_app = Blueprint("user_app", __name__, template_folder="templates")

# Get user by username or raise 404 error.
# def get_user(username):
#     return User.objects.get_or_404(username=username)


@user_app.route('/user/manage', methods=['POST'])
# @jinja2_view('user/manage.html')
# @csrf_token
# @csrf_protect
def manage():
    # form = UserInfoForm(request.forms)
    # if form.validate():
    #     if request.user:
    #         request.user.username = form.username.data
    #         return redirect('/')
    #     else:
    #         user = User(email=form.email.data, username=form.username.data,
    #                     is_email_confirmed=True)
    #         user.save()
    #         login.login_user(str(user.id))
    #         session = get_session(request)
    #         if 'email' in session:
    #             del(session['email'])
    #         return redirect('/')
    # return {'form': form, 'token': request.csrf_token}
    pass


@user_app.route('/user/<username>', methods=['GET'])
# @jinja2_view('user/user.html')
def user_index(username):
    # page = get_page()
    # user = get_user(username)
    #
    # pastes = user.pastes.order_by('-updated_at')
    # if not (request.user and request.user == user):
    #     pastes = pastes(is_private=False)
    #
    # pastes, summary = paginate(pastes, page)
    #
    # return {'user': user,
    #         'pastes': pastes,
    #         'page_summary': summary,
    #         'tags': Tag.objects().order_by('-popularity')[:10]}
    pass


@user_app.route('/user/<username>/likes', methods=['GET'])
# @jinja2_view('user/likes.html')
def likes_get(username):
    # user = get_user(username)
    #
    # page = get_page()
    # likes = user.likes.order_by('-updated_at')
    # likes, summary = paginate(likes, page)
    #
    # return {'user': user,
    #         'likes': likes,
    #         'page_summary': summary,
    #         'tags': Tag.objects().order_by('-popularity')[:10]}
    pass


@user_app.route('/user/watch', methods=['POST'])
def watch_user():
    # user = User.objects(username=request.params.get('user')).first_or_404()
    # request.user.watched_users.append(user)
    # request.user.save()
    # return {'watchedStatus': request.user.is_watched(user)}
    pass


@user_app.route('/user/unwatch', methods=['POST'])
def unwatch_user():
    # user = User.objects(username=request.params.get('user')).first_or_404()
    # request.user.watched_users.remove(user)
    # request.user.save()
    # return {'watchedStatus': request.user.is_watched(user)}
    pass
