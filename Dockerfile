FROM python:3.7-slim

RUN apt update 
RUN apt -y upgrade 
RUN apt install -y build-essential
# RUN apt install -y supervisor 

# RUN echo "files = /etc/supervisor/conf.d/*.ini" >> /etc/supervisor/supervisord.conf

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# create user 
ARG user=genesis
ARG group=genesis
ARG uid=1000
ARG gid=1001
RUN adduser ${user}

USER ${user}
RUN mkdir /home/${user}/src
RUN mkdir /home/${user}/log
RUN mkdir -p /home/${user}/src/telegram/log

# cp project files 
ADD app/ /home/${user}/src/app/
ADD telegram/ home/${user}/src/telegram/
ADD config.py /home/${user}/src
# ADD supervisord-conf/genesisapi.ini /etc/supervisor/conf.d/genesisapi.ini
# ADD supervisord-conf/telegram.ini /etc/supervisor/conf.d/telegram.ini
ADD genesis-gunicorn.sh /home/${user}/src/

# EXPOSE 8080

# USER root
# RUN chmod -R a+rw /home/${user}/src/telegram/log/

CMD ["sh", "/home/genesis/src/genesis-gunicorn.sh"]
# CMD ["supervisord","--nodaemon","-c", "/etc/supervisor/supervisord.conf"]