FROM python:3.8

RUN pip install cbor sawtooth-sdk==1.2.5

WORKDIR /project
# COPY . .

ENV PATH "$PATH:/project/tp"
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION 'python'

ENTRYPOINT ["python3", "main.py"]
