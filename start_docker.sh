#!/bin/bash

# Script para iniciar el sistema RAG dockerizado

echo "🐳 Iniciando sistema RAG con Docker Compose..."

# Verificar si Docker y Docker Compose están instalados
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true

# Construir e iniciar los servicios
echo "🔨 Construyendo e iniciando servicios..."
if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 20

# Verificar el estado de los servicios
echo "📊 Estado de los servicios:"
if command -v docker-compose &> /dev/null; then
    docker-compose ps
else
    docker compose ps
fi

echo ""
echo "✅ Sistema RAG iniciado exitosamente!"
echo ""
echo "🔗 URLs de acceso:"
echo "   - Ollama: http://localhost:11434"
echo "   - Milvus: http://localhost:19530"
echo "   - Milvus Web UI: http://localhost:9091"
echo ""
echo "📝 Comandos útiles:"
echo "   - Ver logs: docker-compose logs -f"
echo "   - Detener: docker-compose down"
echo "   - Reiniciar: docker-compose restart"
echo "   - Ejecutar ejemplo: docker-compose exec rag-app python example.py"
echo ""
echo "🧪 Para desarrollo con Jupyter:"
echo "   docker-compose --profile dev up -d jupyter"
echo "   Jupyter estará disponible en: http://localhost:8888"
