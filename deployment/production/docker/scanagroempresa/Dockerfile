# Create intermediate image
FROM python:3.7.0-stretch as intermediate

RUN mkdir -p /root/.ssh
COPY ssh_key/* /root/.ssh/

RUN chmod -R 600 /root/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

ARG SCANAGROEMPRESA_TAG=master

RUN mkdir -p /usr/src/
WORKDIR /usr/src
RUN git clone --branch ${SCANAGROEMPRESA_TAG} --depth 1 git@github.com:kartoza/scanagroempresa.git

ADD uwsgi.ini.tpl /usr/src/scanagroempresa/django_app/uwsgi.ini.tpl

RUN rm -f /usr/src/scanagroempresa/django_app/uwsgi.ini

FROM python:3.7.0-stretch

# Install orca via npm
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
# orca depends on the following packages
RUN apt update -y; apt install -y nodejs xvfb libxtst6 libgconf-2-4 libnss3-dev libasound2
RUN npm install -g --unsafe-perm=true electron@1.8.4 orca@1.2.1

# use xvfb to run orca
RUN rm /usr/bin/orca
ADD orca.sh /usr/bin/orca

# Install gdal
RUN apt update -y; apt install -y gdal-bin python3-gdal libgdal-dev
# no python gdal==2.1.2 so we install 2.1.3
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal \
	&& export C_INCLUDE_PATH=/usr/include/gdal \
	&& pip install gdal==2.1.3

COPY --from=intermediate /usr/src/scanagroempresa/django_app/ /home/web/extra_app/

COPY --from=intermediate /usr/src/scanagroempresa/kobo_sync_service/ /home/web/kobo_sync_service/

ADD entrypoint.sh /entrypoint.sh

ADD install-theme-app.sh /install-theme-app.sh

ADD wait-for-databases.sh /wait-for-databases.sh

ADD wait-for-kobo-cache-databases.sh /wait-for-kobo-cache-databases.sh

WORKDIR /home/web/extra_app

RUN pip install -r REQUIREMENTS.txt

RUN pip install -r /home/web/kobo_sync_service/REQUIREMENTS.txt

RUN apt update; apt install -y postgresql-client gettext

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uwsgi", "--ini", "uwsgi.ini"]

