#FROM python:3.11-slim
#
#WORKDIR /flask_api_exam
#
#COPY . .
#
#ENV PYTHONPATH=/flask_api_exam
#
#RUN pip install --no-cache-dir -r requirements.txt
#
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]


FROM python:3.11-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
