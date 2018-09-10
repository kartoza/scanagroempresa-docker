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
ARG SCANWEBGIS_DOCKER_TAG=master
RUN git clone --branch ${SCANWEBGIS_DOCKER_TAG} --depth 1 git@github.com:kartoza/scanwebgis-docker.git

FROM geosolutionsit/geonode-generic:1.0

#RUN mkdir -p /home/web/extra_app

COPY --from=intermediate /usr/src/scanwebgis-docker/django_project/ /usr/src/scanwebgis-docker/
