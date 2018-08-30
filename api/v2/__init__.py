'''
___init__.py
main config  file
'''

from flask_api import FlaskAPI
from api.v2.config import CONFIG
from api.v2.manage import DBSetup
from flask_cors import CORS

CONN = DBSetup()


def create_app(config):
    ''' function that receives configaration and creates the app'''
    app = FlaskAPI(__name__)
    CORS(app)
    app.config.from_object(CONFIG[config])
    app.url_map.strict_slashes = False
    from api.v2.answer.views import answer_blueprint
    from api.v2.question.views import question_blueprint
    from api.v2.comment.views import comment_blueprint
    from api.v2.user.views import auth_blueprint
    from . errors_handler import resource_not_found, method_not_allowed, server_error, bad_request
    app.register_blueprint(answer_blueprint, url_prefix='/api/v2')
    app.register_blueprint(question_blueprint, url_prefix='/api/v2')
    app.register_blueprint(comment_blueprint, url_prefix='/api/v2')
    app.register_blueprint(auth_blueprint, url_prefix='/api/v2/auth')
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(405,method_not_allowed)
    app.register_error_handler(500, server_error)
    app.register_error_handler(400, bad_request)
    CONN.create_tables()
    return app
