#!/usr/bin/env python3
"""
Script de configuración para el sistema RAG con Milvus y Ollama
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Ejecutar un comando del sistema"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def check_ollama():
    """Verificar si Ollama está instalado y funcionando"""
    print("🔍 Verificando Ollama...")
    try:
        result = subprocess.run("ollama --version", shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Ollama encontrado: {result.stdout.strip()}")
        
        # Verificar si el modelo qwen3:4b está disponible
        result = subprocess.run("ollama list", shell=True, check=True, capture_output=True, text=True)
        if "qwen3:4b" in result.stdout:
            print("✅ Modelo qwen3:4b encontrado")
            return True
        else:
            print("⚠️  Modelo qwen3:4b no encontrado. Descargando...")
            return run_command("ollama pull qwen3:4b", "Descarga del modelo qwen3:4b")
    except subprocess.CalledProcessError:
        print("❌ Ollama no está instalado o no está funcionando")
        print("Por favor, instala Ollama desde: https://ollama.ai/")
        return False

def check_docker():
    """Verificar si Docker está instalado"""
    print("🔍 Verificando Docker...")
    try:
        result = subprocess.run("docker --version", shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Docker encontrado: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Docker no está instalado")
        print("Por favor, instala Docker desde: https://docs.docker.com/get-docker/")
        return False

def install_python_dependencies():
    """Instalar dependencias de Python"""
    print("📦 Instalando dependencias de Python...")
    return run_command(f"{sys.executable} -m pip install -r requirements.txt", "Instalación de dependencias")

def setup_environment():
    """Configurar archivo de entorno"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creando archivo .env...")
        with open(env_file, "w") as f:
            f.write("""# Configuración de Ollama y Milvus
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_MODEL=qwen3:4b
MILVUS_HOST=localhost
MILVUS_PORT=19530
""")
        print("✅ Archivo .env creado")
    else:
        print("✅ Archivo .env ya existe")

def main():
    """Función principal de configuración"""
    print("🚀 CONFIGURACIÓN DEL SISTEMA RAG")
    print("="*40)
    
    # Verificar Ollama
    if not check_ollama():
        print("❌ Configuración fallida: Ollama no disponible")
        sys.exit(1)
    
    # Verificar Docker
    if not check_docker():
        print("❌ Configuración fallida: Docker no disponible")
        sys.exit(1)
    
    # Configurar entorno
    setup_environment()
    
    # Instalar dependencias
    if not install_python_dependencies():
        print("❌ Configuración fallida: Error instalando dependencias")
        sys.exit(1)
    
    print("\n🎉 CONFIGURACIÓN COMPLETADA")
    print("="*40)
    print("Siguiente pasos:")
    print("1. Ejecuta: ./start_milvus.sh (para iniciar Milvus)")
    print("2. Ejecuta: python example.py (para probar el sistema)")
    print("\nAsegúrate de que Ollama esté ejecutándose en segundo plano.")

if __name__ == "__main__":
    main()
