import requests
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()

@app.api_route("/proxer/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
def proxer(rest: str, request: Request, payload: Optional[dict] = None):

    h = dict(request.headers)
    # TODO: magari sovrascrivilo
    if h.get('host'):
        del h['host']

    call = getattr(requests, request.method.lower())
    if payload:
        # TODO: magari fare per metodo
        response = call(url=rest, data=payload,
                        headers=h, allow_redirects=False)
    else:
        response = call(url=rest, headers=h, allow_redirects=False)
    response = requests.get(rest)
    response.headers['Access-Control-Allow-Origin'] = '*'

    # TODO: prima o poi risolvilo, per ora va bene
    if response.headers.get('Content-Encoding'):
        del response.headers['Content-Encoding']

    r = Response(headers=response.headers, content=response.content,
                 status_code=response.status_code)
    return r