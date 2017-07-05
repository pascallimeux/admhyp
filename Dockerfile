FROM python:3.6-slim
MAINTAINER Pascal Limeux <pascal.limeux@orange.com>

# Set env variables
ENV GOPATH=/opt/gopath
# select config.ProductionConfig for production
#ENV APP_SETTINGS=config.ProductionConfig
ENV APP_SETTINGS=config.DevelopmentConfig

# Install Linux packages
RUN apt-get update && apt-get install -y openssh-server
RUN apt-get install -y build-essential python-dev gcc
RUN apt-get install -y libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev
RUN apt-get install -y nginx supervisor
# remove next line in production
RUN apt-get install -y nano net-tools

# Setup credentials
RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh
COPY ./keys/id_rsa /root/.ssh/id_rsa
COPY ./keys/id_rsa.pub /root/.ssh/id_rsa.pub
RUN chmod 600 /root/.ssh/id_rsa && chmod 600 /root/.ssh/id_rsa.pub

# Setup application
RUN mkdir -p /opt/gopath/src/github.com/hyperledger
RUN mkdir /app
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install -r requirements.txt
COPY . /app

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY ./docker_conf/app.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/app.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord / gunicorn
RUN mkdir -p /var/log/supervisor
COPY ./docker_conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# Start process
EXPOSE  8080
CMD ["/usr/bin/supervisord"]

#EXPOSE  8000
#CMD ["python", "/app/src/run.py", "-p 8000"]