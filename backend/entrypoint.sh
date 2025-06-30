#!/bin/bash
set -e

echo "⏳ Esperando a que PostgreSQL esté listo..."

until pg_isready -h db -p 5432 -U admin; do
  sleep 1
done

echo "✅ PostgreSQL está listo."

# Iniciamo la aplicación sin migraciones automáticas por ahora
echo "🚀 Iniciando el servidor Flask..."
flask run --host=0.0.0.0 --port=5000 