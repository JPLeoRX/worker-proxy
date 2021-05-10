FROM python:3.8

RUN pip install fastapi==0.63.0
RUN pip install uvicorn==0.13.3
RUN pip install injectable==3.4.4
RUN pip install requests==2.25.1
RUN pip install pika==1.1.0
RUN pip install simplestr==0.3

COPY ./proxy-shared-message-protocol /proxy-shared-message-protocol
WORKDIR /proxy-shared-message-protocol
RUN python setup.py sdist bdist_wheel
RUN pip install .

COPY ./proxy-shared-utils /proxy-shared-utils
WORKDIR /proxy-shared-utils
RUN python setup.py sdist bdist_wheel
RUN pip install .

COPY ./proxy-client /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7777"]
