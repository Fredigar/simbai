# SIMBA Frontend

Frontend moderno para SIMBA (Sistema Inteligente de Mensajería con Backend Avanzado) construido con Framework7.

## 🚀 Características

- ✨ **Interfaz de chat moderna** con mensajes en tiempo real
- 🔄 **Streaming de respuestas** para experiencia fluida
- 📁 **Subida de archivos** (PDF, DOCX, TXT)
- 🔍 **RAG Avanzado** con búsqueda semántica
- 💬 **Múltiples conversaciones** con historial
- ⚙️ **Configuración flexible** (modelo LLM, temperatura, etc.)
- 📱 **Responsive** - funciona en móvil, tablet y desktop
- 🎨 **Diseño Material** con Framework7

## 📋 Requisitos

- Un navegador web moderno (Chrome, Firefox, Safari, Edge)
- Backend de SIMBA corriendo (por defecto en http://82.223.12.60:8000)
- Servidor web para servir archivos estáticos (Python, Nginx, Apache, etc.)

## 🛠️ Instalación y Despliegue

### Opción 1: Servidor Python Simple (Desarrollo/Testing)

```bash
# En el servidor Ubuntu (donde está SIMBA)
cd /ruta/a/frontend-new

# Iniciar servidor HTTP en puerto 3000
python3 -m http.server 3000

# O en segundo plano
nohup python3 -m http.server 3000 > /dev/null 2>&1 &
```

Acceder en: http://82.223.12.60:3000

### Opción 2: Nginx (Producción Recomendada)

```bash
# 1. Copiar frontend a directorio web
sudo mkdir -p /var/www/simba-frontend
sudo cp -r * /var/www/simba-frontend/

# 2. Crear configuración de Nginx
sudo nano /etc/nginx/sites-available/simba-frontend
```

Contenido del archivo de configuración:

```nginx
server {
    listen 3000;
    server_name _;

    root /var/www/simba-frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Habilitar compresión
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Cache de assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 3. Activar sitio
sudo ln -s /etc/nginx/sites-available/simba-frontend /etc/nginx/sites-enabled/

# 4. Verificar configuración
sudo nginx -t

# 5. Reiniciar Nginx
sudo systemctl restart nginx
```

Acceder en: http://82.223.12.60:3000

### Opción 3: Junto con el Backend

Si quieres servir el frontend desde el mismo Nginx que sirve el backend:

```bash
# 1. Copiar frontend al directorio de SIMBA
sudo cp -r /ruta/a/frontend-new /opt/simba/frontend

# 2. Modificar nginx.conf del backend para incluir el frontend
# Agregar location para el frontend
```

## ⚙️ Configuración

### Backend URL

Por defecto, el frontend se conecta a: `http://82.223.12.60:8000`

Para cambiar esto:

1. Abre el frontend en tu navegador
2. Haz clic en el icono de **Configuración** (⚙️)
3. Modifica "Backend URL"
4. Los cambios se guardan automáticamente en localStorage

O edita directamente `js/config.js`:

```javascript
const AppConfig = {
    backend: {
        baseURL: 'http://tu-servidor:8000',
        // ...
    },
    // ...
};
```

## 🎯 Uso

### 1. Crear una Nueva Conversación

- Haz clic en el botón **+** en la barra superior
- O haz clic en "Iniciar Nueva Conversación" en la pantalla de bienvenida

### 2. Enviar Mensajes

- Escribe tu mensaje en el campo de texto
- Presiona **Enter** o haz clic en el botón de **enviar** (→)
- Las respuestas se mostrarán en tiempo real con streaming

### 3. Subir Archivos

- Haz clic en el icono de **clip** (📎)
- Selecciona archivos PDF, DOCX o TXT
- Los archivos se subirán e indexarán automáticamente para RAG

### 4. Ver Conversaciones Anteriores

- Haz clic en el icono de **menú** (☰) en la esquina superior izquierda
- Selecciona una conversación de la lista

### 5. Configuración

Personaliza la experiencia:
- **Modelo LLM**: GPT-4, GPT-3.5, Claude 3, etc.
- **Temperatura**: Controla la creatividad de las respuestas (0-2)
- **Streaming**: Activa/desactiva respuestas en tiempo real

## 📁 Estructura del Proyecto

```
frontend-new/
├── index.html          # Página principal
├── css/
│   └── app.css        # Estilos personalizados
├── js/
│   ├── config.js      # Configuración de la app
│   ├── api.js         # Cliente API para backend
│   └── app.js         # Lógica principal Framework7
└── README.md          # Esta documentación
```

## 🔧 Desarrollo

### Modificar Estilos

Edita `css/app.css` para personalizar la apariencia.

### Modificar Funcionalidad

- `js/config.js`: Configuración general
- `js/api.js`: Llamadas al backend
- `js/app.js`: Lógica de la interfaz

### Debug

Abre la consola del navegador (F12) para ver logs:

```javascript
// Acceder al estado de la app
console.log(AppState);

// Acceder a la instancia de Framework7
console.log(simbaApp);

// Ver configuración
console.log(AppConfig);
```

## 🌐 Compatibilidad

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🐛 Solución de Problemas

### El frontend no se conecta al backend

1. Verifica que el backend esté corriendo:
   ```bash
   curl http://82.223.12.60:8000/health
   ```

2. Verifica la URL del backend en Configuración

3. Revisa la consola del navegador (F12) para errores

### Los mensajes no se envían

1. Asegúrate de haber creado una conversación
2. Verifica que el backend tenga una API key configurada (OpenAI o Anthropic)
3. Revisa los logs del backend:
   ```bash
   sudo docker compose -f /opt/simba/backend/docker-compose.prod.yml logs backend
   ```

### Los archivos no se suben

1. Verifica que el archivo sea PDF, DOCX o TXT
2. Verifica que el tamaño sea menor a 50MB
3. Revisa los logs del backend para errores de procesamiento

## 📝 Notas

- El frontend es 100% estático (HTML/CSS/JS)
- No requiere compilación ni build
- Todas las dependencias se cargan desde CDN
- Los datos de conversaciones se almacenan en el backend
- La configuración se guarda en localStorage del navegador

## 🚀 Producción

Para producción, considera:

1. **SSL/HTTPS**: Configura certificados SSL
2. **CDN**: Opcionalmente, sirve assets desde CDN
3. **Compresión**: Habilita gzip en Nginx
4. **Cache**: Configura headers de cache apropiados
5. **Monitoreo**: Agrega analytics o monitoreo de errores

## 📄 Licencia

MIT License - Ver LICENSE en el repositorio principal de SIMBA.

---

**¿Necesitas ayuda?** Revisa la documentación completa en SIMBA o abre un issue en GitHub.
