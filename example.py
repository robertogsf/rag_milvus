#!/usr/bin/env python3
"""
Ejemplo de uso del sistema RAG con Milvus y Ollama (Qwen3:4b)
"""

from rag_system import RAGSystem
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Función principal de ejemplo"""
    try:
        # Inicializar el sistema RAG
        print("🚀 Inicializando sistema RAG con Ollama...")
        rag = RAGSystem()
        
        # Documentos de ejemplo
        documentos_ejemplo = [
            """
            Python es un lenguaje de programación interpretado cuya filosofía hace hincapié en la legibilidad de su código.
            Se trata de un lenguaje de programación multiparadigma, ya que soporta orientación a objetos, programación 
            imperativa y, en menor medida, programación funcional. Es un lenguaje interpretado, dinámico y multiplataforma.
            """,
            """
            Milvus es una base de datos vectorial de código abierto construida para alimentar aplicaciones de inteligencia artificial.
            Ofrece almacenamiento, indexación y gestión consistente de embeddings vectoriales generados por modelos de deep learning
            y otras técnicas de machine learning. Milvus hace que sea fácil construir aplicaciones AI robustas y escalables.
            """,
            """
            RAG (Retrieval-Augmented Generation) es una técnica que combina la recuperación de información con la generación de texto.
            Funciona recuperando documentos relevantes de una base de datos y luego usando esa información como contexto para 
            generar respuestas más precisas y fundamentadas. Es especialmente útil para crear chatbots y sistemas de preguntas
            y respuestas que necesitan acceso a información específica de dominio.
            """,
            """
            Los embeddings son representaciones vectoriales densas de texto que capturan el significado semántico de las palabras
            o frases. Se generan utilizando modelos de deep learning como BERT, GPT o sentence transformers. Estos vectores
            permiten realizar búsquedas semánticas, donde se pueden encontrar textos similares en significado aunque no
            compartan las mismas palabras exactas.
            """,
            """
            La inteligencia artificial generativa es una rama de la IA que se enfoca en crear contenido nuevo, como texto,
            imágenes, música o código. Los modelos como GPT-3, GPT-4, DALL-E y Stable Diffusion son ejemplos de IA generativa.
            Estos modelos aprenden patrones de grandes cantidades de datos y pueden generar contenido original que es
            coherente y contextualmente relevante.
            """
        ]
        
        # Añadir documentos al sistema
        print("📚 Añadiendo documentos al sistema...")
        rag.add_documents(documentos_ejemplo)
        print("✅ Documentos añadidos exitosamente")
        
        # Realizar consultas de ejemplo
        preguntas = [
            "¿Qué es Python?",
            "¿Cómo funciona RAG?",
            "¿Qué son los embeddings?",
            "¿Para qué sirve Milvus?",
            "¿Qué es la inteligencia artificial generativa?"
        ]
        
        print("\n" + "="*50)
        print("🤖 INICIANDO CONSULTAS RAG")
        print("="*50)
        
        for i, pregunta in enumerate(preguntas, 1):
            print(f"\n📝 Pregunta {i}: {pregunta}")
            print("-" * 40)
            
            # Hacer la consulta
            resultado = rag.ask(pregunta)
            
            # Mostrar la respuesta
            print(f"💬 Respuesta: {resultado['answer']}")
            
            # Mostrar fuentes (opcional)
            if resultado['sources']:
                print(f"\n📖 Fuentes consultadas ({len(resultado['sources'])}):")
                for j, fuente in enumerate(resultado['sources'][:2], 1):  # Mostrar solo las 2 primeras
                    print(f"   {j}. {fuente['text']} (Score: {fuente['score']:.4f})")
            
            print()
        
        print("="*50)
        print("✅ Demostración completada exitosamente!")
        
        # Ejemplo interactivo
        print("\n🎯 Modo interactivo - Haz tu propia pregunta:")
        print("(Presiona Enter sin texto para salir)")
        
        while True:
            pregunta_usuario = input("\n❓ Tu pregunta: ").strip()
            
            if not pregunta_usuario:
                break
                
            resultado = rag.ask(pregunta_usuario)
            print(f"\n💬 Respuesta: {resultado['answer']}")
        
        print("\n👋 ¡Hasta luego!")
        
    except Exception as e:
        logger.error(f"Error en la demostración: {e}")
        print(f"❌ Error: {e}")
        print("\n💡 Asegúrate de que:")
        print("   1. Milvus esté ejecutándose (docker run -p 19530:19530 milvusdb/milvus:latest)")
        print("   2. Tienes configurada tu API key de OpenAI en el archivo .env")
        print("   3. Todas las dependencias están instaladas (pip install -r requirements.txt)")

if __name__ == "__main__":
    main()
