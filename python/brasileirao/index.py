"Pratica dos conceitos de web apis aprendidos"

import re
import werkzeug

from flask import Flask, Blueprint
from flask import make_response, render_template, jsonify
from flask import session, request

from api_reposta import resposta
from utils import checkContentType
from utils import checkAcceptHeader
from utils import authenticationRequired
from utils import rateLimit
from flask_caching import Cache


config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
api = Blueprint('api', __name__, url_prefix='/api')

cache = Cache(config={'CACHE_TYPE': 'simple', 'timeout': 60})


@api.route('/classificacoes')
#@authenticationRequired
@checkAcceptHeader(['text/html', 'application/json'])
@rateLimit(2)
def classificacoes(contentType):
    if 'text/html' == contentType:
        return render_template(
            'index.html', 
            classificacao=resposta['classificacoes'])

    elif 'application/json' == contentType or '*/*' == contentType:
        return jsonify(resposta['classificacoes'])


@api.route('/rodadas')
@authenticationRequired
def rodadas():
    return jsonify(resposta['rodadas'])


@api.route('/rodadas/<numero>')
@authenticationRequired
def rodada(numero):
    """
    Agenda notificação para uma rodada especifica.

    Returns:
        list: lista com todos os jogos de uma rodada especifica.
    """

    rodada = list(filter(
        lambda rodada: rodada['rodada'] == numero,
        resposta['rodadas']))

    if not rodada:
        return 'Rodada não encontrada', 404

    return jsonify(rodada)


app.register_blueprint(api)
cache.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
