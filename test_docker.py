#!/usr/bin/env python3
"""
Script de prueba para el sistema RAG dockerizado
"""

import os
import time
import logging
from rag_system import RAGSystem
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/rag_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def wait_for_services():
    """Esperar a que los servicios estén disponibles"""
    logger.info("Esperando a que los servicios estén disponibles...")
    
    # Esperar a Ollama
    max_retries = 30
    for i in range(max_retries):
        try:
            import ollama
            ollama_host = os.getenv('OLLAMA_HOST', 'localhost')
            ollama_port = os.getenv('OLLAMA_PORT', '11434')
            client = ollama.Client(host=f'http://{ollama_host}:{ollama_port}')
            client.list()
            logger.info("✅ Ollama está disponible")
            break
        except Exception as e:
            if i == max_retries - 1:
                logger.error(f"❌ No se pudo conectar a Ollama después de {max_retries} intentos")
                raise
            logger.info(f"⏳ Esperando a Ollama... ({i+1}/{max_retries})")
            time.sleep(2)
    
    # Esperar a Milvus
    for i in range(max_retries):
        try:
            from pymilvus import connections
            milvus_host = os.getenv('MILVUS_HOST', 'localhost')
            milvus_port = os.getenv('MILVUS_PORT', '19530')
            connections.connect(host=milvus_host, port=milvus_port)
            connections.disconnect("default")
            logger.info("✅ Milvus está disponible")
            break
        except Exception as e:
            if i == max_retries - 1:
                logger.error(f"❌ No se pudo conectar a Milvus después de {max_retries} intentos")
                raise
            logger.info(f"⏳ Esperando a Milvus... ({i+1}/{max_retries})")
            time.sleep(2)

def main():
    """Función principal de prueba"""
    try:
        logger.info("🚀 Iniciando prueba del sistema RAG")
        
        # Cargar variables de entorno
        load_dotenv()
        
        # Esperar a que los servicios estén listos
        wait_for_services()
        
        # Inicializar el sistema RAG
        logger.info("🔧 Inicializando sistema RAG...")
        rag = RAGSystem()
        
        # Documentos de ejemplo
        documentos_ejemplo = [
            "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Es conocido por su sintaxis clara y legible.",
            "Milvus es una base de datos vectorial de código abierto construida para manejar embeddings vectoriales y búsquedas de similitud.",
            "RAG (Retrieval-Augmented Generation) es una técnica que combina la recuperación de información relevante con la generación de texto.",
            "Docker es una plataforma que permite desarrollar, enviar y ejecutar aplicaciones en contenedores.",
            "Ollama es una herramienta que permite ejecutar modelos de lenguaje grandes localmente en tu máquina.",
            "Los embeddings son representaciones vectoriales de texto que capturan el significado semántico de las palabras.",
            "La búsqueda semántica utiliza embeddings para encontrar contenido similar basándose en el significado, no solo en palabras clave."
        ]
        
        # Añadir documentos al sistema
        logger.info("📄 Añadiendo documentos al sistema...")
        rag.add_documents(documentos_ejemplo)
        
        # Realizar consultas de ejemplo
        consultas = [
            "¿Qué es Python?",
            "¿Cómo funciona Milvus?",
            "Explícame qué es RAG",
            "¿Para qué sirve Docker?",
            "¿Qué son los embeddings?"
        ]
        
        logger.info("❓ Realizando consultas de ejemplo...")
        for i, consulta in enumerate(consultas, 1):
            logger.info(f"\n--- Consulta {i}: {consulta} ---")
            try:
                respuesta = rag.query(consulta)
                logger.info(f"Respuesta: {respuesta}")
            except Exception as e:
                logger.error(f"Error en consulta '{consulta}': {e}")
        
        logger.info("\n✅ Prueba completada exitosamente!")
        
    except Exception as e:
        logger.error(f"❌ Error en la prueba: {e}")
        raise

if __name__ == "__main__":
    main()
