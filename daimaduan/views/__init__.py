
#
# @app.hook('before_request')
# def before_request():
#     request.user = login.get_user()
#
#
# @app.hook('after_request')
# def after_request():
#     Jinja2Template.defaults['session'] = request.environ.get('beaker.session')
#
#
# @app.get('/status')
# def status():
#     return {'pastes_count': Paste.objects().count(),
#             'codes_count': Code.objects().count(),
#             'users_count': User.objects().count()}
