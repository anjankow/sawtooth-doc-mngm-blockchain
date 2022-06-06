FROM python:3.8

RUN pip install sawtooth-sdk cbor

WORKDIR /project
# COPY . .

ENV PATH "$PATH:/project/tp"

ENTRYPOINT ["python3", "main.py"]
