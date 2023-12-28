FROM python:3.10

RUN pip install --trusted-host pip.uis.st --extra-index-url http://pip.uis.st/simple/ pg-import

COPY ./cmd.sh /cmd.sh

CMD '/cmd.sh'
