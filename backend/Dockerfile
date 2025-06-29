FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema, incluyendo postgresql-client para pg_isready
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Asegurar que el script de entrada sea ejecutable
RUN chmod +x entrypoint.sh

# Crear un endpoint de salud para healthchecks
RUN echo 'from flask import Flask\napp = Flask(__name__)\n@app.route("/api/health")\ndef health():\n    return {"status": "healthy"}, 200\n\nif __name__ == "__main__":\n    app.run(host="0.0.0.0", port=5000)' > health_check.py

EXPOSE 5000 