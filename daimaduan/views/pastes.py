# coding: utf-8
import base64
import hashlib
import hmac
import json
import time

from daimaduan.forms.paste import PasteForm
from flask import abort
from flask import current_app, request
from flask import make_response
from flask import redirect
from flask import render_template, Blueprint
from flask_login import current_user, login_required

from daimaduan.models.base import Paste, Code
from daimaduan.models.tag import Tag

ITEMS_PER_PAGE = 20


paste_app = Blueprint("paste_app", __name__, template_folder="templates")


# Get paste by hash id or raise 404 error.
def get_paste(hash_id):
    return Paste.objects.get_or_404(hash_id=hash_id)


# def get_pastes_from_search(p=1):
#     query_string = request.query.q
#
#     def get_string_by_keyword(keyword, query_string):
#         string = ''
#         result = re.search('\s*%s:([a-zA-Z+-_#]+)\s*' % keyword, query_string)
#         if result:
#             if len(result.groups()) == 1:
#                 string = result.groups()[0]
#         query_string = query_string.replace('%s:%s' % (keyword, string), '')
#         return string, query_string
#
#     tag, query_string = get_string_by_keyword('tag', query_string)
#     user, query_string = get_string_by_keyword('user', query_string)
#     keyword = query_string.strip()
#
#     criteria = {'title__contains': keyword, 'is_private': False}
#     if tag:
#         criteria['tags'] = tag
#     if user:
#         user_object = User.objects(username=user).first()
#         criteria['user'] = user_object
#
#     return keyword, Paste.objects(**criteria).order_by('-updated_at')[(p - 1) * ITEMS_PER_PAGE:p * ITEMS_PER_PAGE]
#
#
# @app.get('/search', name='pastes.search')
# @jinja2_view('search.html')
# def search_get():
#     keyword, pastes = get_pastes_from_search()
#     return {'query_string': request.query.q,
#             'keyword': keyword,
#             'pastes': pastes}
#
#
# @app.get('/search_more')
# @jinja2_view('pastes/pastes.html')
# def search_post():
#     p = int(request.query.p)
#     if not p:
#         p = 2
#
#     keyword, pastes = get_pastes_from_search(p=p)
#     return {'pastes': pastes}
#
#
@paste_app.route('/create', methods=['GET', 'POST'])
@login_required
def create_paste():
    if request.method == 'GET':
        return render_template('pastes/create.html',
                               form=PasteForm(data={'codes': [{'title': '', 'content': ''}]}))
    else:
        form = PasteForm()
        if form.validate_on_submit():
            user = current_user.user
            paste = Paste(title=form.title.data, user=user, is_private=form.is_private.data)
            tags = []
            for i, c in enumerate(form.codes):
                tag_name = c.tag.data.lower()
                if not c.title.data:
                    c.title.data = '代码片段%s' % (i + 1)
                code = Code(title=c.title.data,
                            content=c.content.data,
                            tag=tag_name,
                            user=user)
                code.save()
                tags.append(tag_name)
                tag = Tag.objects(name=tag_name).first()
                if tag:
                    tag.popularity += 1
                else:
                    tag = Tag(name=tag_name)
                tag.save()
                paste.codes.append(code)
            paste.tags = list(set(tags))
            paste.save()
            return redirect('/paste/%s' % paste.hash_id)
        return render_template('pastes/create.html',
                               form=form)


@paste_app.route('/<hash_id>', methods=['GET'])
def view_paste(hash_id):
    paste = Paste.objects.get_or_404(hash_id=hash_id)
    paste.increase_views()

    sig = message = timestamp = None
    if current_user.is_authenticated:
        # create a JSON packet of our data attributes
        data = json.dumps({'id': str(current_user.id), 'username': current_user.username, 'email': current_user.email})
        # encode the data to base64
        message = base64.b64encode(data)
        # generate a timestamp for signing the message
        timestamp = int(time.time())
        # generate our hmac signature
        sig = hmac.HMAC(current_app.config['DISQUS']['secret_key'], '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()

    return render_template('pastes/view.html',
                           paste=paste,
                           message=message,
                           timestamp=timestamp,
                           sig=sig)


@paste_app.route('/<hash_id>/like', methods=['POST'])
@login_required
def like(hash_id):
    paste = get_paste(hash_id)
    return paste.toggle_like_by(request.user, True)


@paste_app.route('/<hash_id>/unlike', methods=['POST'])
@login_required
def unlike(hash_id):
     paste = get_paste(hash_id)
     return paste.toggle_like_by(request.user, False)


@paste_app.route('/<hash_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_get(hash_id):
    paste = get_paste(hash_id)
    if not paste.is_user_owned(request.user):
        abort(404)
    if request.method == 'GET':
        data = {'title': paste.title,
                'is_private': paste.is_private,
                'codes': [{'title': code.title, 'content': code.content, 'tag': code.tag} for code in paste.codes]}
        form = PasteForm(data=data)
        return render_template('pastes/edit.html',
                               form=form,
                               paste=paste)
    else:
        form = PasteForm()
        if form.validate_on_submit():
            paste.title = form.title.data
            paste.is_private = form.is_private.data
            tags = []
            codes = [code for code in paste.codes]
            paste.codes = []
            for code in codes:
                code.delete()
            for i, c in enumerate(form.codes):
                tag_name = c.tag.data.lower()
                if not c.title.data:
                    c.title.data = '代码片段%s' % (i + 1)
                code = Code(title=c.title.data,
                            content=c.content.data,
                            tag=tag_name,
                            user=current_user)
                code.save()
                tags.append(tag_name)
                tag = Tag.objects(name=tag_name).first()
                if tag:
                    tag.popularity += 1
                else:
                    tag = Tag(name=tag_name)
                tag.save()
                paste.codes.append(code)
            paste.tags = list(set(tags))
            paste.save()
            return redirect('/paste/%s' % paste.hash_id)
        return render_template('pastes/edit.html',
                               form=form,
                               paste=paste)


@paste_app.route('/<hash_id>/delete', methods=['POST'])
@login_required
def delete(hash_id):
    paste = get_paste(hash_id)

    if current_user.owns_record(paste):
        paste.delete()
        return redirect('/')
    else:
        abort(403)


@paste_app.route('/<hash_id>/embed.js', methods=['GET'])
def embed_js(hash_id):
    paste = get_paste(hash_id)

    resp = make_response(render_template('paste/embed.js', paste=paste), 200)
    resp.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return resp
