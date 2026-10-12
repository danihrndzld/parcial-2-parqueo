"""API del parqueo. Proyecto base de la parte práctica del Parcial 2.

    GET  /health                 200
    POST /reset                  200   vacía los tickets
    POST /tickets                201 / 409 placa con ticket abierto / 422
    GET  /tickets/{id}           200 / 404
    POST /tickets/{id}/salida    200 / 404 / 409 ticket ya cerrado / 422

Las reglas de cobro están en el README. El estado vive en memoria.
"""

import math
import re
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, field_validator

GRACIA_MIN = 15
TARIFA_HORA = 10
PLACA = re.compile(r"^[PMC]\d{3}[A-Z]{3}$")

app = FastAPI(title="parqueo")
tickets: dict[int, dict] = {}
next_id = 0


class Entrada(BaseModel):
    placa: str
    entrada: datetime

    @field_validator("placa")
    @classmethod
    def placa_valida(cls, v: str) -> str:
        v = v.strip().upper()
        if not PLACA.match(v):
            raise ValueError("placa con formato inválido, se espera p. ej. P123ABC")
        return v


class Salida(BaseModel):
    salida: datetime


def cobrar(minutos: int) -> int:
    if minutos <= GRACIA_MIN:
        return 0
    horas = math.ceil(minutos / 60)
    return horas * TARIFA_HORA


def get_or_404(ticket_id: int) -> dict:
    ticket = tickets.get(ticket_id)
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe el ticket {ticket_id}")
    return ticket


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/reset")
def reset() -> dict:
    global next_id
    tickets.clear()
    next_id = 0
    return {"tickets": 0}


@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def abrir(data: Entrada, response: Response) -> dict:
    global next_id
    if any(t["placa"] == data.placa and t["salida"] is None for t in tickets.values()):
        raise HTTPException(status.HTTP_409_CONFLICT, f"{data.placa} ya tiene un ticket abierto")
    next_id += 1
    ticket = {"id": next_id, "placa": data.placa, "entrada": data.entrada,
              "salida": None, "minutos": None, "monto": None}
    tickets[next_id] = ticket
    response.headers["Location"] = f"/tickets/{next_id}"
    return ticket


@app.get("/tickets/{ticket_id}")
def leer(ticket_id: int) -> dict:
    return get_or_404(ticket_id)


@app.post("/tickets/{ticket_id}/salida")
def cerrar(ticket_id: int, data: Salida) -> dict:
    ticket = get_or_404(ticket_id)
    if ticket["salida"] is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, f"el ticket {ticket_id} ya se cobró")
    if data.salida <= ticket["entrada"]:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "la salida debe ser posterior a la entrada")
    minutos = math.ceil((data.salida - ticket["entrada"]).total_seconds() / 60)
    ticket.update(salida=data.salida, minutos=minutos, monto=cobrar(minutos))
    return ticket


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
