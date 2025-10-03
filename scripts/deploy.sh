#!/bin/bash

# Script de Deploy para Produção
# Uso: ./scripts/deploy.sh

set -e  # Para o script se algum comando falhar

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verifica se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado!"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado!"
        exit 1
    fi
}

# Verifica se arquivo .env existe
check_env() {
    if [ ! -f ".env" ]; then
        warning "Arquivo .env não encontrado. Copiando do exemplo..."
        cp env.example .env
        warning "IMPORTANTE: Configure as variáveis no arquivo .env antes de continuar!"
        exit 1
    fi
}

# Cria diretórios necessários
create_directories() {
    log "Criando diretórios necessários..."
    mkdir -p logs
    success "Diretórios criados"
}

# Para containers existentes
stop_containers() {
    log "Parando containers existentes..."
    docker-compose -f docker-compose.prod.yml down --remove-orphans || true
    success "Containers parados"
}

# Remove imagens antigas
cleanup_images() {
    log "Removendo imagens antigas..."
    docker image prune -f
    success "Imagens antigas removidas"
}

# Constrói as imagens
build_images() {
    log "Construindo imagens..."
    docker-compose -f docker-compose.prod.yml build --no-cache
    success "Imagens construídas"
}

# Inicia os serviços
start_services() {
    log "Iniciando serviços..."
    docker-compose -f docker-compose.prod.yml up -d
    success "Serviços iniciados"
}

# Verifica se os serviços estão funcionando
health_check() {
    log "Verificando saúde dos serviços..."
    
    # Aguarda os serviços iniciarem
    sleep 30
    
    # Verifica API
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        success "API está funcionando"
    else
        error "API não está respondendo"
        return 1
    fi
}

# Mostra status dos containers
show_status() {
    log "Status dos containers:"
    docker-compose -f docker-compose.prod.yml ps
}

# Mostra logs
show_logs() {
    log "Últimos logs da aplicação:"
    docker-compose -f docker-compose.prod.yml logs --tail=50 backend
}

# Função principal
main() {
    log "🚀 Iniciando deploy da aplicação..."
    
    check_docker
    check_env
    create_directories
    stop_containers
    cleanup_images
    build_images
    start_services
    
    if health_check; then
        success "🎉 Deploy realizado com sucesso!"
        show_status
        log "Aplicação disponível em:"
        log "  - Frontend: http://localhost:8080"
        log "  - API: http://localhost:8000"
        log "  - Docs: http://localhost:8000/docs"
    else
        error "❌ Deploy falhou!"
        show_logs
        exit 1
    fi
}

# Executa função principal
main "$@"
