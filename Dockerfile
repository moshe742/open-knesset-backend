# Pulled March 22, 2023
FROM --platform=linux/amd64 python:3.8@sha256:a07637d351af5829bbd650735a5beed77fb467a124388191ac3fa5b8812e67c5
RUN pip install --upgrade pip && pip install gunicorn==20.1.0
WORKDIR /srv
COPY gunicorn_conf.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY server.py ./
COPY api ./api
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["gunicorn", "-c", "gunicorn_conf.py", "server:app"]
