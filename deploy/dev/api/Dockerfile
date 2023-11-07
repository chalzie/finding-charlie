FROM python:3.9

WORKDIR /opt

COPY ./deploy/reqs.txt ./reqs.txt

RUN pip install --no-cache-dir --upgrade -r reqs.txt

COPY ./api ./api

CMD ["uvicorn", "api.app:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
