#!/bin/bash
# Script de Instalación Rápida de SIMBA
# Para Ubuntu Server

set -e

echo "=========================================="
echo "  SIMBA - Instalación Rápida"
echo "=========================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Descargar e instalar dependencias
echo -e "${GREEN}[1/5]${NC} Descargando instalador..."
wget -q https://raw.githubusercontent.com/Fredigar/simbai/claude/architect-coding-standards-01YKsKujq3VoAYWmtBxdaaVq/backend/install.sh
chmod +x install.sh

echo -e "${GREEN}[2/5]${NC} Ejecutando instalador (esto puede tomar unos minutos)..."
sudo ./install.sh

# Paso 2: Clonar repositorio
echo -e "${GREEN}[3/5]${NC} Clonando repositorio SIMBA..."
cd /opt/simba
sudo git clone -b claude/architect-coding-standards-01YKsKujq3VoAYWmtBxdaaVq https://github.com/Fredigar/simbai.git backend
cd backend

# Paso 3: Configurar .env
echo -e "${GREEN}[4/5]${NC} Configurando variables de entorno..."
sudo cp .env.example .env

# Generar SECRET_KEY
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
sudo sed -i "s/your-secret-key-here/$SECRET_KEY/" .env

# Generar DB_PASSWORD seguro
DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(16))")
sudo sed -i "s/change_this_password/$DB_PASSWORD/" .env
sudo sed -i "s/PASSWORD/$DB_PASSWORD/" .env

echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE:${NC} Necesitas configurar al menos una API key"
echo ""
echo "Edita el archivo /opt/simba/.env y agrega tu API key:"
echo "  sudo nano /opt/simba/.env"
echo ""
echo "Opciones:"
echo "  - OPENAI_API_KEY=sk-..."
echo "  - ANTHROPIC_API_KEY=sk-ant-..."
echo ""
read -p "Presiona ENTER cuando hayas configurado tu API key..."

# Paso 4: Iniciar servicios
echo -e "${GREEN}[5/5]${NC} Iniciando servicios SIMBA..."
sudo simba start

# Esperar a que los servicios inicien
echo ""
echo "Esperando a que los servicios inicien..."
sleep 10

# Verificar estado
echo ""
echo -e "${GREEN}Estado de los servicios:${NC}"
sudo simba status

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Instalación completada!${NC}"
echo "=========================================="
echo ""
echo "🌐 Accede a SIMBA en:"
echo "   - API: http://$(hostname -I | awk '{print $1}')"
echo "   - Docs: http://$(hostname -I | awk '{print $1}')/docs"
echo ""
echo "📋 Comandos útiles:"
echo "   sudo simba status    # Ver estado"
echo "   sudo simba logs      # Ver logs"
echo "   sudo simba restart   # Reiniciar"
echo "   sudo simba stop      # Detener"
echo ""
echo "📖 Documentación completa: INSTALACION.md"
echo ""
