from flask import Flask, Blueprint, request
from flask_restplus import Api, Resource, fields
from marshmallow import Schema, fields as ma_field, post_load
from functools import wraps

app = Flask(__name__)

# blueprint = Blueprint('api', __name__, url_prefix='/api')
# api = Api(blueprint, doc='/documentation') # doc=False
# app.register_blueprint(blueprint)
# app.config['SWAGGER_UI_JSONEDITOR'] = True

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    }
}

api = Api(app, authorizations=authorizations)

a_language = api.model('Language', 
    {'language': fields.String('The language')},
    {'framwork': fields.String('The framwork')}
)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'message': 'Token is missing'}, 401
        if token != 'mytoken':
            return {'message': 'Your token is wrong.'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated

class TheLanguage(object):
    def __init__(self, language, framework):
        self.language = language
        self.framework = framework

    def __repr__(self):
        return '{} is the language. {} is the framework'.format(self.language, self.language)

class LanguageSchema(Schema):
    language = ma_field.String()
    framework = ma_field.String()

    @post_load
    def create_language(self, data):
        return Language(**data)

# languages = [{'language': 'python', 'id': 1}]
languages = []
python = TheLanguage(language='python', framework='Flask')
languages.append(python)

@api.route('/language')
class Language(Resource):

    # @api.marshal_with(a_language, envelop='data')
    @api.doc(security='apiKey')
    @token_required
    def get(self):
        schema = LanguageSchema(many=True)
        return schema.dump(languages)

    @api.expect(a_language)
    def post(self):
        schema = LanguageSchema()
        new_language = schema.load(api.payload)
        languages.append(new_language.data)
        return {'result': 'Language added'}, 201

if __name__ == '__main__':
    app.run(debug=True)