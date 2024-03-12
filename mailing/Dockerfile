FROM node:latest

# Install node modules
#RUN npm install -g nodemon

COPY . \app
WORKDIR \app

RUN apt-get -y update
ENV DOCKER_VERSION=20.10.9

RUN DEBIAN_FRONTEND=noninteractive apt-get install mailutils nano -y 
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install postfix
RUN npm install --save express

CMD ["/etc/init.d/postfix", "restart"]