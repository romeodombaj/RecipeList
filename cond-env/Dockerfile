FROM python:3.11.4
WORKDIR /app
COPY requirements.txt req.txt
RUN pip3 install -r req.txt
COPY . .
CMD ["python3", "app.py"]
