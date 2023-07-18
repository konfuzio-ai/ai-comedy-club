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

RUN apt-get install libglib2.0-0 -y
RUN pip install opencv-python

RUN pip install --upgrade Flask-SocketIO==4.3.1 python-engineio==3.13.2 python-socketio==4.6.0 Flask==2.0.3 Werkzeug==2.0.3 opencv_python==4.7.0.68 gunicorn==20.1.0 eventlet==0.30.2

RUN apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall netbase

RUN pip install --upgrade protobuf==3.20.1 tensorflow==2.3.0 pillow==8.3.2 numpy==1.20.3