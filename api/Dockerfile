FROM python:3.8

WORKDIR .

COPY requirements.txt ./
RUN apt-get -y update && apt-get -y install ffmpeg && pip3 install --no-cache-dir -r requirements.txt
RUN apt-get -y update

COPY . .

CMD [ "python3","-u", "./api.py" ]