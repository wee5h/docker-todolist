FROM python:3.11-slim

WORKDIR /api

COPY requirements.txt requirements.txt 

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

#CMD directly invokes a command, rather than running it through shell, on the startup of a container.
CMD ["flask", "run"]
