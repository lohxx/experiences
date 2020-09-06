"Pratica dos conceitos de web apis aprendidos"

import re
import werkzeug

from flask import Flask, Blueprint
from flask import make_response, render_template, jsonify
from flask import session, request

from api_reposta import resposta
from utils import checkContentType
from utils import checkAcceptHeader

app = Flask(__name__)

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/classificacoes')
@checkAcceptHeader(['text/html', 'application/json'])
def classificacoes(contentType):
    if 'text/html' == contentType:
        return render_template(
            'index.html', 
            classificacao=resposta['classificacoes'])

    elif 'application/json' == contentType or '*/*' == contentType:
        return jsonify(resposta['classificacoes'])


@api.route('/rodadas')
def rodadas():
    return jsonify(resposta['rodadas'])


@api.route('/rodadas/<numero>')
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

if __name__ == '__main__':
    app.run(debug=True)
