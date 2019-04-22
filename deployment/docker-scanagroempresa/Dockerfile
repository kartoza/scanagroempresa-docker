FROM python:3.7.0-stretch

# This section taken on 2 July 2015 from
# https://docs.docker.com/examples/running_ssh_service/
# Sudo is needed by pycharm when it tries to pip install packages
RUN apt-get update && apt-get install -y openssh-server sudo
RUN mkdir /var/run/sshd
RUN echo 'root:docker' | chpasswd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

ADD REQUIREMENTS.txt REQUIREMENTS.txt

RUN pip install -r REQUIREMENTS.txt

# Install orca via npm
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
# orca depends on the following packages
RUN apt update -y; apt install -y nodejs xvfb libxtst6 libgconf-2-4 libnss3-dev libasound2
RUN npm install -g --unsafe-perm=true electron@1.8.4 orca@1.2.1

## use xvfb to run orca
RUN rm /usr/bin/orca
ADD orca.sh /usr/bin/orca

RUN apt update; apt install -y postgresql-client

ADD entrypoint.sh /entrypoint.sh

ADD wait-for-databases.sh /wait-for-databases.sh

ADD wait-for-kobo-cache-databases.sh /wait-for-kobo-cache-databases.sh

WORKDIR /home/web/extra_app

EXPOSE 22
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/usr/sbin/sshd", "-D"]

