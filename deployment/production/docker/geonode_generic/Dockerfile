# Create intermediate image because it will
FROM python:3.7.0-stretch as intermediate

RUN mkdir -p /root/.ssh
COPY ssh_key/* /root/.ssh/

RUN chmod -R 600 /root/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN mkdir -p /usr/src/
WORKDIR /usr/src

# Copy customized geonode settings
ARG SCANAGROEMPRESA_DOCKER_TAG=master
RUN git clone --branch ${SCANAGROEMPRESA_DOCKER_TAG} --depth 1 git@github.com:kartoza/scanagroempresa-docker.git

FROM geosolutionsit/geonode-generic:1.0

COPY --from=intermediate /usr/src/scanagroempresa-docker/django_project/ /usr/src/scanagroempresa-docker/

RUN pip install -r /usr/src/scanagroempresa-docker/requirements.txt

ADD install-theme-app.sh /install-theme-app.sh

ADD entrypoint.sh /entrypoint.sh

ADD uwsgi.ini /usr/src/app/uwsgi.ini

ENTRYPOINT ["/entrypoint.sh"]
