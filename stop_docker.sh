#!/bin/bash

# Script para detener el sistema RAG dockerizado

echo "🛑 Deteniendo sistema RAG..."

# Detener y eliminar contenedores
if command -v docker-compose &> /dev/null; then
    docker-compose down
else
    docker compose down
fi

echo "✅ Sistema RAG detenido exitosamente!"

# Mostrar información sobre volúmenes
echo ""
echo "💾 Los datos persisten en volúmenes Docker:"
echo "   - ollama_data (modelos de Ollama)"
echo "   - milvus_data (datos de Milvus)"
echo ""
echo "Para eliminar todos los datos:"
echo "   docker-compose down -v"
