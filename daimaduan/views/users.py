# coding: utf-8
from flask import Blueprint
from flask import request

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


@user_app.route('/oauth/<provider>', methods=['GET'])
def oauth_signin(provider):
    # oauth_service = oauth_services[provider]
    # redirect_uri = app.config['oauth.%s.callback_url' % provider]
    # scope = app.config['oauth.%s.scope' % provider]
    #
    # url = oauth_service.get_authorize_url(scope=scope,
    #                                       response_type='code',
    #                                       redirect_uri=redirect_uri)
    # redirect(url)
    pass


@user_app.route('/oauth/<provider>/callback', methods=['GET'])
# @jinja2_view('user/manage.html')
# @csrf_token
def oauth_callback(provider):
    # logger.info("Oauth callback for %s" % provider)
    # redirect_uri = app.config['oauth.%s.callback_url' % provider]
    # oauth_service = oauth_services[provider]
    # session = get_session(request)
    #
    # data = dict(code=request.params.get('code'),
    #             grant_type='authorization_code',
    #             redirect_uri=redirect_uri)
    #
    # if provider == 'google':
    #     oauth_session = oauth_service.get_auth_session(data=data, decoder=json.loads)
    #     user_info = oauth_session.get('userinfo').json()
    #     email = session['email'] = user_info['email']
    #     username = user_info['given_name']
    # elif provider == 'github':
    #     oauth_session = oauth_service.get_auth_session(data=data)
    #     user_info = oauth_session.get('user').json()
    #     email = session['email'] = user_info['email']
    #     username = user_info['login']
    #
    # access_token = oauth_session.access_token
    # user_info['id'] = str(user_info['id'])
    #
    # logger.info("%s oauth access token is: %s" % (provider, access_token))
    # logger.info("%s oauth user info is %s" % (provider, user_info))
    #
    # user = User.find_by_oauth(provider, user_info['id'])
    # if user:
    #     # TODO: 直接登录时更新 token.
    #     login.login_user(str(user.id))
    #     return redirect('/')
    # else:
    #     user = User.objects(email=email).first()
    #     if user:
    #         user_oauth = UserOauth(provider=provider, openid=user_info['id'], token=access_token)
    #         user_oauth.save()
    #         login.login_user(str(user.id))
    #         return redirect('/')
    #     else:
    #         return {'form': UserInfoForm(email=email, username=username), 'token': request.csrf_token}
    pass


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


@user_app.route('/signin', methods=['GET', 'POST'])
# @jinja2_view('user/signin.html')
# @csrf_token
def signin_get():
    if request.method == 'GET':
    # if request.user:
    #     redirect('/')
    # else:
    #     return {'form': SigninForm(), 'token': request.csrf_token}
        pass
    else:
        # session = get_session(request)
        #
        # form = SigninForm(request.POST)
        # if form.validate():
        #     login.login_user(str(form.user.id))
        #
        #     if 'oauth_provider' in session:
        #         user_bind_oauth(form.user, session)
        #
        #     redirect('/')
        # else:
        #     return locals()
        pass


@user_app.route('/signout', methods=['DELETE'])
def signout_delete():
    # login.logout_user()
    # request.environ.get('beaker.session').delete()
    pass


@user_app.route('/signup', methods=['GET', 'POST'])
# @jinja2_view('user/signup.html')
# @csrf_token
def signup_get():
    if request.method == 'GET':
    #     if request.user:
    #         redirect('/')
    #     else:
    #         return {'form': SignupForm(), 'token': request.csrf_token}
        pass
    else:
        # form = SignupForm(request.forms)
        # if form.validate():
        #     user = User()
        #     form.populate_obj(user)
        #     user.save()
        #     login.login_user(user.id)
        #     send_confirm_email(app.config, user.email)
        #     return redirect('/active_email')
        # return {'form': form, 'token': request.csrf_token}
        pass


@user_app.route('/lost_password', methods=['GET', 'POST'])
# @jinja2_view('user/lost_password.html')
def lost_password_get():
    if request.method == 'GET':
        # return {'form': EmailForm()}
        pass
    else:
        # form = EmailForm(request.forms)
        # if form.validate():
        #     user = User.objects(email=form.email.data).first()
        #     send_reset_password_email(app.config, user.email)
        #     return redirect('/reset_password_email_sent')
        # return {'form': form}
        pass


@user_app.route('/reset_password_email_sent', methods=['GET'])
# @jinja2_view('error.html')
def reset_password_email_sent():
    # return {'title': u"重置密码的邮件已经发出", 'message': u"重置密码的邮件已经发出, 请查收邮件并重置密码"}
    pass


@user_app.route('/reset_password/<token>', methods=['GET', 'POST'])
# @jinja2_view('user/reset_password.html')
def reset_password(token):
    if request.method == 'GET':
        # email = validate_token(app.config, token)
        # if email:
        #     user = User.objects(email=email).first()
        #     if user:
        #         return {'form': PasswordForm(), 'token': token}
        # abort(404)
        pass
    else:
        # email = validate_token(app.config, token)
        # if email:
        #     user = User.objects(email=email).first()
        #     if user:
        #         form = PasswordForm(request.forms)
        #         if form.validate():
        #             user.password = user.generate_password(form.password.data)
        #             user.save()
        #             redirect('/reset_password_success')
        #         return {'form': PasswordForm(), 'token': token}
        # abort(404)
        pass


@user_app.route('/reset_password_success', methods=['GET'])
# @jinja2_view('error.html')
def reset_password_success():
    # return {'title': u"重置密码成功", 'message': u"您的密码已经重置, 请重新登录"}
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


@user_app.route('/confirm/<token>', methods=['GET'])
# @jinja2_view('email/confirm.html')
def confirm_email(token):
    # email = validate_token(app.config, token)
    # if email:
    #     user = User.objects(email=email).first()
    #     if user:
    #         if (request.user is not None and user == request.user) or request.user is None:
    #             if user.is_email_confirmed:
    #                 return {'title': u"Email已经激活过了", 'message': u"对不起，您的email已经激活过了。"}
    #             else:
    #                 user.is_email_confirmed = True
    #                 user.email_confirmed_on = datetime.datetime.now()
    #                 user.save()
    #                 return {'title': u'Email已经激活', 'message': u'您的email已经激活，请点击登录查看最新代码段。'}
    # return {'title': u'Email验证链接错误', 'message': u'对不起，您的验证链接无效或者已经过期。'}
    pass


@user_app.route('/active_email', methods=['GET'])
# @csrf_token
# @jinja2_view('email/active.html')
def active_email():
    # return {'email': request.user.email, 'title': u'注册成功', 'token': request.csrf_token}
    pass


@user_app.route('/success_sendmail', methods=['GET'])
# @jinja2_view('email/confirm.html')
def sendmail_success():
    # return {'title': u"激活邮件发送成功", 'message': u"激活邮件发送成功, 请检查并激活您的账户。"}
    pass


@user_app.route('/sendmail', methods=['POST'])
# @csrf_protect
def send_mail_post():
    # form = EmailForm(request.forms)
    # if form.validate():
    #     user = User.objects(email=form.email.data).first()
    #     send_confirm_email(app.config, user.email)
    #     return redirect('/success_sendmail')
    # return {'form': form}
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
