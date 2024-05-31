FROM python:latest

RUN mkdir -p /usr/src/fastapi-app/
WORKDIR /usr/src/fastapi-app/

# env from the terminal to export
ARG DB_HOST_NAME
ARG DB_NAME
ARG DB_USER
ARG db_password
ARG SECRECT_KEY
ARG ALGORITHM
ARG ACCESS_TOKEN_EXPIRE_MINUTES

# env variable defined in the app
# for example from the app/Database/DatabaseQuery/database_engine.py db_name = os.getenv('db_name')
ENV db_host_name=${DB_HOST_NAME}
ENV db_name=${DB_NAME}
ENV db_user=${DB_USER}
ENV db_password=${DB_PASSWORD}
ENV SECRECT_KEY=${SECRECT_KEY}
ENV ALGORITHM=${ALGORITHM}
ENV ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}


COPY ../../requirements.txt /usr/src/fastapi-app/

RUN pip install -r requirements.txt

COPY ../../  /usr/src/fastapi-app/

EXPOSE 8080

CMD ["fastapi","run", "app/main.py","--port","8080"]