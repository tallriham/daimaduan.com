from daimaduan.utils.pagination import get_page, paginate
from flask import Blueprint, render_template, request

from daimaduan.models.base import Paste
from daimaduan.models.tag import Tag
from daimaduan.views.pastes import ITEMS_PER_PAGE

tag_app = Blueprint('tag_app', __name__, template_folder="templates")


@tag_app.route('/<tag_name>', methods=['GET'])
def tag(tag_name):
    tag = Tag.objects.get_or_404(name=tag_name)
    page = get_page()

    pastes = tag.pastes(is_private=False).order_by('-updated_at')
    pastes, summary = paginate(pastes, page)

    return render_template('tags/view.html',
                           tag=tag,
                           pastes=pastes,
                           page_summary=summary)


@tag_app.route('/<tag_name>/more', methods=['GET'])
def tag_more(tag_name):
    p = int(request.args.p)
    if not p:
        return {}
    return render_template('pastes/pastes.html',
                           pastes=Paste.objects(tags=tag_name, is_private=False).order_by('-updated_at')[(p - 1) * ITEMS_PER_PAGE:p * ITEMS_PER_PAGE])