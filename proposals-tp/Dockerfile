FROM python:3.8

RUN pip install sawtooth-sdk cbor

WORKDIR /project
COPY . .

ENV PATH "$PATH:/project/tp"
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION 'python'

ENTRYPOINT ["python3", "main.py"]
