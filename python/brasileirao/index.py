from collections import OrderedDict

import re
import werkzeug
from functools import wraps

from flask import Flask
from flask import request, make_response, render_template, jsonify

from api_reposta import resposta

app = Flask(__name__)

AVALIABLE_REPRESENTATIONS = ['text/html', 'application/json']


def checkContentType(func):
    @wraps(func)
    def deco(*args, **kwargs):
        ContentTypeHeader = request.headers.get('Content-Type', '')
        return func(*args, **kwargs)
    
    return deco


def checkAcceptHeader(func):
    """
        Valida se o servidor tem alguma das representações especificadas
        pelo cliente atraves do header Accept.

        As atuais representações disponibilizadas pelo servidor são: text/html e application/json.

        Raises:
            werkzeug.exceptions.NotAcceptable: Retorna o status code 406 para os clientes.

        Returns:
            str/dict: resposta da função decorada.
    """
    @wraps(func)
    def deco(*args, **kwargs):    
        global qFactor

        mimes_fav = []
        AcceptedRepresentations = request.headers.get('Accept', '').split(',')

        for content_type in AcceptedRepresentations:
            try:
                mime, qfactor = content_type.split(';')
            except ValueError:
                mime, qfactor = content_type, 'q=0'

            mime = mime.strip()

            if mime in AVALIABLE_REPRESENTATIONS:
                mimes_fav.append((mime, float(qfactor.split('=')[-1])))

            elif '*/*' == mime:
                mimes_fav.append((mime, 0))

        mimes_fav.sort(key=lambda rep: rep[1], reverse=True)

        if mimes_fav:
            qFactor = mimes_fav[0][0]
            return func(*args, **kwargs)
        
        raise werkzeug.exceptions.NotAcceptable(
            f"Representações disponíveis: {', '.join(AVALIABLE_REPRESENTATIONS)}")

    return deco


@app.route('/api/classificacoes')
@checkAcceptHeader
def classificacoes():
    if 'text/html' == qFactor:
        return render_template(
            'index.html', 
            classificacao=resposta['classificacoes'])

    elif 'application/json' == qFactor:
        return jsonify(resposta['classificacoes'])

    # O cliente aceita qualquer tipo de representação, então mandamos JSON por padrão.
    elif '*/*' == qFactor:
        return jsonify(resposta['classificacoes'])
 

@app.route('/api/rodadas')
@checkAcceptHeader
def rodadas():
    return resposta['rodadas']


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
