import uvicorn
from fastapi import FastAPI, APIRouter
from locacao.controladores.controlador_base import ControladorBase
from locacao.controladores.controlador_locadora import ControladorLocadora

VERSAO_API = '/v1'

def vincular_controlador(app: FastAPI, controlador: ControladorBase):
    roteador = APIRouter(prefix=VERSAO_API)
    for endpoint in controlador.endpoints:
        roteador.add_api_route(endpoint=endpoint, **endpoint.rota)
    app.include_router(roteador)

app = FastAPI()

control_locadora = ControladorLocadora()

vincular_controlador(app, control_locadora)

if __name__ == '__main__':
    uvicorn.run("api:app", port=8000, host='0.0.0.0', reload = True)