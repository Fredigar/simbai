# 🚀 SIMBA - Guía de Deployment

Guía completa para deployar SIMBA en un servidor Ubuntu.

---

## 📋 Requisitos

### Servidor
- **OS**: Ubuntu 20.04 LTS o superior
- **RAM**: Mínimo 2GB (Recomendado 4GB+)
- **CPU**: 2 cores (Recomendado 4+)
- **Disco**: 20GB disponibles
- **Acceso**: Root o sudo

### Servicios Externos
- API Key de OpenAI **O** Anthropic
- (Opcional) Dominio propio
- (Opcional) Certificado SSL

---

## 🎯 Opción 1: Instalación Automática (Recomendada)

### Paso 1: Descargar el instalador

```bash
# En tu servidor Ubuntu
wget https://raw.githubusercontent.com/TU_USUARIO/simbai/main/backend/install.sh
chmod +x install.sh
```

### Paso 2: Ejecutar instalación

```bash
sudo ./install.sh
```

El script instalará automáticamente:
- ✅ Docker & Docker Compose
- ✅ Dependencias del sistema
- ✅ Estructura de directorios
- ✅ Servicio systemd
- ✅ Script de gestión `simba`

### Paso 3: Clonar el código

```bash
cd /opt/simba
sudo git clone https://github.com/TU_USUARIO/simbai.git backend
```

### Paso 4: Configurar variables de entorno

```bash
sudo nano /opt/simba/.env
```

**Edita el archivo y agrega tus API keys:**

```env
# Database
DB_PASSWORD=tu_password_seguro_aqui

# API Keys (REQUERIDO)
OPENAI_API_KEY=sk-...
# O
ANTHROPIC_API_KEY=sk-ant-...

# Application
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=genera_un_secret_key_seguro
```

### Paso 5: Iniciar SIMBA

```bash
sudo simba start
```

### Paso 6: Verificar instalación

```bash
# Ver estado
sudo simba status

# Ver logs
sudo simba logs

# Verificar endpoint
curl http://localhost/health
```

✅ **¡Listo!** SIMBA está corriendo en tu servidor.

---

## 🔧 Opción 2: Instalación Manual

### 1. Instalar Docker

```bash
# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clonar repositorio

```bash
cd /opt
sudo git clone https://github.com/TU_USUARIO/simbai.git simba
cd simba/backend
```

### 3. Configurar .env

```bash
sudo cp .env.example .env
sudo nano .env
```

### 4. Iniciar con Docker Compose

```bash
# Production
sudo docker-compose -f docker-compose.prod.yml up -d

# Ver logs
sudo docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🌐 Configuración de Dominio y SSL

### Opción A: Con Let's Encrypt (Certificado Gratis)

```bash
# Instalar Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Auto-renovación
sudo certbot renew --dry-run
```

### Opción B: Certificado Propio

```bash
# Copiar certificados
sudo cp fullchain.pem /opt/simba/backend/nginx/ssl/
sudo cp privkey.pem /opt/simba/backend/nginx/ssl/

# Editar nginx config
sudo nano /opt/simba/backend/nginx/nginx.conf
# Descomentar sección HTTPS
```

### Actualizar Nginx config para tu dominio

```bash
sudo nano /opt/simba/backend/nginx/nginx.conf
```

Cambiar `server_name _;` por `server_name tu-dominio.com;`

```bash
# Reiniciar
sudo simba restart
```

---

## 📝 Comandos de Gestión

El script de instalación crea el comando `simba` para gestionar el servicio:

```bash
# Iniciar SIMBA
sudo simba start

# Detener SIMBA
sudo simba stop

# Reiniciar SIMBA
sudo simba restart

# Ver logs en tiempo real
sudo simba logs

# Ver estado de servicios
sudo simba status

# Actualizar desde Git
sudo simba update
```

---

## 🔍 Verificación de Servicios

### Verificar que todos los contenedores estén corriendo:

```bash
sudo docker ps
```

Deberías ver:
- ✅ simba-backend
- ✅ simba-db (PostgreSQL)
- ✅ simba-redis
- ✅ simba-chromadb
- ✅ simba-nginx

### Verificar endpoints:

```bash
# Health check
curl http://localhost/health

# API info
curl http://localhost/

# Chat endpoint (requiere auth)
curl -X POST http://localhost/chat/conversations \
  -H "Content-Type: application/json" \
  -d '{"assistant_id":"ASSISTANT_ID","title":"Test"}'
```

---

## 🔐 Seguridad

### 1. Firewall

```bash
# Habilitar UFW
sudo ufw enable

# Permitir puertos necesarios
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS

# Ver estado
sudo ufw status
```

### 2. Cambiar passwords por defecto

Edita `/opt/simba/.env`:
- `DB_PASSWORD`: Password de PostgreSQL
- `SECRET_KEY`: Clave secreta de la aplicación

### 3. Rate Limiting

El archivo `nginx.conf` incluye rate limiting configurado:
- API general: 10 req/s
- Chat endpoints: 5 req/s

### 4. Actualizaciones

```bash
# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Actualizar SIMBA
sudo simba update
```

---

## 📊 Monitoreo

### Ver logs

```bash
# Logs de todos los servicios
sudo simba logs

# Logs de un servicio específico
sudo docker-compose -f /opt/simba/backend/docker-compose.prod.yml logs backend

# Logs con follow
sudo simba logs -f

# Últimas 100 líneas
sudo docker-compose -f /opt/simba/backend/docker-compose.prod.yml logs --tail=100
```

### Logs guardados

Los logs se guardan en:
- **Application**: `/opt/simba/backend/logs/`
- **Nginx**: `/opt/simba/backend/logs/nginx/`

### Espacio en disco

```bash
# Ver uso de Docker
sudo docker system df

# Limpiar recursos no usados
sudo docker system prune -a
```

---

## 🔄 Backup y Restore

### Backup de base de datos

```bash
# Crear backup
sudo docker exec simba-db pg_dump -U simba simba > backup_$(date +%Y%m%d).sql

# Comprimir
gzip backup_$(date +%Y%m%d).sql
```

### Restore de base de datos

```bash
# Descomprimir
gunzip backup_20231201.sql.gz

# Restaurar
sudo docker exec -i simba-db psql -U simba simba < backup_20231201.sql
```

### Backup de ChromaDB

```bash
# Copiar datos de vectores
sudo cp -r /opt/simba/backend/chroma_data /backup/chroma_backup_$(date +%Y%m%d)
```

---

## ⚡ Optimización para Producción

### 1. Ajustar workers de Uvicorn

En `docker-compose.prod.yml`:
```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Regla general: `workers = (2 x CPU cores) + 1`

### 2. Ajustar conexiones de PostgreSQL

Edita `/opt/simba/backend/docker-compose.prod.yml`:
```yaml
db:
  command: postgres -c max_connections=200
```

### 3. Configurar Redis cache

En tu `.env`:
```env
REDIS_URL=redis://redis:6379/0
```

### 4. Habilitar compresión en Nginx

Ya está configurada en `nginx.conf`:
- ✅ Gzip habilitado
- ✅ Tipos MIME optimizados

---

## 🐛 Troubleshooting

### Error: "Cannot connect to database"

```bash
# Verificar que PostgreSQL está corriendo
sudo docker ps | grep postgres

# Ver logs de PostgreSQL
sudo docker-compose -f /opt/simba/backend/docker-compose.prod.yml logs db

# Reiniciar servicio
sudo simba restart
```

### Error: "ChromaDB connection failed"

```bash
# Verificar ChromaDB
sudo docker ps | grep chroma

# Reiniciar ChromaDB
sudo docker-compose -f /opt/simba/backend/docker-compose.prod.yml restart chromadb
```

### Error: "API key not configured"

```bash
# Verificar .env
sudo cat /opt/simba/.env | grep API_KEY

# Editar .env
sudo nano /opt/simba/.env

# Reiniciar
sudo simba restart
```

### Contenedor no inicia

```bash
# Ver logs del contenedor
sudo docker logs simba-backend

# Ver todos los logs
sudo simba logs

# Reiniciar todo
sudo simba stop
sudo simba start
```

### Alto uso de memoria

```bash
# Ver uso de recursos
sudo docker stats

# Reducir workers en docker-compose.prod.yml
# Cambiar: --workers 4  →  --workers 2
```

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs: `sudo simba logs`
2. Verifica el estado: `sudo simba status`
3. Consulta la documentación: `/opt/simba/backend/README.md`
4. Abre un issue en GitHub

---

## ✅ Checklist de Deployment

Antes de considerar el deployment completo:

- [ ] Docker instalado y funcionando
- [ ] Código clonado en `/opt/simba/backend`
- [ ] Variables de entorno configuradas (`.env`)
- [ ] API keys agregadas (OpenAI o Anthropic)
- [ ] Firewall configurado
- [ ] Servicios iniciados (`simba start`)
- [ ] Health check respondiendo (`/health`)
- [ ] (Opcional) Dominio configurado
- [ ] (Opcional) SSL habilitado
- [ ] (Opcional) Backup programado

---

**¡SIMBA está listo para producción!** 🚀
