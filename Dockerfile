FROM python

WORKDIR /app
COPY . .
RUN apt-get update && apt-get install tesseract-ocr -y
RUN pip install -r requirements.txt

CMD ["python", "main.py"]