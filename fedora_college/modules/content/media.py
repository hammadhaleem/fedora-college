# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from flask import url_for, g
from fedora_college.modules.content.forms import *  # noqa
from fedora_college.core.models import *  # noqa
from flask_fas_openid import fas_login_required
from sqlalchemy import desc

bundle = Blueprint('content', __name__, template_folder='templates')

# authenticated media.


def authenticated():
    return hasattr(g, 'fas_user') and g.fas_user

# media view


@bundle.route('/media/view')
@bundle.route('/media/view/')
@bundle.route('/media/view/<mediaid>')
@bundle.route('/media/view/<mediaid>/')
@bundle.route('/media/view/page/<id>')
@bundle.route('/media/view/page/<id>/')
def displaymedia(mediaid=None, id=0):
    id = int(id)
    token = None
    try:
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first_or_404()
        token = user.token
    except:
        pass
    url = url_for('content.displaymedia')
    if mediaid is not None:
            media = Media.query.filter_by(media_id=mediaid). order_by(
                desc(Media.media_id)).limit(10).all()
            return render_template(
                'media/index.html',
                data=media,
                url=url,
                id=id,
                lists=media,
                token=token
            )
    else:
        lists = Media.query.order_by(
            desc(Media.media_id)).all()
        id = int(id)
        if id > 0:
            media = lists[id:id + 10]
        else:
            id = 0
            media = lists[0:10]
        return render_template(
            'media/index.html', data=media,
            lists=lists[0:20],
            url=url,
            id=id,
            token=token
        )

# media add


@bundle.route('/media/add/', methods=['GET', 'POST'])
@bundle.route('/media/add', methods=['GET', 'POST'])
@fas_login_required
def uploadmedia():

    if authenticated():
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first_or_404()
        token = user.token
        tags = Tags.query.all()
        form_action = url_for('api.uploadvideo', token=token)
        return render_template('media/uploadmedia.html',
                               form_action=form_action,
                               title="add media",
                               tags=tags,
                               head="Add New Media")
    abort(404)

# media view / revise media


@bundle.route('/media/view/<mediaid>/revise')
@bundle.route('/media/view/<mediaid>/revise/')
@fas_login_required
def revisemedia(mediaid=None):
    if authenticated():
        user = UserProfile.query. \
            filter_by(username=g.fas_user['username']).first_or_404()
        token = user.token
        tags = Tags.query.all()
        form_action = url_for('api.revisevideo',
                              videoid=mediaid,
                              token=token)
        return render_template('media/uploadmedia.html',
                               form_action=form_action,
                               title="add media",
                               tags=tags,
                               head="Revise media")
    abort(404)
