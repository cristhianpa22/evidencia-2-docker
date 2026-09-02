FROM python:3.10-slim
RUN apt-get update && apt-get upgrade -y
WORKDIR /home/capsdevp/Documentos/workspace/docker/evidencia_2/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python3", "sample_app.py"]

