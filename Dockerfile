FROM python:3.10-slim

RUN apt-get update && apt-get install -y poppler-utils

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
