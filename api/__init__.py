'''
___init__.py
main config  file
'''

from flask_api import FlaskAPI
from api.config import CONFIG



def create_app(config):
    ''' function that receives configaration and creates the app'''
    app = FlaskAPI(__name__)
    app.config.from_object(CONFIG[config])
    app.url_map.strict_slashes = False
    from api.answer.views import answer_blueprint
    from api.question.views import question_blueprint
    app.register_blueprint(answer_blueprint, url_prefix='/api/v1')
    app.register_blueprint(question_blueprint, url_prefix='/api/v1')
    return app
