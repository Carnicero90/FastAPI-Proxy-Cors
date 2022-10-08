import requests
from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import Response as Res
import json

app = FastAPI()


@app.api_route("/proxer/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
def proxer(rest: str, response: Response, request: Request, payload: Optional[dict] = None):

    h = dict(request.headers)
    if h.get('host'):
        del h['host']
    call = getattr(requests, request.method.lower())
    rest = rest + '?' + str(request.query_params)
    print(h)
    if payload:
        # TODO: magari fare per metodo (anzi: sicuramente), comunque cosi ci funzia solo per json (magari conviene davvero farlo piu a basso livello, via socket?)
        r = call(url=rest, data=json.dumps(payload),
                 headers=h, stream=True)
    else:
        r = call(url=rest, headers=h, stream=True)
    h = r.headers

    for key, value in h.items():
        response.headers[key] = value

    response.headers['Access-Control-Allow-Origin'] = '*'

    r = Res(headers=response.headers, content=r.raw.data,
                 status_code=r.status_code)
    return r
