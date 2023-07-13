FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel

WORKDIR /code

RUN pip install markupsafe==2.0.1
RUN pip install traitlets==5.1.1
RUN pip install pygments==2.4.1
RUN pip install jupyter

RUN pip install pytest
RUN pip install textblob
RUN pip install transformers

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
RUN apt-get update && apt-get install libgl1 -y
RUN pip install fer