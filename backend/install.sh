#!/bin/bash

###############################################################################
# SIMBA - Script de Instalación para Ubuntu Server
#
# Este script instala y configura SIMBA en un servidor Ubuntu
###############################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
    echo ""
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "Este script debe ejecutarse como root (usa sudo)"
   exit 1
fi

print_header "SIMBA - Instalación en Ubuntu Server"

# Step 1: Update system
print_info "Actualizando sistema..."
apt-get update
apt-get upgrade -y
print_success "Sistema actualizado"

# Step 2: Install Docker
print_info "Instalando Docker..."
if ! command -v docker &> /dev/null; then
    # Install prerequisites
    apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Add Docker's official GPG key
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Set up repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker Engine
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    print_success "Docker instalado"
else
    print_success "Docker ya está instalado"
fi

# Step 3: Install Docker Compose
print_info "Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose instalado"
else
    print_success "Docker Compose ya está instalado"
fi

# Step 4: Create application directory
print_info "Creando directorio de aplicación..."
APP_DIR="/opt/simba"
mkdir -p $APP_DIR
cd $APP_DIR
print_success "Directorio creado: $APP_DIR"

# Step 5: Create .env file
print_info "Configurando variables de entorno..."
if [ ! -f "$APP_DIR/.env" ]; then
    cat > $APP_DIR/.env << 'ENVEOF'
# Database
DB_PASSWORD=change_this_password_in_production

# API Keys (REQUERIDO - Agrega tus keys)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Application
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=change_this_secret_key_in_production
ENVEOF

    print_success "Archivo .env creado"
    print_info "⚠️  IMPORTANTE: Edita $APP_DIR/.env y agrega tus API keys"
else
    print_info "Archivo .env ya existe"
fi

# Step 6: Create necessary directories
print_info "Creando directorios necesarios..."
mkdir -p $APP_DIR/{data,logs,nginx/ssl}
chmod 755 $APP_DIR/{data,logs}
print_success "Directorios creados"

# Step 7: Configure firewall
print_info "Configurando firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 22/tcp
    print_success "Firewall configurado"
else
    print_info "UFW no instalado, saltando configuración de firewall"
fi

# Step 8: Create systemd service
print_info "Creando servicio systemd..."
cat > /etc/systemd/system/simba.service << 'SERVICEEOF'
[Unit]
Description=SIMBA - Sistema Inteligente de Mensajería
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/simba/backend
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
User=root

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable simba.service
print_success "Servicio systemd creado"

# Step 9: Create management script
print_info "Creando script de gestión..."
cat > /usr/local/bin/simba << 'SCRIPTEOF'
#!/bin/bash
cd /opt/simba/backend

case "$1" in
    start)
        docker-compose -f docker-compose.prod.yml up -d
        echo "✓ SIMBA iniciado"
        ;;
    stop)
        docker-compose -f docker-compose.prod.yml down
        echo "✓ SIMBA detenido"
        ;;
    restart)
        docker-compose -f docker-compose.prod.yml restart
        echo "✓ SIMBA reiniciado"
        ;;
    logs)
        docker-compose -f docker-compose.prod.yml logs -f
        ;;
    status)
        docker-compose -f docker-compose.prod.yml ps
        ;;
    update)
        git pull
        docker-compose -f docker-compose.prod.yml build
        docker-compose -f docker-compose.prod.yml up -d
        echo "✓ SIMBA actualizado"
        ;;
    *)
        echo "Uso: simba {start|stop|restart|logs|status|update}"
        exit 1
        ;;
esac
SCRIPTEOF

chmod +x /usr/local/bin/simba
print_success "Script de gestión creado: simba"

# Final messages
print_header "Instalación Completada"
echo ""
print_success "SIMBA instalado correctamente en $APP_DIR"
echo ""
print_info "Próximos pasos:"
echo ""
echo "1. Copia tu código a $APP_DIR/backend:"
echo "   cd $APP_DIR"
echo "   git clone <tu-repo> backend"
echo ""
echo "2. Edita las variables de entorno:"
echo "   nano $APP_DIR/.env"
echo "   (Agrega OPENAI_API_KEY o ANTHROPIC_API_KEY)"
echo ""
echo "3. Inicia SIMBA:"
echo "   simba start"
echo ""
echo "4. Ver logs:"
echo "   simba logs"
echo ""
echo "5. Ver estado:"
echo "   simba status"
echo ""
echo "Comandos disponibles:"
echo "  simba start   - Iniciar SIMBA"
echo "  simba stop    - Detener SIMBA"
echo "  simba restart - Reiniciar SIMBA"
echo "  simba logs    - Ver logs"
echo "  simba status  - Ver estado"
echo "  simba update  - Actualizar desde git"
echo ""
print_info "SIMBA estará disponible en http://$(hostname -I | awk '{print $1}')"
echo ""
