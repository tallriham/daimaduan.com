# coding: utf-8
import logging

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.assets import Environment
from flask.ext.assets import Bundle
from daimaduan.utils.filters import datetimeformat
from daimaduan.utils.filters import time_passed
from daimaduan.utils.filters import ternary


db = MongoEngine()

# def get_current_path():
#     file_name = os.path.dirname(__file__)
#     return os.path.abspath(file_name)
from daimaduan.views.pastes import paste_app
from daimaduan.views.users import user_app

logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger('daimaduan')


app = Flask(__name__)
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(paste_app, url_prefix='/paste')

app.config['MONGODB_SETTINGS'] = {
    'db': 'daimaduan',
    'host': '192.168.99.100'
}
db.init_app(app)

app.jinja_env.filters['time_passed'] = time_passed
app.jinja_env.filters['ternary'] = ternary
app.jinja_env.filters['datetimeformat'] = datetimeformat

assets = Environment(app)
js = Bundle('js/app.js',
            'js/errors.js',
            'js/highlightjs.line.numbers.min.js',
            'js/pastes.js',
            'js/tags.js',
            'js/users.js',
            filters='uglifyjs', output='js/compiled.js')
assets.register('js_all', js)

css = Bundle('css/app.css',
             'css/errors.css',
             'css/pastes.css',
             'css/tags.css',
             'css/users.css',
             filters='cssmin', output='css/compiled.css')
assets.register('css_all', css)

# app.config.load_config('%s/config.cfg' % get_current_path())
# # Check if there's a key in env variables
# # if you want to set config on the fly, use env var
# # a.b.c in config => A_B_C in env var
# for key in app.config.keys():
#     k = key.replace('.', '_').upper()
#     if k in os.environ:
#         app.config[key] = os.environ[k]
# app.config['SECRET_KEY'] = app.config['site.validate_key']

# jinja = JinajaPlugin(template_path='%s/templates' % get_current_path())
# login = LoginPlugin()
#
# app.install(login)
# app.install(jinja)
# app.install(MongoenginePlugin())
#
# oauth_services = {}
# oauth_services['google'] = OAuth2Service(**oauth_config(app.config, 'google'))
# oauth_services['github'] = OAuth2Service(**oauth_config(app.config, 'github'))
