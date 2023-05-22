# Dockerfile
FROM python:3.11.3
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
ENV FLASK_APP=app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]