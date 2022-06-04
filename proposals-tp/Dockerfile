FROM python:3.8

RUN pip install sawtooth-sdk cbor

WORKDIR /project
# COPY . .

### to compile settings proto file ###
######################################
# RUN apt update && apt install -y protobuf-compiler
# RUN wget https://raw.githubusercontent.com/hyperledger/sawtooth-sdk-python/main/protos/setting.proto
# RUN protoc -I=. --python_out=./tp/ setting.proto
######################################

ENV PATH "$PATH:/project/tp"

ENTRYPOINT ["python3", "main.py"]
