FROM python:3.8

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -U -r requirements.txt

CMD ["python", "-u", "run.py"]
