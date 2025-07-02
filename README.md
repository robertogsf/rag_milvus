# Sistema RAG con Milvus y Ollama

Este proyecto implementa un sistema RAG (Retrieval-Augmented Generation) usando Milvus como base de datos vectorial y Ollama con el modelo Qwen3:4b para la generación de respuestas.

## 🚀 Características

- **Base de datos vectorial**: Milvus para almacenamiento y búsqueda de embeddings
- **Modelo local**: Ollama con Qwen3:4b (sin necesidad de API keys externas)
- **Embeddings**: Sentence Transformers para generar embeddings de texto
- **Búsqueda semántica**: Encuentra documentos relevantes basándose en similitud vectorial
- **Generación aumentada**: Combina recuperación y generación para respuestas contextuales
- **🐳 Dockerizado**: Aislamiento completo en contenedores para fácil despliegue

## 📋 Opciones de instalación

### Opción 1: 🐳 Docker (Recomendado)

La forma más fácil y aislada de ejecutar el sistema:

#### Requisitos:
- Docker
- Docker Compose

#### Instalación rápida:

```bash
# Clonar o descargar el proyecto
cd rag_milvus

# Iniciar todo el sistema
./start_docker.sh
```

El script automáticamente:
- Construye la imagen de la aplicación
- Descarga e inicia Ollama con el modelo Qwen3:4b
- Inicia Milvus con persistencia de datos
- Configura la red entre contenedores
- Ejecuta pruebas del sistema

#### Servicios disponibles:
- **Ollama**: `http://localhost:11434`
- **Milvus**: `http://localhost:19530`
- **Milvus Web UI**: `http://localhost:9091`
- **Jupyter (opcional)**: `http://localhost:8888`

#### Comandos útiles:

```bash
# Gestor avanzado (recomendado)
./rag_manager.sh start          # Iniciar desarrollo
./rag_manager.sh start-prod     # Iniciar producción  
./rag_manager.sh stop           # Detener
./rag_manager.sh status         # Ver estado
./rag_manager.sh logs           # Ver logs
./rag_manager.sh test           # Ejecutar pruebas
./rag_manager.sh health         # Verificar salud
./rag_manager.sh backup         # Hacer backup
./rag_manager.sh clean          # Limpiar todo
./rag_manager.sh help           # Ver ayuda completa

# Comandos básicos alternativos
./start_docker.sh               # Iniciar el sistema
./stop_docker.sh                # Detener el sistema

# Docker Compose directo
docker-compose up -d            # Iniciar servicios
docker-compose logs -f          # Ver logs en tiempo real
docker-compose exec rag-app python test_docker.py  # Ejecutar pruebas
docker-compose exec rag-app bash                   # Acceder al contenedor
docker-compose --profile dev up -d jupyter         # Iniciar Jupyter
```

### Opción 2: 🔧 Instalación local

#### Requisitos previos

1. **Python 3.8+**
2. **Docker** - Para ejecutar Milvus
3. **Ollama** - Para el modelo de lenguaje local

#### Instalación de Ollama:

```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar el modelo Qwen3:4b
ollama pull qwen3:4b
```

#### Instalación de Docker:
Sigue las instrucciones en [docs.docker.com](https://docs.docker.com/get-docker/)

## 🛠️ Instalación (Local)

1. **Clona o descarga el proyecto**

2. **Ejecuta el script de configuración:**
```bash
python setup.py
```

Este script:
- Verifica que Ollama y Docker estén instalados
- Descarga el modelo Qwen3:4b si no está disponible
- Instala las dependencias de Python
- Configura el archivo `.env`

3. **Inicia Milvus:**
```bash
chmod +x start_milvus.sh
./start_milvus.sh
```

## 🎯 Uso

### Ejemplo básico:

```bash
python example.py
```

### Uso programático:

```python
from rag_system import RAGSystem

# Inicializar el sistema
rag = RAGSystem()

# Añadir documentos
documentos = [
    "Python es un lenguaje de programación...",
    "Milvus es una base de datos vectorial...",
    # ... más documentos
]
rag.add_documents(documentos)

# Hacer una consulta
respuesta = rag.query("¿Qué es Python?")
print(respuesta)
```

## 📁 Estructura del proyecto

```
rag_with_milvus/
├── .env                   # Configuración de entorno (local)
├── .env.docker           # Configuración de entorno (Docker)
├── .dockerignore         # Archivos ignorados por Docker
├── Dockerfile            # Imagen de la aplicación
├── docker-compose.yml    # Orquestación de servicios (desarrollo)
├── docker-compose.prod.yml # Orquestación optimizada (producción)
├── nginx.conf            # Configuración de Nginx
├── requirements.txt      # Dependencias de Python
├── setup.py             # Script de configuración (local)
├── start_milvus.sh      # Script para iniciar Milvus (local)
├── start_docker.sh      # Script básico para Docker
├── stop_docker.sh       # Script básico para detener Docker
├── rag_manager.sh       # Gestor avanzado del sistema
├── milvus_client.py     # Cliente para interactuar con Milvus
├── rag_system.py        # Sistema RAG principal
├── example.py           # Ejemplo de uso
├── test_docker.py       # Pruebas completas para Docker
├── data/                # Directorio para datos
├── logs/                # Directorio para logs
└── backups/             # Directorio para backups automáticos
```

## ⚙️ Configuración

### Docker (Recomendado)

La configuración para Docker está en `.env.docker`:

```properties
# Configuración de Ollama
OLLAMA_HOST=ollama
OLLAMA_PORT=11434
OLLAMA_MODEL=qwen3:4b

# Configuración de Milvus
MILVUS_HOST=milvus
MILVUS_PORT=19530
```

### Local

El archivo `.env` contiene la configuración del sistema:

```properties
# Configuración de Ollama
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_MODEL=qwen3:4b

# Configuración de Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

## 🔧 Personalización

### Cambiar el modelo de Ollama:

1. Descarga otro modelo: `ollama pull modelo:tag`
2. Actualiza `OLLAMA_MODEL` en `.env`

### Cambiar el modelo de embeddings:

Modifica la variable `MODEL_NAME` en `milvus_client.py`:

```python
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

### Ajustar parámetros de búsqueda:

En `rag_system.py`, modifica los parámetros de búsqueda:

```python
# Número de documentos a recuperar
TOP_K = 5

# Parámetros de generación
options={
    "temperature": 0.7,    # Creatividad (0.0 - 1.0)
    "num_predict": 500     # Longitud máxima de respuesta
}
```

## 🐛 Solución de problemas

### Docker

1. **Error: "docker" no encontrado**
   - Instala Docker: [docs.docker.com](https://docs.docker.com/get-docker/)
   - Verifica instalación: `docker --version`

2. **Error: "docker-compose" no encontrado**
   - Instala Docker Compose o usa `docker compose`
   - Verifica: `docker-compose --version`

3. **Puertos ocupados**
   - Verifica puertos libres: `netstat -tlnp | grep -E '(11434|19530|9091)'`
   - Modifica puertos en `docker-compose.yml` si es necesario

4. **Problemas de permisos**
   - En Linux: `sudo usermod -aG docker $USER` (reiniciar sesión)
   - Ejecutar: `chmod +x start_docker.sh stop_docker.sh`

5. **Contenedores no inician correctamente**
   - Ver logs: `docker-compose logs`
   - Reiniciar: `docker-compose restart`
   - Limpiar: `docker-compose down -v && docker-compose up --build`

### Local (Instalación tradicional)

### Problemas comunes:

1. **Error: "ollama" no encontrado**
   - Verifica que Ollama esté instalado: `ollama --version`
   - Asegúrate de que esté en el PATH

2. **Error: Modelo no encontrado**
   - Descarga el modelo: `ollama pull qwen3:4b`
   - Verifica modelos disponibles: `ollama list`

3. **Error: No se puede conectar a Milvus**
   - Verifica que Docker esté ejecutándose
   - Ejecuta: `./start_milvus.sh`
   - Verifica que el puerto 19530 esté libre

4. **Error: Dependencias de Python**
   - Actualiza pip: `pip install --upgrade pip`
   - Instala dependencias: `pip install -r requirements.txt`

### Verificar el estado de los servicios:

#### Docker:
```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs
docker-compose logs -f

# Estadísticas de recursos
docker stats
```

#### Local:

```bash
# Verificar Ollama
ollama list

# Verificar Milvus (Docker)
docker ps | grep milvus

# Verificar puertos
netstat -tlnp | grep -E '(11434|19530)'
```

## 📊 Monitoreo

### Docker:
- **Contenedores**: `docker-compose ps`
- **Logs**: `docker-compose logs -f [servicio]`
- **Recursos**: `docker stats`
- **Milvus Web UI**: `http://localhost:9091`

### Local:
- **Ollama**: `http://localhost:11434`
- **Milvus**: Puerto 19530
- **Logs**: Los logs se muestran en la consola durante la ejecución

## 🔄 Migración de datos

### Backup automático:
```bash
# Usando el gestor avanzado
./rag_manager.sh backup

# Los backups se guardan en ./backups/YYYYMMDD_HHMMSS/
```

### Restaurar datos:
```bash
./rag_manager.sh restore ./backups/20250102_143000
```

### Backup manual:
```bash
# Hacer backup de volúmenes manualmente
docker run --rm -v rag_milvus_milvus_data:/data -v $(pwd):/backup ubuntu tar czf /backup/milvus_backup.tar.gz -C /data .
docker run --rm -v rag_milvus_ollama_data:/data -v $(pwd):/backup ubuntu tar czf /backup/ollama_backup.tar.gz -C /data .
```

## 🏭 Producción

Para usar en producción, utiliza la configuración optimizada:

```bash
# Iniciar en modo producción
./rag_manager.sh start-prod

# O con docker-compose directamente
docker-compose -f docker-compose.prod.yml up -d

# Con Nginx como proxy (opcional)
docker-compose -f docker-compose.prod.yml --profile nginx up -d
```

### Diferencias en producción:
- **Recursos limitados**: Memoria y CPU controlados
- **Reinicio automático**: `restart: always`
- **Healthchecks mejorados**: Más robustos
- **Configuración de cache**: Optimizada para Milvus
- **Logs persistentes**: Configuración para logging
- **Nginx opcional**: Para balanceador de carga
