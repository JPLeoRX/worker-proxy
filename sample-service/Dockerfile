FROM python:3.8

RUN pip install fastapi==0.63.0
RUN pip install uvicorn==0.13.3
RUN pip install injectable==3.4.4
RUN pip install simplestr

COPY . /fastapi-app
WORKDIR /fastapi-app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7001"]
