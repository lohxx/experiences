from functools import wraps

from flask import request, session
import datetime
import base64
import werkzeug


def doBasicAuth(b64data):
    _, encodedArgs = b64data.split('Basic')
    user, password = str(base64.b64decode(encodedArgs.strip())).split(':')
    print(user, password)

    if user and password:
        return user, password, True

    return None, None, False


def authenticationRequired(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authenticated = None

        if request.args.get('api_key'):
            authenticated = True

        elif request.headers.get('Authorization'):
            authorization = request.headers.get('Authorization')

            if 'Basic' in authorization:
                user, passw, authenticated = doBasicAuth(authorization)

        # Falta HMAC

        if not authenticated:
            return 'É necessario se autenticar', 401

        return func(*args, **kwargs)

    return wrapper


def checkContentType(accepted_reps):
    """
    Valida o payload enviado para o servidor.


    Raises:
        werkzeug.exceptions.UnsupportedMediaType: Caso o tipo do payload
        não seja suportado pelo servidor.

    Returns:
        any: retorno da view function
    """            
    
    def decorator(func):
        @wraps(func)
        def deco(*args, **kwargs):
            content_type = request.headers.get('Content-Type', '').split(';')[0]

            if content_type.strip() not in accepted_reps:
                raise werkzeug.exceptions.UnsupportedMediaType(
                    f'Apenas a representação do tipo: {", ".join(accepted_reps)} é aceita')
            
            return func(*args, **kwargs)
        
        return deco

    return decorator


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
                return func(mimes_fav[0][0], *args, **kwargs)

            raise werkzeug.exceptions.NotAcceptable(
                f"Representações disponíveis: {', '.join(representations)}")

        return deco
    return decorator

