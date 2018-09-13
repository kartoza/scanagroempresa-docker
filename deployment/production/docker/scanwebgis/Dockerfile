# Create intermediate image because it will
FROM python:3.7.0-stretch as intermediate

RUN mkdir -p /root/.ssh
COPY ssh_key/* /root/.ssh/

RUN chmod -R 600 /root/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

ARG SCANWEBGIS_TAG=master

RUN mkdir -p /usr/src/
WORKDIR /usr/src
RUN git clone --branch ${SCANWEBGIS_TAG} --depth 1 git@github.com:kartoza/scanwebgis.git

ADD uwsgi.ini /usr/src/scanwebgis/django_app/uwsgi.ini

FROM python:3.7.0-stretch

#RUN mkdir -p /home/web/extra_app

COPY --from=intermediate /usr/src/scanwebgis/django_app/ /home/web/extra_app/

ADD entrypoint.sh /entrypoint.sh

WORKDIR /home/web/extra_app

RUN pip install -r REQUIREMENTS.txt

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uwsgi", "--ini", "uwsgi.ini"]

