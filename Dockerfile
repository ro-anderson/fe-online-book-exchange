# Start from the official Python base image.
FROM python:3.9 as base

# Environment variables to configure Flask
ENV API_HOST="0.0.0.0" \
    API_PORT="5000" \
    API_GROUP="fastapi" \
    API_USER="fastapi" \
    API_DIR="/usr/src/api" \
    FLASK_ENV="development" \
    FLASK_APP="api.py" \
    DEBUG_HOST="0.0.0.0" \
    DEBUG_PORT="5678" \
    DEBUG_LIB_PATH="/usr/src/api" \
    DEBUG_MODULE="app" \
    DEBUG_FILE="main.py"

# Work directory inside container
WORKDIR ${API_DIR}

# Copy the file with the requirements to the /code directory.
COPY ./requirements.txt ${API_DIR}/requirements.txt
COPY . /usr/src/api

# Install requirements
RUN pip install --no-cache-dir --upgrade -r ${API_DIR}/requirements.txt

# Expose Flask to outside the container
EXPOSE ${API_PORT}

# Up uvicorn sever
CMD uvicorn app.main:app --host ${API_HOST} --port ${API_PORT} --reload


###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install debugpy
CMD python -m debugpy --listen ${DEBUG_HOST}:${DEBUG_PORT} --wait-for-client ${DEBUG_LIB_PATH}/${DEBUG_MODULE}/${DEBUG_FILE}
EXPOSE ${DEBUG_PORT}

###########START NEW IMAGE: PRODUCTION ###################
FROM base as prod
COPY ./app /usr/src/api/app
