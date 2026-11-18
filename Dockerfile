FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i '1s/^\xEF\xBB\xBF//; s/\r$//' entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]