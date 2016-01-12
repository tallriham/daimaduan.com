# coding: utf-8
from flask import Blueprint, render_template
from flask import request

from flask_login import current_user

from daimaduan.models.base import User
from daimaduan.models.tag import Tag
from daimaduan.utils.pagination import paginate, get_page

user_app = Blueprint("user_app", __name__, template_folder="templates")


@user_app.route('/user/manage', methods=['POST'])
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


@user_app.route('/<username>', methods=['GET'])
def view_user(username):
    page = get_page()
    user = User.objects.get_or_404(username=username)

    pastes = user.pastes.order_by('-updated_at')
    if not (current_user.is_authenticated and current_user.user == user):
        pastes = pastes(is_private=False)

    pagination = pastes.paginate(page, per_page=20)

    return render_template('user/user.html',
                           user=user,
                           pagination=pagination,
                           tags=Tag.objects().order_by('-popularity')[:10])


@user_app.route('/<username>/likes', methods=['GET'])
def view_likes(username):
    user = User.objects.get_or_404(username=username)

    page = get_page()
    likes = user.likes.order_by('-updated_at')
    pagination = likes.paginate(page, per_page=20)

    return render_template('user/likes.html',
                           user=user,
                           pagination=pagination,
                           tags=Tag.objects().order_by('-popularity')[:10])


@user_app.route('/user/watch', methods=['POST'])
def watch_user():
    user = User.objects(username=request.args.get('user')).first_or_404()
    current_user.user.watched_users.append(user)
    current_user.user.save()
    return {'watchedStatus': current_user.user.is_watched(user)}


@user_app.route('/user/unwatch', methods=['POST'])
def unwatch_user():
    user = User.objects(username=request.params.get('user')).first_or_404()
    current_user.user.watched_users.remove(user)
    current_user.user.save()
    return {'watchedStatus': request.user.is_watched(user)}
