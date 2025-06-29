#!/bin/bash
set -e

echo "⏳ Esperando a que PostgreSQL esté listo..."

until pg_isready -h db -p 5432 -U admin; do
  sleep 1
done

echo "✅ PostgreSQL está listo."

# Opcional: migraciones automáticas si usás Flask-Migrate
# flask db upgrade

echo "🚀 Iniciando el servidor Flask..."
flask run --host=0.0.0.0 --port=5000 