# Sistema RAG con Milvus y Ollama

Este proyecto implementa un sistema RAG (Retrieval-Augmented Generation) usando Milvus como base de datos vectorial y Ollama con el modelo Qwen3:4b para la generación de respuestas.

## 🚀 Características

- **Base de datos vectorial**: Milvus para almacenamiento y búsqueda de embeddings
- **Modelo local**: Ollama con Qwen3:4b (sin necesidad de API keys externas)
- **Embeddings**: Sentence Transformers para generar embeddings de texto
- **Búsqueda semántica**: Encuentra documentos relevantes basándose en similitud vectorial
- **Generación aumentada**: Combina recuperación y generación para respuestas contextuales

## 📋 Requisitos previos

### Software necesario:

1. **Python 3.8+**
2. **Docker** - Para ejecutar Milvus
3. **Ollama** - Para el modelo de lenguaje local

### Instalación de Ollama:

```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar el modelo Qwen3:4b
ollama pull qwen3:4b
```

### Instalación de Docker:
Sigue las instrucciones en [docs.docker.com](https://docs.docker.com/get-docker/)

## 🛠️ Instalación

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
├── .env                 # Configuración de entorno
├── requirements.txt     # Dependencias de Python
├── setup.py            # Script de configuración
├── start_milvus.sh     # Script para iniciar Milvus
├── milvus_client.py    # Cliente para interactuar con Milvus
├── rag_system.py       # Sistema RAG principal
└── example.py          # Ejemplo de uso
```

## ⚙️ Configuración

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

```bash
# Verificar Ollama
ollama list

# Verificar Milvus (Docker)
docker ps | grep milvus

# Verificar puertos
netstat -tlnp | grep -E '(11434|19530)'
```

## 📊 Monitoreo

- **Ollama**: `http://localhost:11434`
- **Milvus**: Puerto 19530
- **Logs**: Los logs se muestran en la consola durante la ejecución

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 📚 Referencias

- [Milvus Documentation](https://milvus.io/docs)
- [Ollama Documentation](https://ollama.ai/)
- [Sentence Transformers](https://www.sbert.net/)
- [Qwen3 Model](https://huggingface.co/Qwen)
