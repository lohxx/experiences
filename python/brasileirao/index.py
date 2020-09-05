"Pratica dos conceitos de web apis aprendidos"

from collections import OrderedDict

import re
import werkzeug
from functools import wraps

from flask import Flask
from flask import request, make_response, render_template, jsonify

from api_reposta import resposta

app = Flask(__name__)


def checkContentType(func):
    @wraps(func)
    def deco(*args, **kwargs):
        ContentTypeHeader = request.headers.get('Content-Type', '')
        return func(*args, **kwargs)
    
    return deco


def checkAcceptHeader(representations):
    """
    Valida se o servidor tem alguma das representações especificadas
    pelo cliente atraves do header Accept.

    Args:
        representations (list): As representações disponibilizadas pelo servidor.


    Raises:
        ValueError: Exception se a lista de representações estiver vazia.

        werkzeug.exceptions.NotAcceptable: Retorna o status code 406 para os clientes
        quando não temos a representação desejada disponivel.

    Returns:
        str/dict: resposta da função decorada.
    """    

    def decorator(func):

        @wraps(func)
        def deco(*args, **kwargs):    
            global qFactor

            if not representations:
                raise ValueError('É necessario fornecer as representações disponiveis')

            mimes_fav = []
            for content_type in request.headers.get('Accept', '').split(','):
                try:
                    mime, qfactor = content_type.split(';')
                except ValueError:
                    mime, qfactor = content_type, 'q=0'

                mime = mime.strip()

                if mime in representations:
                    mimes_fav.append((mime, float(qfactor.split('=')[-1])))

                elif '*/*' == mime:
                    mimes_fav.append((mime, 0))

            mimes_fav.sort(key=lambda rep: rep[1], reverse=True)

            if mimes_fav:
                qFactor = mimes_fav[0][0]
                return func(*args, **kwargs)

            raise werkzeug.exceptions.NotAcceptable(
                f"Representações disponíveis: {', '.join(representations)}")

        return deco
    return decorator


@app.route('/api/classificacoes')
@checkAcceptHeader(['text/html', 'application/json'])
def classificacoes():
    if 'text/html' == qFactor:
        return render_template(
            'index.html', 
            classificacao=resposta['classificacoes'])

    elif 'application/json' == qFactor or '*/*' == qFactor:
        return jsonify(resposta['classificacoes'])


@app.route('/api/rodadas')
@checkAcceptHeader(['application/json'])
def rodadas():
    return jsonify(resposta['rodadas'])


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
