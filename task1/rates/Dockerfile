FROM python:3.8-slim-buster
ARG ip
ENV doc_ip $ip
COPY . .

RUN pip3 install -U gunicorn
RUN pip3 install -Ur requirements.txt
RUN chmod 777 gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]