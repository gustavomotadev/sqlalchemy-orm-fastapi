import uvicorn
from fastapi import FastAPI
from typing import Callable
from locacao.controladores.controlador_base import ControladorBase
from locacao.controladores.controlador_aluno import ControladorAluno

def vincular_controlador(app: FastAPI, controlador: ControladorBase):
    for endpoint in controlador.endpoints:
        app.add_api_route(path=endpoint.rota, endpoint=endpoint, 
            methods=endpoint.metodos)

app = FastAPI()

controlador_aluno = ControladorAluno()

vincular_controlador(app, controlador_aluno)

if __name__ == '__main__':
    uvicorn.run("api:app", port=8000, host='0.0.0.0', reload = True)