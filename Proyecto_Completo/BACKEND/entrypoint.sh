#!/bin/bash
set -e

echo "Generando cliente Prisma..."
prisma generate

echo "Iniciando aplicación Flask..."
exec python app.py
