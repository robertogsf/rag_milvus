import os
import logging
from typing import List, Dict, Any
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class MilvusClient:
    """Cliente para gestionar operaciones con Milvus"""
    
    def __init__(self, host: str = None, port: str = None):
        self.host = host or os.getenv('MILVUS_HOST', 'localhost')
        self.port = port or os.getenv('MILVUS_PORT', '19530')
        self.collection_name = "documents"
        self.collection = None
        
        # Inicializar el modelo de embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # Dimensión del modelo all-MiniLM-L6-v2
        
    def connect(self):
        """Conectar a Milvus"""
        try:
            connections.connect("default", host=self.host, port=self.port)
            logger.info(f"Conectado a Milvus en {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Error al conectar con Milvus: {e}")
            raise
    
    def create_collection(self):
        """Crear la colección si no existe"""
        try:
            # Verificar si la colección ya existe
            if utility.has_collection(self.collection_name):
                logger.info(f"La colección '{self.collection_name}' ya existe")
                self.collection = Collection(self.collection_name)
                return
            
            # Definir el schema de la colección
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.embedding_dim)
            ]
            
            schema = CollectionSchema(fields, "Colección para documentos RAG")
            
            # Crear la colección
            self.collection = Collection(self.collection_name, schema)
            logger.info(f"Colección '{self.collection_name}' creada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al crear la colección: {e}")
            raise
    
    def create_index(self):
        """Crear índice para búsqueda vectorial"""
        try:
            index_params = {
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            
            self.collection.create_index("embedding", index_params)
            logger.info("Índice creado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al crear el índice: {e}")
            raise
    
    def insert_documents(self, texts: List[str]):
        """Insertar documentos en la colección"""
        try:
            # Generar embeddings
            embeddings = self.encoder.encode(texts)
            
            # Preparar datos para inserción
            data = [
                texts,
                embeddings.tolist()
            ]
            
            # Insertar datos
            mr = self.collection.insert(data)
            self.collection.flush()
            
            logger.info(f"Insertados {len(texts)} documentos exitosamente")
            return mr
            
        except Exception as e:
            logger.error(f"Error al insertar documentos: {e}")
            raise
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Buscar documentos similares"""
        try:
            # Cargar la colección en memoria
            self.collection.load()
            
            # Generar embedding de la consulta
            query_embedding = self.encoder.encode([query])
            
            # Parámetros de búsqueda
            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 10}
            }
            
            # Realizar búsqueda
            results = self.collection.search(
                query_embedding,
                "embedding",
                search_params,
                limit=top_k,
                output_fields=["text"]
            )
            
            # Formatear resultados
            similar_docs = []
            for hits in results:
                for hit in hits:
                    similar_docs.append({
                        "text": hit.entity.get("text"),
                        "score": hit.score,
                        "id": hit.id
                    })
            
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error en la búsqueda: {e}")
            raise
    
    def delete_collection(self):
        """Eliminar la colección"""
        try:
            if utility.has_collection(self.collection_name):
                utility.drop_collection(self.collection_name)
                logger.info(f"Colección '{self.collection_name}' eliminada")
        except Exception as e:
            logger.error(f"Error al eliminar la colección: {e}")
            raise
