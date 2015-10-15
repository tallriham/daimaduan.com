# coding: utf-8
from bottle import abort
from bottle import request
from bottle import redirect
from bottle import jinja2_view

from daimaduan.bootstrap import app
from daimaduan.bootstrap import login

from daimaduan.forms import PasteForm

from daimaduan.models import Syntax
from daimaduan.models import Code
from daimaduan.models import Paste
from daimaduan.models import Tag


@app.route('/', name='pastes.index')
@jinja2_view('index.html')
def index():
    return {'pastes': Paste.objects().order_by('-updated_at')}


@app.get('/create', name='pastes.create')
@login.login_required
@jinja2_view('pastes/create.html')
def create_get():
    form = PasteForm(data={'codes': [{'title': '', 'content': ''}]})
    return {'form': form}


@app.post('/create', name='pastes.create')
@login.login_required
@jinja2_view('pastes/create.html')
def create_post():
    form = PasteForm(request.POST)
    if form.validate():
        user = login.get_user()
        paste = Paste(title=form.title.data, user=user)
        tags = []
        for c in form.codes:
            tag_name = c.tag.data.lower()
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
    return {'form': form}



@app.route('/paste/<hash_id>', name='pastes.show')
@jinja2_view('pastes/view.html')
def view(hash_id):
    paste = Paste.objects(hash_id=hash_id).first()
    if not paste:
        abort(404)
    return {'paste': paste}


@app.route('/paste/<hash_id>/edit', name='pastes.update')
@login.login_required
@jinja2_view('pastes/edit.html')
def edit_get(hash_id):
    paste = Paste.objects(hash_id=hash_id).first()
    if not paste:
        abort(404)
    if paste.user.id != request.user.id:
        abort(404)
    data = {'title': paste.title,
            'codes': [{'title': code.title, 'content': code.content, 'tag': code.tag} for code in paste.codes]}
    form = PasteForm(data=data)
    return {'form': form, 'paste': paste}


@app.post('/paste/<hash_id>/edit', name='pastes.update')
@login.login_required
@jinja2_view('pastes/edit.html')
def edit_post(hash_id):
    paste = Paste.objects(hash_id=hash_id).first()
    if not paste:
        abort(404)
    if paste.user.id != request.user.id:
        abort(404)
    form = PasteForm(request.POST)
    if form.validate():
        user = login.get_user()
        paste.title = form.title.data
        tags = []
        for code in paste.codes:
            paste.codes.remove(code)
            code.delete()
        for c in form.codes:
            tag_name = c.tag.data.lower()
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
    return {'form': form, 'paste': paste}


@app.route('/tags', name='tags.index')
@jinja2_view('tags/index.html')
def tags():
    return {'tags': Tag.objects().order_by('-popularity')}


@app.route('/tag/<tag_name>', name='tags.show')
@jinja2_view('tags/view.html')
def tag(tag_name):
    return {'tag': Tag.objects(name=tag_name).first(),
            'pastes': Paste.objects(tags=tag_name)[:10]}
