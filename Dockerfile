FROM python:3.13.3-slim-bookworm

LABEL authors="Jose Roberto Assis <assisjrt@gmail.com>"
LABEL image.description="simple web uuid application image"
LABEL image.source="https://github.com/assisjrt/simple-web-uuid.git"
LABEL image.title="simple web uuid"
LABEL image.version="0.1.0"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING=UTF-8
ENV POETRY_VIRTUALENVS_CREATE=false
ENV APP_ENVIRONMENT=development
ENV DEBUG=False

ARG _USER=NjU1MzY
ARG _GROUP=NjU1MzY
ARG _UID=65536
ARG _GID=65536
ARG _DOCUMENT_ROOT=/app

WORKDIR ${_DOCUMENT_ROOT}

CMD ["gunicorn", "simple_web_uuid:app", "--bind", "0.0.0.0:8080", "--worker-class", "gevent", "--workers", "1", "--worker-connections", "1000", "--keep-alive", "5", "--timeout", "10", "--log-level=info", "--access-logfile", "-", "--error-logfile", "-"]

SHELL ["/bin/bash", "-eux", "-c"]

RUN addgroup --system ${_GROUP} --gid ${_GID} --force-badname \
    && \
    adduser --system --uid ${_UID} --ingroup ${_GROUP} --home /home/${_USER} \
        --disabled-password --shell /bin/bash ${_USER} --force-badname --quiet

COPY --chown=${_USER}:${_GROUP} . .

RUN pip install --no-cache-dir poetry==2.1.3 \
    && poetry config requests.max-retries 3 \
    && poetry config installer.max-workers "$(nproc)" \
    && poetry install \
        --no-interaction \
        --no-ansi \
        --no-root \
        --only main

RUN chown -Rf ${_USER}:${_GROUP} \
    ${_DOCUMENT_ROOT}

USER ${_USER}
