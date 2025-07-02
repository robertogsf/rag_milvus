import os
import ollama
from typing import List, Dict, Any
from milvus_client import MilvusClient
from dotenv import load_dotenv
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class RAGSystem:
    """Sistema RAG (Retrieval-Augmented Generation) con Milvus y Ollama"""
    
    def __init__(self):
        # Configurar Ollama
        self.ollama_host = os.getenv('OLLAMA_HOST', 'localhost')
        self.ollama_port = os.getenv('OLLAMA_PORT', '11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'qwen3:4b')
        
        # Configurar cliente Ollama
        self.ollama_client = ollama.Client(host=f'http://{self.ollama_host}:{self.ollama_port}')
        
        # Inicializar cliente de Milvus
        self.milvus_client = MilvusClient()
        
        # Conectar y configurar Milvus
        self.setup_milvus()
    
    def setup_milvus(self):
        """Configurar Milvus"""
        try:
            self.milvus_client.connect()
            self.milvus_client.create_collection()
            self.milvus_client.create_index()
            logger.info("Milvus configurado exitosamente")
        except Exception as e:
            logger.error(f"Error configurando Milvus: {e}")
            raise
    
    def add_documents(self, documents: List[str]):
        """Añadir documentos al sistema"""
        try:
            # Dividir documentos en chunks si son muy largos
            chunks = []
            for doc in documents:
                chunks.extend(self._split_text(doc))
            
            # Insertar en Milvus
            self.milvus_client.insert_documents(chunks)
            logger.info(f"Añadidos {len(chunks)} chunks de documentos")
            
        except Exception as e:
            logger.error(f"Error añadiendo documentos: {e}")
            raise
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Dividir texto en chunks más pequeños"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Intentar cortar en un punto natural (espacio, punto, etc.)
            if end < len(text):
                last_space = chunk.rfind(' ')
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                
                # Usar el último separador natural encontrado
                cut_point = max(last_space, last_period, last_newline)
                if cut_point > start + chunk_size // 2:  # Solo si no está muy al principio
                    chunk = text[start:start + cut_point + 1]
                    end = start + cut_point + 1
            
            chunks.append(chunk.strip())
            start = max(end - overlap, start + 1)  # Evitar bucles infinitos
            
            if start >= len(text):
                break
        
        return [chunk for chunk in chunks if chunk]  # Filtrar chunks vacíos
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Recuperar contexto relevante para una consulta"""
        try:
            similar_docs = self.milvus_client.search_similar(query, top_k)
            logger.info(f"Recuperados {len(similar_docs)} documentos relevantes")
            return similar_docs
        except Exception as e:
            logger.error(f"Error recuperando contexto: {e}")
            raise
    
    def generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generar respuesta usando OpenAI GPT"""
        try:
            # Construir el contexto
            context = "\n\n".join([doc["text"] for doc in context_docs])
            
            # Construir el prompt
            prompt = f"""Basándote en el siguiente contexto, responde a la pregunta de manera precisa y detallada.

Contexto:
{context}

Pregunta: {query}

Respuesta:"""
            
            # Llamar a Ollama
            response = self.ollama_client.chat(
                model=self.ollama_model,
                messages=[
                    {"role": "system", "content": "Eres un asistente útil que responde preguntas basándose en el contexto proporcionado. Si la información no está en el contexto, indícalo claramente."},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "temperature": 0.7,
                    "num_predict": 500
                }
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            raise
    
    def ask(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """Método principal para hacer preguntas al sistema RAG"""
        try:
            # Recuperar contexto relevante
            context_docs = self.retrieve_context(question, top_k)
            
            if not context_docs:
                return {
                    "question": question,
                    "answer": "No se encontró información relevante para responder tu pregunta.",
                    "sources": []
                }
            
            # Generar respuesta
            answer = self.generate_response(question, context_docs)
            
            # Preparar fuentes
            sources = [
                {
                    "text": doc["text"][:200] + "..." if len(doc["text"]) > 200 else doc["text"],
                    "score": doc["score"]
                }
                for doc in context_docs
            ]
            
            return {
                "question": question,
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error en consulta RAG: {e}")
            return {
                "question": question,
                "answer": f"Error procesando la consulta: {str(e)}",
                "sources": []
            }
    
    def reset_database(self):
        """Reiniciar la base de datos (eliminar todos los documentos)"""
        try:
            self.milvus_client.delete_collection()
            self.setup_milvus()
            logger.info("Base de datos reiniciada")
        except Exception as e:
            logger.error(f"Error reiniciando base de datos: {e}")
            raise
