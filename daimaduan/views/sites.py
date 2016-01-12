# coding: utf-8
import re

from flask import abort
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
from daimaduan.models import LoginManagerUser
from daimaduan.models.base import Code
from daimaduan.models.base import Paste
from daimaduan.models.base import User
from daimaduan.models.tag import Tag
from daimaduan.utils.pagination import get_page
from daimaduan.utils.pagination import paginate
from daimaduan.views.pastes import ITEMS_PER_PAGE


@login_manager.user_loader
def load_user(user_id):
    user = User.objects.get_or_404(id=user_id)
    return LoginManagerUser(user)


site_app = Blueprint("site_app", __name__, template_folder="templates")


@site_app.route('/', methods=['GET'])
def index():
    page = get_page()
    pagination = Paste.objects(is_private=False).order_by('-updated_at').paginate(page=page, per_page=20)

    return render_template('index.html',
                           pagination=pagination,
                           tags=Tag.objects().order_by('-popularity')[:10])


@site_app.route('/tags', methods=['GET'])
def tags():
    return render_template('tags/index.html',
                           tags=Tag.objects().order_by('-popularity'))


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
            user_mixin = LoginManagerUser(user)
            login_user(user_mixin)

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


@site_app.route('/oauth/<provider>', methods=['GET'])
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


@site_app.route('/oauth/<provider>/callback', methods=['GET'])
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


@site_app.route('/lost_password', methods=['GET', 'POST'])
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


@site_app.route('/reset_password_email_sent', methods=['GET'])
# @jinja2_view('error.html')
def reset_password_email_sent():
    # return {'title': u"重置密码的邮件已经发出", 'message': u"重置密码的邮件已经发出, 请查收邮件并重置密码"}
    pass


@site_app.route('/reset_password/<token>', methods=['GET', 'POST'])
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


@site_app.route('/reset_password_success', methods=['GET'])
# @jinja2_view('error.html')
def reset_password_success():
    # return {'title': u"重置密码成功", 'message': u"您的密码已经重置, 请重新登录"}
    pass


@site_app.route('/confirm/<token>', methods=['GET'])
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


@site_app.route('/active_email', methods=['GET'])
# @csrf_token
# @jinja2_view('email/active.html')
def active_email():
    # return {'email': request.user.email, 'title': u'注册成功', 'token': request.csrf_token}
    pass


@site_app.route('/success_sendmail', methods=['GET'])
# @jinja2_view('email/confirm.html')
def sendmail_success():
    # return {'title': u"激活邮件发送成功", 'message': u"激活邮件发送成功, 请检查并激活您的账户。"}
    pass


@site_app.route('/sendmail', methods=['POST'])
# @csrf_protect
def send_mail_post():
    # form = EmailForm(request.forms)
    # if form.validate():
    #     user = User.objects(email=form.email.data).first()
    #     send_confirm_email(app.config, user.email)
    #     return redirect('/success_sendmail')
    # return {'form': form}
    pass


def get_pastes_from_search(query_string, p=1):
    def get_string_by_keyword(keyword, query_string):
        string = ''
        result = re.search('\s*%s:([a-zA-Z+-_#]+)\s*' % keyword, query_string)
        if result:
            if len(result.groups()) == 1:
                string = result.groups()[0]
        query_string = query_string.replace('%s:%s' % (keyword, string), '')
        return string, query_string

    tag, query_string = get_string_by_keyword('tag', query_string)
    user, query_string = get_string_by_keyword('user', query_string)
    keyword = query_string.strip()

    criteria = {'title__contains': keyword, 'is_private': False}
    if tag:
        criteria['tags'] = tag
    if user:
        user_object = User.objects(username=user).first()
        if user_object:
            criteria['user'] = user_object

    return keyword, Paste.objects(**criteria).order_by('-updated_at').paginate(p, per_page=2)


@site_app.route('/search', methods=['GET'])
def search_paste():
    page = get_page()
    q = request.args['q']
    keyword, pagination = get_pastes_from_search(q, p=page)
    return render_template('search.html',
                           query_string=q,
                           keyword=keyword,
                           pagination=pagination)
