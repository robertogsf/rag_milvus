#!/bin/bash

# Script avanzado para gestión del sistema RAG dockerizado

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}🐳 Gestor del Sistema RAG Dockerizado${NC}"
    echo ""
    echo "Uso: $0 [COMANDO] [OPCIONES]"
    echo ""
    echo "Comandos:"
    echo "  start         Iniciar el sistema (desarrollo)"
    echo "  start-prod    Iniciar el sistema (producción)"
    echo "  stop          Detener el sistema"
    echo "  restart       Reiniciar el sistema"
    echo "  status        Ver estado de los servicios"
    echo "  logs          Ver logs en tiempo real"
    echo "  test          Ejecutar pruebas"
    echo "  shell         Acceder al contenedor de la app"
    echo "  clean         Limpiar contenedores y volúmenes"
    echo "  backup        Hacer backup de los datos"
    echo "  restore       Restaurar datos desde backup"
    echo "  update        Actualizar imágenes y reiniciar"
    echo "  health        Verificar salud de los servicios"
    echo "  help          Mostrar esta ayuda"
    echo ""
    echo "Opciones:"
    echo "  --dev         Incluir servicios de desarrollo (Jupyter)"
    echo "  --build       Forzar rebuild de imágenes"
    echo "  --verbose     Mostrar output detallado"
}

# Función para verificar dependencias
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
        echo -e "${RED}❌ Docker Compose no está instalado${NC}"
        exit 1
    fi
}

# Función para ejecutar docker-compose
run_compose() {
    if command -v docker-compose &> /dev/null; then
        docker-compose "$@"
    else
        docker compose "$@"
    fi
}

# Función para iniciar servicios
start_services() {
    local env_file="docker-compose.yml"
    local profile=""
    local build_arg=""
    
    if [[ "$1" == "prod" ]]; then
        env_file="docker-compose.prod.yml"
        echo -e "${YELLOW}🚀 Iniciando en modo PRODUCCIÓN${NC}"
    else
        echo -e "${YELLOW}🚀 Iniciando en modo DESARROLLO${NC}"
    fi
    
    if [[ "$*" == *"--dev"* ]]; then
        profile="--profile dev"
    fi
    
    if [[ "$*" == *"--build"* ]]; then
        build_arg="--build"
    fi
    
    echo -e "${BLUE}🛑 Deteniendo servicios existentes...${NC}"
    run_compose -f "$env_file" down 2>/dev/null || true
    
    echo -e "${BLUE}🔨 Iniciando servicios...${NC}"
    run_compose -f "$env_file" up -d $build_arg $profile
    
    echo -e "${BLUE}⏳ Esperando a que los servicios estén listos...${NC}"
    sleep 10
    
    show_status "$env_file"
    show_urls
}

# Función para mostrar estado
show_status() {
    local env_file="${1:-docker-compose.yml}"
    echo -e "${BLUE}📊 Estado de los servicios:${NC}"
    run_compose -f "$env_file" ps
}

# Función para mostrar URLs
show_urls() {
    echo ""
    echo -e "${GREEN}✅ Sistema RAG iniciado exitosamente!${NC}"
    echo ""
    echo -e "${BLUE}🔗 URLs de acceso:${NC}"
    echo "   - Ollama: http://localhost:11434"
    echo "   - Milvus: http://localhost:19530"
    echo "   - Milvus Web UI: http://localhost:9091"
    echo "   - Jupyter (si está activo): http://localhost:8888"
    echo ""
}

# Función para ver logs
show_logs() {
    local service="${1:-}"
    if [[ -n "$service" ]]; then
        run_compose logs -f "$service"
    else
        run_compose logs -f
    fi
}

# Función para ejecutar pruebas
run_tests() {
    echo -e "${BLUE}🧪 Ejecutando pruebas del sistema...${NC}"
    run_compose exec rag-app python test_docker.py
}

# Función para verificar salud
check_health() {
    echo -e "${BLUE}🏥 Verificando salud de los servicios...${NC}"
    
    # Verificar Ollama
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        echo -e "${GREEN}✅ Ollama: Saludable${NC}"
    else
        echo -e "${RED}❌ Ollama: No disponible${NC}"
    fi
    
    # Verificar Milvus
    if curl -s http://localhost:9091/health > /dev/null; then
        echo -e "${GREEN}✅ Milvus: Saludable${NC}"
    else
        echo -e "${RED}❌ Milvus: No disponible${NC}"
    fi
    
    # Verificar contenedores
    echo ""
    run_compose ps
}

# Función para hacer backup
backup_data() {
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    echo -e "${BLUE}💾 Creando backup en $backup_dir...${NC}"
    
    # Backup de Milvus
    docker run --rm \
        -v rag_milvus_milvus_data:/data \
        -v "$(pwd)/$backup_dir":/backup \
        ubuntu tar czf /backup/milvus_backup.tar.gz -C /data .
    
    # Backup de Ollama
    docker run --rm \
        -v rag_milvus_ollama_data:/data \
        -v "$(pwd)/$backup_dir":/backup \
        ubuntu tar czf /backup/ollama_backup.tar.gz -C /data .
    
    echo -e "${GREEN}✅ Backup completado en $backup_dir${NC}"
}

# Función para restaurar backup
restore_data() {
    local backup_dir="${1:-}"
    if [[ -z "$backup_dir" ]]; then
        echo -e "${RED}❌ Especifica el directorio de backup${NC}"
        echo "Uso: $0 restore <directorio_backup>"
        exit 1
    fi
    
    if [[ ! -d "$backup_dir" ]]; then
        echo -e "${RED}❌ Directorio de backup no existe: $backup_dir${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}⚠️  Esto sobrescribirá los datos actuales. ¿Continuar? (y/N)${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Operación cancelada"
        exit 0
    fi
    
    echo -e "${BLUE}🔄 Restaurando desde $backup_dir...${NC}"
    
    # Detener servicios
    run_compose down
    
    # Restaurar Milvus
    if [[ -f "$backup_dir/milvus_backup.tar.gz" ]]; then
        docker run --rm \
            -v rag_milvus_milvus_data:/data \
            -v "$(pwd)/$backup_dir":/backup \
            ubuntu tar xzf /backup/milvus_backup.tar.gz -C /data
    fi
    
    # Restaurar Ollama
    if [[ -f "$backup_dir/ollama_backup.tar.gz" ]]; then
        docker run --rm \
            -v rag_milvus_ollama_data:/data \
            -v "$(pwd)/$backup_dir":/backup \
            ubuntu tar xzf /backup/ollama_backup.tar.gz -C /data
    fi
    
    echo -e "${GREEN}✅ Restauración completada${NC}"
    echo -e "${BLUE}🚀 Iniciando servicios...${NC}"
    start_services
}

# Función para limpiar
clean_system() {
    echo -e "${YELLOW}⚠️  Esto eliminará todos los contenedores y volúmenes. ¿Continuar? (y/N)${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Operación cancelada"
        exit 0
    fi
    
    echo -e "${BLUE}🧹 Limpiando sistema...${NC}"
    run_compose down -v --remove-orphans
    docker system prune -f
    echo -e "${GREEN}✅ Sistema limpiado${NC}"
}

# Script principal
main() {
    check_dependencies
    
    case "${1:-help}" in
        start)
            start_services dev "${@:2}"
            ;;
        start-prod)
            start_services prod "${@:2}"
            ;;
        stop)
            echo -e "${BLUE}🛑 Deteniendo servicios...${NC}"
            run_compose down
            echo -e "${GREEN}✅ Servicios detenidos${NC}"
            ;;
        restart)
            echo -e "${BLUE}🔄 Reiniciando servicios...${NC}"
            run_compose restart
            show_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs "${2:-}"
            ;;
        test)
            run_tests
            ;;
        shell)
            run_compose exec rag-app bash
            ;;
        clean)
            clean_system
            ;;
        backup)
            backup_data
            ;;
        restore)
            restore_data "${2:-}"
            ;;
        update)
            echo -e "${BLUE}🔄 Actualizando imágenes...${NC}"
            run_compose pull
            start_services dev --build
            ;;
        health)
            check_health
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ Comando desconocido: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar script principal
main "$@"
