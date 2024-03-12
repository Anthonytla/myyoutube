FROM node:14.18.1

# Install node modules
#RUN npm install -g nodemon
COPY . .
WORKDIR .
# Create app directory
#RUN mkdir -p /usr/src/app/
#WORKDIR /usr/src/app/

RUN npm install

#ENV HOST 0.0.0.0
# Install app dependencies
#CMD [ "npm", "run", "buildStart"]