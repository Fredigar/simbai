# Guía de Instalación de SIMBA en Ubuntu

Esta guía te llevará paso a paso para instalar SIMBA en tu servidor Ubuntu 82.223.12.60.

## Paso 1: Conectarse al Servidor

```bash
ssh usuario@82.223.12.60
```

## Paso 2: Descargar y Ejecutar el Instalador Automatizado

```bash
# Descargar el script de instalación
wget https://raw.githubusercontent.com/Fredigar/simbai/claude/architect-coding-standards-01YKsKujq3VoAYWmtBxdaaVq/backend/install.sh

# Dar permisos de ejecución
chmod +x install.sh

# Ejecutar el instalador (instalará Docker, Docker Compose, y configurará todo)
sudo ./install.sh
```

El instalador hará automáticamente:
- ✅ Instalar Docker y Docker Compose
- ✅ Crear el directorio `/opt/simba`
- ✅ Configurar el servicio systemd
- ✅ Crear el comando de gestión `simba`
- ✅ Configurar el firewall (UFW)

## Paso 3: Clonar el Repositorio

```bash
# Cambiar al directorio de SIMBA
cd /opt/simba

# Clonar el repositorio
sudo git clone -b claude/architect-coding-standards-01YKsKujq3VoAYWmtBxdaaVq https://github.com/Fredigar/simbai.git backend

# Entrar al directorio backend
cd backend
```

## Paso 4: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
sudo cp .env.example .env

# Editar el archivo .env
sudo nano .env
```

Configura las siguientes variables importantes:

```env
# Configuración General
DEBUG=False
SECRET_KEY=GENERA_UNA_CLAVE_SECRETA_AQUI

# Base de Datos (cambia la contraseña)
DB_PASSWORD=TuPasswordSegura123!
DATABASE_URL=postgresql+asyncpg://simba:TuPasswordSegura123!@db:5432/simba

# APIs de LLMs (al menos una es necesaria)
OPENAI_API_KEY=sk-...tu-api-key-de-openai...
# O
ANTHROPIC_API_KEY=sk-ant-...tu-api-key-de-anthropic...

# Servicios (estas ya están configuradas correctamente)
REDIS_URL=redis://redis:6379/0
CHROMA_HOST=chromadb
CHROMA_PORT=8000
```

**Para generar una SECRET_KEY segura**, ejecuta:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Guarda el archivo presionando `Ctrl+X`, luego `Y`, luego `Enter`.

## Paso 5: Iniciar SIMBA

```bash
# Iniciar todos los servicios
sudo simba start

# Ver el estado de los servicios
sudo simba status

# Ver los logs en tiempo real (opcional)
sudo simba logs
```

Los servicios que se iniciarán son:
- **Backend FastAPI** (puerto 8000)
- **PostgreSQL** (base de datos)
- **Redis** (caché)
- **ChromaDB** (vectores para RAG)
- **Nginx** (proxy reverso, puerto 80)

## Paso 6: Verificar la Instalación

```bash
# Verificar que todos los contenedores estén corriendo
sudo docker ps

# Verificar el health check del backend
curl http://localhost/health

# Ver los logs del backend
sudo simba logs backend
```

Deberías ver una respuesta JSON del health check:
```json
{"status":"ok"}
```

## Paso 7: Acceder a SIMBA

Una vez que todo esté corriendo, puedes acceder a SIMBA en:

- **API**: http://82.223.12.60
- **Documentación API**: http://82.223.12.60/docs
- **Health Check**: http://82.223.12.60/health

## Comandos de Gestión

El instalador crea el comando `simba` para gestionar fácilmente el sistema:

```bash
sudo simba start      # Iniciar todos los servicios
sudo simba stop       # Detener todos los servicios
sudo simba restart    # Reiniciar todos los servicios
sudo simba status     # Ver estado de los servicios
sudo simba logs       # Ver logs en tiempo real
sudo simba update     # Actualizar SIMBA desde GitHub
```

## Configuración Opcional: Dominio y SSL

Si tienes un dominio apuntando a tu servidor, puedes configurar HTTPS:

```bash
# Instalar Certbot
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Editar la configuración de Nginx para tu dominio
sudo nano /opt/simba/backend/nginx/nginx.conf
# Cambia 'your-domain.com' por tu dominio real

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# Reiniciar Nginx
sudo simba restart nginx
```

## Solución de Problemas

### Ver logs de un servicio específico
```bash
sudo simba logs backend    # Logs del backend
sudo simba logs db         # Logs de PostgreSQL
sudo simba logs nginx      # Logs de Nginx
```

### Reiniciar un servicio específico
```bash
cd /opt/simba/backend
sudo docker-compose -f docker-compose.prod.yml restart backend
```

### Verificar puertos abiertos
```bash
sudo netstat -tlnp | grep -E ':(80|8000|5432|6379)'
```

### Si los contenedores no inician
```bash
# Ver logs detallados
sudo simba logs

# Verificar el archivo .env
sudo cat /opt/simba/.env

# Reiniciar desde cero
sudo simba stop
sudo simba start
```

## Seguridad

**Importante**: Después de la instalación:

1. **Cambia las contraseñas por defecto** en el archivo `.env`
2. **Configura el firewall**:
   ```bash
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # HTTP
   sudo ufw allow 443/tcp   # HTTPS
   sudo ufw enable
   ```
3. **Configura SSL/HTTPS** para producción (ver sección opcional arriba)
4. **Mantén las API keys seguras** - nunca las compartas ni las commits a GitHub

## Monitoreo

Para monitorear el uso de recursos:

```bash
# Ver uso de CPU/memoria de contenedores
sudo docker stats

# Ver espacio en disco
df -h

# Ver logs del sistema
sudo journalctl -u simba.service -f
```

## Backups

Para hacer backup de la base de datos:

```bash
# Crear backup
sudo docker exec -t simba-db-1 pg_dump -U simba simba > backup_$(date +%Y%m%d).sql

# Restaurar backup
sudo docker exec -i simba-db-1 psql -U simba simba < backup_20231215.sql
```

---

## ¿Necesitas Ayuda?

Si encuentras algún problema durante la instalación:

1. Revisa los logs: `sudo simba logs`
2. Verifica que todas las variables de entorno estén configuradas correctamente
3. Asegúrate de que tienes al menos una API key configurada (OpenAI o Anthropic)
4. Verifica que los puertos 80, 8000, 5432, 6379 no estén siendo usados por otros servicios

---

**¡Listo!** SIMBA debería estar corriendo en tu servidor Ubuntu.
