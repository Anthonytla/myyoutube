FROM openjdk:8-jdk-alpine

WORKDIR /app

COPY pom.xml ./
COPY static ./static
COPY src ./src

RUN apk add --update maven