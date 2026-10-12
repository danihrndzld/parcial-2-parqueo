<h1 align="center">Parqueo</h1>

<p align="center">
  Parte práctica del Parcial 2 de Calidad y Automatización en Ingeniería de Software, UFM 2026.<br>
  Un API de parqueo en Python con una regla de cobro que no se cumple, una suite de Bruno incompleta y un Jenkinsfile que no funciona como puerta.
</p>

<p align="center">
  <a href="#qué-hay-que-hacer">Qué hay que hacer</a> |
  <a href="#reglas-de-cobro">Reglas de cobro</a> |
  <a href="#entrega">Entrega</a> |
  <a href="#uso-de-ia">Uso de IA</a> |
  <a href="#problemas-comunes">Problemas comunes</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/puntos-5-2E5D4B" alt="5 puntos">
  <img src="https://img.shields.io/badge/tiempo-45%20min-2E5D4B" alt="45 minutos">
  <img src="https://img.shields.io/badge/Python-uv-3776AB" alt="Python con uv">
  <img src="https://img.shields.io/badge/Bruno-bru%20run-F4AA41" alt="Bruno">
  <img src="https://img.shields.io/badge/Jenkins-Pipeline-D24939" alt="Jenkins">
</p>

El repositorio trae el API, dos colecciones de Bruno (`bruno/smoke` y `bruno/regresion`, ambas en verde), el `Containerfile` del API y un `Jenkinsfile`. Para correr el proyecto tal como viene:

```bash
uv run api.py                                    # escucha en 127.0.0.1:8000
cd bruno/regresion && bru run --env local --sandbox=developer
```

El `Jenkinsfile` construye la imagen del API con `docker build`, así que el contenedor `jenkins` tiene que traer el CLI de docker y el socket del motor montado. Antes de empezar, este comando tiene que listar los contenedores, incluido `jenkins`. Si responde `docker: not found` o `Cannot connect to the Docker daemon`, se recrea el contenedor `jenkins` con el CLI de docker instalado y el socket del motor montado en `/var/run/docker.sock`.

```bash
podman exec jenkins docker ps      # con Docker Desktop: docker exec jenkins docker ps
```

## Qué hay que hacer

| Inciso | Puntos | Qué se pide |
|---|---|---|
| **P1. Regresión** | 1.5 | La suite `bruno/regresion` no cubre una de las reglas de cobro. Agregar dos casos que la cubran, con aserciones sobre el resultado que da la tabla. Si el API no cumple la regla, la suite tiene que quedar en rojo. |
| **P2. Jenkins** | 2 | El `Jenkinsfile` corre, pero tiene exactamente tres fallas por las que no funciona como puerta ni reporta bien. Corregirlas en el mismo archivo y explicar cada una en `RESPUESTAS.md`, en una línea: qué estaba mal y qué consecuencia tenía. Crear en Jenkins un job `parcial2` de tipo Pipeline que lea el `Jenkinsfile` de este repositorio, rama `main`. |
| **P3. Evidencia** | 1.5 | Tres builds del job `parcial2`, en el orden de la lista de abajo y con un commit por paso. Cada build tiene que terminar antes del push siguiente, porque si dos pushes caen en la misma revisión de Jenkins se ejecuta un solo build. Cualquier build se puede lanzar con *Build Now* en vez de esperar a que Jenkins detecte el push. |

Los tres pasos de P3 son estos:

1. Push del `Jenkinsfile` corregido, todavía sin la prueba de P1. El build queda en verde.
2. Push de la prueba de P1. El build queda en rojo.
3. Arreglar `api.py` para que cumpla la regla, y push. El build vuelve a verde.

`RESPUESTAS.md` y `evidencia/` pueden ir en un commit posterior a los tres pasos. El build que dispare ese commit no cuenta.

## Reglas de cobro

Estas reglas deciden si un resultado es correcto.

| Concepto | Regla |
|---|---|
| Placa | Letra `P`, `M` o `C`, tres dígitos y tres letras, por ejemplo `P123ABC`. Se acepta en minúsculas y se guarda en mayúsculas. Cualquier otro formato da 422. |
| Ticket abierto | Una placa no puede tener dos tickets abiertos a la vez. El segundo da 409. |
| Minutos | De la entrada a la salida, redondeados hacia arriba al minuto. |
| Gracia | 15 minutos o menos cuestan Q0. |
| Tarifa | Pasada la gracia, Q10 por hora o fracción, contadas desde la entrada. |
| Tope | Ningún ticket paga más de Q60. |
| Salida | Tiene que ser posterior a la entrada, si no da 422. Un ticket se cobra una sola vez, y el segundo cobro da 409. |

## Entrega

Antes de que termine el período, se sube a MiU la URL de un repositorio propio, creado desde este con *Use this template*. Ese repositorio tiene que ser público, porque así Jenkins lo lee sin credenciales y se puede calificar. El repositorio tiene que contener lo siguiente:

- El `Jenkinsfile` corregido y la prueba de P1 en `bruno/regresion/`.
- `RESPUESTAS.md`, con una línea por cada falla del `Jenkinsfile`, el número de build y el SHA de los tres builds de P3, y el nombre de la aserción que falló en el build rojo, tal como aparece en su Test Result.
- `evidencia/jenkins/01-rojo.png` y `evidencia/jenkins/02-verde.png`, con la vista de Stages de los builds de los pasos 2 y 3 y la barra de direcciones visible.

Se califica la rama `main` y su historial, así que no se permite squash ni force push.

## Uso de IA

Se permite usar IA en cualquier inciso, por ejemplo un asistente de chat, Copilot o un agente en la terminal. Se califica lo que queda en el repositorio y en Jenkins, con la misma llave que si no se hubiera usado IA. Las explicaciones de `RESPUESTAS.md` tienen que describir los cambios que de verdad hay en el `Jenkinsfile`.

## Problemas comunes

Si el puerto 8000 ya está ocupado por otro API, este comando muestra qué proceso lo tiene:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```
