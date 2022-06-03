FROM python:3.8

RUN pip install sawtooth-sdk cbor

WORKDIR /project
# COPY . .

### to compile settings proto file ###
######################################
# RUN PROTOC_ZIP=protoc-3.14.0-linux-x86_64.zip \
#     curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.14.0/$PROTOC_ZIP \
#     sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc \
#     sudo unzip -o $PROTOC_ZIP -d /usr/local 'include/*' \
#     rm -f $PROTOC_ZIP
# RUN wget https://raw.githubusercontent.com/hyperledger/sawtooth-core/main/families/settings/protos/settings.proto
# RUN protoc -I=. --python_out=./tp/ settings.proto
######################################

ENV PATH "$PATH:/project/tp"

ENTRYPOINT ["python3", "main.py"]
