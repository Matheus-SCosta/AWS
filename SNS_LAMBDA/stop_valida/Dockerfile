FROM ubuntu:20.04
RUN apt update -y \
    && apt install curl unzip python3-pip -y \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \ 
    && unzip awscliv2.zip \ 
    && ./aws/install \
    && pip install boto3 moto
ADD stop.py /home/ubuntu/
ENTRYPOINT [ "python3", "/home/ubuntu/stop.py" ]
