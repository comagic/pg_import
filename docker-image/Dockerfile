FROM python:3.10

RUN apt-get update && apt-get -y install postgresql-client
RUN pip install pg-import

COPY ./cmd.sh /cmd.sh

CMD ["/cmd.sh"]
