#!/bin/bash

# Script para iniciar Milvus con Docker

echo "🚀 Iniciando Milvus con Docker..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Detener contenedor existente si está corriendo
echo "🛑 Deteniendo contenedor Milvus existente (si existe)..."
docker stop milvus-standalone 2>/dev/null || true
docker rm milvus-standalone 2>/dev/null || true

# Crear directorio para datos de Milvus
mkdir -p $(pwd)/volumes/milvus

# Iniciar Milvus standalone
echo "🐳 Iniciando contenedor Milvus..."
docker run -d \
  --name milvus-standalone \
  --security-opt seccomp:unconfined \
  -e ETCD_USE_EMBED=true \
  -e ETCD_DATA_DIR=/var/lib/milvus/etcd \
  -e COMMON_STORAGETYPE=local \
  -v $(pwd)/volumes/milvus:/var/lib/milvus \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:latest

# Esperar a que Milvus esté listo
echo "⏳ Esperando a que Milvus esté listo..."
sleep 10

# Verificar si el contenedor está corriendo
if docker ps | grep -q milvus-standalone; then
    echo "✅ Milvus iniciado exitosamente!"
    echo "📡 Milvus está disponible en localhost:19530"
    echo "🌐 Milvus Web UI disponible en http://localhost:9091"
    echo ""
    echo "Para detener Milvus, ejecuta:"
    echo "docker stop milvus-standalone"
else
    echo "❌ Error al iniciar Milvus"
    echo "Logs del contenedor:"
    docker logs milvus-standalone
fi
