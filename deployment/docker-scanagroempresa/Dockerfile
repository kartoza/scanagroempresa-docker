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

# install anaconda so we can use conda installer package manager
RUN wget https://repo.anaconda.com/archive/Anaconda2-2019.03-Linux-x86_64.sh -O ~/anaconda.sh
RUN bash ~/anaconda.sh -b -p $HOME/anaconda
# set env so we could always access anaconda
RUN echo "PATH=$PATH:$HOME/anaconda/bin" >> ~/.bashrc
# set env so we could install orca
ENV PATH="$PATH:$HOME/anaconda/bin"

RUN conda install -y -c plotly plotly-orca
# orca depends on the following packages
RUN apt-get -y install xvfb libxtst6 libgconf-2-4 libnss3-dev libasound2

RUN apt update; apt install -y postgresql-client

ADD entrypoint.sh /entrypoint.sh

ADD wait-for-databases.sh /wait-for-databases.sh

ADD wait-for-kobo-cache-databases.sh /wait-for-kobo-cache-databases.sh

WORKDIR /home/web/extra_app

EXPOSE 22
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/usr/sbin/sshd", "-D"]

