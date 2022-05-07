FROM python:3.8

RUN pip install sawtooth-sdk
# RUN apt update && apt install -y protobuf-compiler
# RUN protoc  --proto_path=proto --python_out=tp/proto_gen proto/myhandler.proto

WORKDIR /project
COPY . .

ENV PATH "$PATH:/project/tp"

ENTRYPOINT ["python3", "main.py"]
