FROM python:3.12.3-alpine3.19

RUN apk add --no-cache libpcap-dev gcc musl-dev

RUN pip3 install scapy requests

COPY agent.py /agent.py

USER root

CMD [ "python", "/agent.py" ]