#!/bin/bash
# SIMBA Frontend - Script de Despliegue Rápido

set -e

echo "=========================================="
echo "  SIMBA Frontend - Despliegue"
echo "=========================================="
echo ""

# Detectar directorio actual
if [ -d "/root/backend" ]; then
    REPO_DIR="/root/backend"
elif [ -d "/opt/simba/backend" ]; then
    REPO_DIR="/opt/simba"
else
    echo "❌ No se encontró el repositorio de SIMBA"
    exit 1
fi

echo "📁 Repositorio encontrado en: $REPO_DIR"

# Actualizar desde GitHub
echo "📥 Actualizando desde GitHub..."
cd $REPO_DIR
git pull origin claude/architect-coding-standards-01YKsKujq3VoAYWmtBxdaaVq

# Verificar que frontend-new existe
if [ ! -d "$REPO_DIR/frontend-new" ]; then
    echo "❌ No se encontró el directorio frontend-new"
    exit 1
fi

# Preguntar puerto
read -p "¿En qué puerto quieres desplegar el frontend? (default: 3000): " PORT
PORT=${PORT:-3000}

# Verificar si el puerto está ocupado
if netstat -tuln | grep -q ":$PORT "; then
    echo "⚠️  El puerto $PORT ya está en uso"
    read -p "¿Quieres detener el servicio actual? (s/n): " STOP
    if [ "$STOP" = "s" ]; then
        # Intentar matar procesos en ese puerto
        sudo fuser -k ${PORT}/tcp 2>/dev/null || true
        sleep 2
    else
        echo "❌ Cancelado"
        exit 1
    fi
fi

# Iniciar servidor
echo "🚀 Iniciando frontend en puerto $PORT..."
cd $REPO_DIR/frontend-new

# Matar proceso anterior si existe
pkill -f "http.server $PORT" 2>/dev/null || true

# Iniciar en segundo plano
nohup python3 -m http.server $PORT > /tmp/simba-frontend.log 2>&1 &
FRONTEND_PID=$!

# Esperar un momento
sleep 2

# Verificar que está corriendo
if ps -p $FRONTEND_PID > /dev/null; then
    echo ""
    echo "=========================================="
    echo "✅ Frontend desplegado exitosamente!"
    echo "=========================================="
    echo ""
    echo "📍 URL: http://$(hostname -I | awk '{print $1}'):$PORT"
    echo "📊 PID: $FRONTEND_PID"
    echo "📝 Logs: /tmp/simba-frontend.log"
    echo ""
    echo "Para detener el frontend:"
    echo "  kill $FRONTEND_PID"
    echo "  # O:"
    echo "  pkill -f 'http.server $PORT'"
    echo ""
    echo "Para ver logs:"
    echo "  tail -f /tmp/simba-frontend.log"
    echo ""
else
    echo "❌ Error al iniciar el frontend"
    echo "Ver logs: cat /tmp/simba-frontend.log"
    exit 1
fi
