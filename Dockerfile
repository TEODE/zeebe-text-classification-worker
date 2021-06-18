FROM python:3.7.10-slim

ENV LOGGING_LEVEL 20

ENV TASK_NAME text-classification

WORKDIR /usr/src/app 

COPY requirements.txt index.py ./
COPY libs ./libs/
COPY models ./models/

RUN pip install -r requirements.txt

CMD ["python", "index.py"]