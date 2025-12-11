# SIMBA - Manual Completo de Funcionalidades para el Usuario

## 📋 ÍNDICE DE CONTENIDOS

1. **Sistema de Asistentes Múltiples**
2. **Gestión de Conversaciones**
3. **Sistema RAG (Retrieval-Augmented Generation)**
4. **Sistema de Herramientas Dinámico y Extensible**
5. **Subida y Procesamiento de Archivos**
6. **Análisis de Imágenes con IA**
7. **Sistema de Reasoning y Orquestación**
8. **Visualización de Datos (Tablas y Gráficos)**
9. **Gestión de Referencias y Fuentes**
10. **Características Avanzadas de Interfaz**
11. **Personalización y Configuración**
12. **Exportación e Historial**

---

## 1. 🤖 SISTEMA DE ASISTENTES MÚLTIPLES

### Cambio de Asistente en Tiempo Real

SIMBA soporta múltiples asistentes especializados que puedes cambiar sin perder tu conversación:

- **Selector Visual**: Icono del asistente en la barra superior
- **Galería de Asistentes**: Click para ver todos los disponibles
- **Avatar y Nombre**: Cada asistente tiene identidad visual única
- **Indicador Activo**: Checkmark en el asistente actual

**Lo que ves:**
```
┌─────────────────────────────────┐
│ 🤖 Asistente Técnico        ✓   │
│ 📊 Analista de Datos            │
│ 📝 Documentador                 │
│ 🔍 Investigador                 │
└─────────────────────────────────┘
```

### Asistentes Completamente Configurables

Cada asistente es totalmente personalizable:

**Configuración del Asistente:**
```yaml
name: "Asistente Técnico"
avatar: "url/to/avatar.png"
greeting: "Hola, soy tu asistente técnico..."
placeholder: "Pregúntame sobre arquitectura, código..."
model: "magistral-2509"
temperature: 0.1
tools: ["confluence_search", "github_search"]
instructions: |
  Eres un experto técnico que ayuda con...
```

**Características personalizables:**
- **Imagen Principal**: Banner cuando está activo
- **Mensaje de Bienvenida**: Greeting específico
- **Placeholder**: Texto del textarea
- **Modelo IA**: Modelo específico para este asistente
- **Herramientas**: Tools disponibles solo para este asistente
- **System Prompt**: Instrucciones y personalidad
- **Acciones Rápidas**: Shortcuts predefinidos
- **Selector de Dispositivo**: ON/OFF según necesidad

### Switching Temporal con Chip Visual

Cuando cambias de asistente temporalmente:

**Chip Informativo:**
```
┌──────────────────────────────────────┐
│  [🤖 Avatar] Asistente Técnico       │
│  will respond                    [X] │
└──────────────────────────────────────┘
```

- **Click en [X]**: Vuelve al asistente original
- **Mantiene contexto**: No pierdes el historial
- **Transparencia**: Siempre sabes quién responderá

---

## 2. 💬 GESTIÓN DE CONVERSACIONES

### Creación Automática de Conversaciones

- **Primer mensaje real**: La conversación se crea automáticamente
- **Título Inteligente**: Generado por IA según el contenido
- **Guardado Continuo**: Cada mensaje se persiste instantáneamente
- **ID Único**: Cada conversación tiene identificador persistente

### Historial de Conversaciones

**Panel Lateral Izquierdo:**

```
📚 MIS CONVERSACIONES
┌─────────────────────────────────┐
│ 🕐 Hoy                          │
│   • Arquitectura microservicios │
│   • Análisis de logs producción│
├─────────────────────────────────┤
│ 📅 Ayer                         │
│   • Deployment pipeline AWS     │
│   • Documentación API REST      │
├─────────────────────────────────┤
│ 📆 Esta Semana                  │
│   • Review código backend       │
│   • Optimización BD             │
└─────────────────────────────────┘

[🔍 Buscar conversaciones...]
[📊 Estadísticas]
[🗑️ Limpiar Todo]
```

### Funciones del Historial

**Por Conversación:**
- 🔄 **Reanudar**: Continúa donde lo dejaste
- ✏️ **Renombrar**: Cambia el título manualmente
- 📤 **Exportar**: Descarga la conversación completa
- 🗑️ **Eliminar**: Borra la conversación

**Búsqueda Global:**
- Busca por palabras clave en TODAS tus conversaciones
- Encuentra respuestas antiguas instantáneamente
- Resultados ordenados por relevancia

**Estadísticas:**
- Total de conversaciones
- Mensajes enviados/recibidos
- Asistente más usado
- Herramientas más utilizadas
- Tokens consumidos

---

## 3. 🔍 SISTEMA RAG (Retrieval-Augmented Generation)

### ¿Qué es RAG en SIMBA?

RAG significa que SIMBA busca información en tus documentos corporativos ANTES de responder, asegurando respuestas basadas en datos reales de tu empresa.

### Búsqueda Semántica Automática

**Cuando preguntas algo, SIMBA:**

1. **Analiza tu pregunta** → Identifica conceptos clave
2. **Busca en múltiples fuentes** → Sistemas configurados
3. **Encuentra contenido relevante** → Usa embeddings de IA
4. **Te muestra qué encontró** → Referencias numeradas clickeables
5. **Genera respuesta contextualizada** → Basada en documentos reales

### Visualización de Búsqueda RAG

**En cada respuesta ves:**

```
SIMBA responde:
"Según la documentación encontrada, la arquitectura 
utiliza microservicios basados en Docker [1][2]..."

Referencias encontradas:
┌─────────────────────────────────────────┐
│ [1] Guía de Arquitectura - Confluence   │
│     "Los microservicios se despliegan   │
│      en contenedores Docker..."         │
│     📍 Sección: Deployment              │
│     🔗 Ver documento completo           │
├─────────────────────────────────────────┤
│ [2] Docker Compose Config - GitHub      │
│     "version: '3.8' services..."        │
│     📍 Archivo: docker-compose.yml      │
│     🔗 Ver en repositorio               │
└─────────────────────────────────────────┘
```

### Fuentes Agrupadas por Sistema

**Panel de Fuentes:**

```
📚 FUENTES CONSULTADAS

Sistema Wiki (5)
├─ Arquitectura de Sistemas
├─ Guía de Deployment  
├─ Manual de APIs
├─ Troubleshooting Guide
└─ Release Notes v2.3

Documentos Locales (3)
├─ arquitectura-2024.pdf
├─ diagrama-flujo.pptx
└─ especificaciones.docx

Repositorio Código (2)
├─ docker-compose.yml
└─ README.md
```

**Cada fuente muestra:**
- 📄 Título del documento
- 🏷️ Sistema de origen
- 📊 Score de relevancia (0-100%)
- 🔗 Enlace directo al original
- 📝 Extractos específicos citados

### Búsqueda Híbrida

SIMBA combina dos tipos de búsqueda:

**Búsqueda por Palabras Clave:**
- Para términos técnicos exactos
- Nombres de sistemas
- Códigos de error
- Referencias específicas

**Búsqueda Semántica:**
- Entiende el contexto
- Encuentra sinónimos
- Conceptos relacionados
- Documentos similares

---

## 4. 🛠️ SISTEMA DE HERRAMIENTAS DINÁMICO Y EXTENSIBLE

### Arquitectura de Herramientas Fully Configurable

SIMBA implementa un sistema de herramientas completamente dinámico y extensible, similar a Open-WebUI. **No hay herramientas fijas** - todo es configurable, extensible y adaptable a las necesidades de cada organización.

### Conceptos Fundamentales

#### **Tools como Plugins**
- Cada herramienta es un plugin independiente
- Se cargan dinámicamente desde configuración
- Pueden ser activadas/desactivadas sin reiniciar
- Soportan hot-reload para desarrollo

#### **Provider Architecture**
- Sistema basado en "Providers" extensibles
- Cada provider normaliza su API a formato común
- Nuevos providers se añaden sin modificar código core
- Configuración declarativa en YAML/JSON

#### **Tool Discovery Automático**
- SIMBA escanea servicios configurados al inicio
- Detecta automáticamente herramientas disponibles
- Genera definiciones de tools para el LLM
- Actualiza catálogo en tiempo real

### Configuración de Servicios (config.yml)

**Estructura del archivo de configuración:**

```yaml
# SIMBA Configuration - Fully Dynamic Tool System

services:
  # Ejemplo: Confluence
  confluence_wiki:
    enabled: true
    type: confluence
    url: https://confluence.empresa.com
    auth:
      type: basic
      username: ${CONFLUENCE_USER}
      password: ${CONFLUENCE_PASS}
    config:
      spaces: ["TECH", "DEVOPS", "DOCS"]
      max_results: 10
    tools:
      - name: search
        description: "Buscar en wiki corporativa"
        enabled: true
      - name: get_page
        description: "Obtener página específica"
        enabled: true
      - name: get_attachments
        description: "Listar attachments de una página"
        enabled: false
    icon: "fa-book"
    color: "#0052CC"

  # Ejemplo: Carpeta local con búsqueda semántica
  technical_docs:
    enabled: true
    type: folder
    path: /shared/technical-docs
    config:
      watch: true
      embeddings_model: "all-MiniLM-L6-v2"
      chunk_size: 1000
      supported_formats: 
        - pdf
        - docx
        - pptx
        - xlsx
        - md
    tools:
      - name: semantic_search
        description: "Búsqueda semántica en documentos"
        enabled: true
      - name: get_document
        description: "Obtener documento completo"
        enabled: true
    icon: "fa-folder"
    color: "#FF9800"

  # Ejemplo: API personalizada
  custom_erp:
    enabled: true
    type: custom
    url: https://erp.empresa.com/api
    auth:
      type: bearer
      token: ${ERP_API_TOKEN}
    tools:
      - name: query_clients
        description: "Consultar información de clientes"
        enabled: true
        parameters:
          type: object
          properties:
            client_id:
              type: string
              description: "ID del cliente"
            include_history:
              type: boolean
              default: false
          required: ["client_id"]
      - name: create_order
        description: "Crear orden en ERP"
        enabled: true
        parameters:
          type: object
          properties:
            client_id:
              type: string
            items:
              type: array
              items:
                type: object
          required: ["client_id", "items"]
    icon: "fa-database"
    color: "#4CAF50"

  # Ejemplo: Sistema de ticketing
  support_system:
    enabled: true
    type: jira
    url: https://jira.empresa.com
    auth:
      type: api_key
      api_key: ${JIRA_API_KEY}
      header_name: "X-API-Key"
    config:
      default_project: "SUPPORT"
      default_issue_type: "Task"
    tools:
      - name: search_tickets
        description: "Buscar tickets"
        enabled: true
      - name: create_ticket
        description: "Crear nuevo ticket"
        enabled: true
      - name: update_ticket
        description: "Actualizar ticket existente"
        enabled: true
      - name: add_comment
        description: "Añadir comentario a ticket"
        enabled: true
    icon: "fa-ticket"
    color: "#2196F3"

  # Ejemplo: Base de datos SQL
  analytics_db:
    enabled: false
    type: database
    driver: postgresql
    connection_string: ${DB_CONNECTION_STRING}
    config:
      read_only: true
      max_query_time: 30
      allowed_tables: 
        - sales
        - customers
        - products
    tools:
      - name: query_sql
        description: "Ejecutar query SQL de solo lectura"
        enabled: true
        parameters:
          type: object
          properties:
            query:
              type: string
              description: "SQL query"
          required: ["query"]
    icon: "fa-database"
    color: "#9C27B0"

# Provider Types configurables
provider_types:
  confluence:
    class: ConfluenceProvider
    module: providers.confluence
  
  folder:
    class: FolderProvider
    module: providers.folder
  
  custom:
    class: CustomAPIProvider
    module: providers.custom_api
  
  jira:
    class: JiraProvider
    module: providers.jira
  
  database:
    class: DatabaseProvider
    module: providers.database

# Configuración global de tools
tools_config:
  auto_discovery: true
  refresh_interval: 30  # segundos
  cache_ttl: 300
  max_concurrent_calls: 5
```

### Interfaz de Usuario: Gestión de Herramientas

#### **Vista Principal de Tools**

```
🔧 HERRAMIENTAS DISPONIBLES

Filtros: [Todas] [Activas] [Inactivas] [Por Servicio]
Buscar: [___________________] 🔍

┌─────────────────────────────────────────┐
│ 🌐 WIKI CORPORATIVA (3 tools)           │
│    https://confluence.empresa.com       │
│    [●ON ]  [⚙️ Configurar]  [ℹ️ Info]   │
├─────────────────────────────────────────┤
│  ☑️ confluence_search                   │
│     Buscar en espacios de Confluence    │
│                                          │
│  ☑️ confluence_get_page                 │
│     Obtener página específica           │
│                                          │
│  ☐ confluence_get_attachments           │
│     Listar attachments (desactivada)    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📁 DOCUMENTOS TÉCNICOS (2 tools)        │
│    /shared/technical-docs               │
│    [●ON ]  [⚙️ Configurar]  [ℹ️ Info]   │
├─────────────────────────────────────────┤
│  ☑️ folder_semantic_search              │
│     Búsqueda semántica IA               │
│                                          │
│  ☑️ folder_get_document                 │
│     Obtener documento completo          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 🎫 SISTEMA TICKETING (4 tools)          │
│    https://jira.empresa.com             │
│    [○OFF]  [⚙️ Configurar]  [ℹ️ Info]  │
├─────────────────────────────────────────┤
│  ☐ jira_search_tickets                  │
│  ☐ jira_create_ticket                   │
│  ☐ jira_update_ticket                   │
│  ☐ jira_add_comment                     │
└─────────────────────────────────────────┘

[+ Añadir Nuevo Servicio]
[📤 Exportar Configuración]
[📥 Importar Configuración]
```

#### **Panel de Configuración de Servicio**

**Click en ⚙️ Configurar:**

```
┌─────────────────────────────────────────┐
│ ⚙️ CONFIGURAR SERVICIO                  │
│    Wiki Corporativa                     │
├─────────────────────────────────────────┤
│                                          │
│ 📋 Información General                  │
│ ┌──────────────────────────────────┐   │
│ │ Nombre:                          │   │
│ │ [confluence_wiki_______________] │   │
│ │                                  │   │
│ │ Tipo:                            │   │
│ │ [Confluence ▼]                   │   │
│ │                                  │   │
│ │ URL Base:                        │   │
│ │ [https://confluence.empresa.com] │   │
│ │                                  │   │
│ │ Icono:                           │   │
│ │ [fa-book ▼]                      │   │
│ │                                  │   │
│ │ Color:                           │   │
│ │ [🎨 #0052CC]                     │   │
│ └──────────────────────────────────┘   │
│                                          │
│ 🔐 Autenticación                        │
│ ┌──────────────────────────────────┐   │
│ │ Tipo Auth:                       │   │
│ │ [Basic Auth ▼]                   │   │
│ │                                  │   │
│ │ Usuario:                         │   │
│ │ [admin_________________________] │   │
│ │                                  │   │
│ │ Contraseña:                      │   │
│ │ [••••••••••••••••••••••••••••••] │   │
│ │                                  │   │
│ │ ☑️ Usar variables de entorno     │   │
│ └──────────────────────────────────┘   │
│                                          │
│ ⚙️ Configuración Específica             │
│ ┌──────────────────────────────────┐   │
│ │ Espacios a buscar:               │   │
│ │ [TECH, DEVOPS, DOCS____________] │   │
│ │                                  │   │
│ │ Resultados máximos:              │   │
│ │ [10____]                         │   │
│ │                                  │   │
│ │ Timeout (segundos):              │   │
│ │ [30____]                         │   │
│ └──────────────────────────────────┘   │
│                                          │
│ 🔧 Herramientas                         │
│ ┌──────────────────────────────────┐   │
│ │ ☑️ confluence_search             │   │
│ │    [⚙️ Editar parámetros]        │   │
│ │                                  │   │
│ │ ☑️ confluence_get_page           │   │
│ │    [⚙️ Editar parámetros]        │   │
│ │                                  │   │
│ │ ☐ confluence_get_attachments     │   │
│ │    [⚙️ Editar parámetros]        │   │
│ └──────────────────────────────────┘   │
│                                          │
│ [🧪 Test Conexión]                      │
│ [💾 Guardar]  [❌ Cancelar]             │
└─────────────────────────────────────────┘
```

#### **Añadir Nuevo Servicio**

**Click en + Añadir Nuevo Servicio:**

```
┌─────────────────────────────────────────┐
│ ➕ AÑADIR NUEVO SERVICIO                │
├─────────────────────────────────────────┤
│                                          │
│ Selecciona el tipo de servicio:         │
│                                          │
│ 📚 Confluence                            │
│    Sistema wiki corporativa              │
│    [Seleccionar]                         │
│                                          │
│ 📁 Carpeta Local                         │
│    Búsqueda semántica en archivos       │
│    [Seleccionar]                         │
│                                          │
│ 🎫 Jira / Sistema Ticketing             │
│    Gestión de tickets y proyectos       │
│    [Seleccionar]                         │
│                                          │
│ 💾 Base de Datos SQL                    │
│    Consultas a BD corporativas          │
│    [Seleccionar]                         │
│                                          │
│ 🌐 REST API Personalizada               │
│    Cualquier API REST externa           │
│    [Seleccionar]                         │
│                                          │
│ 🔌 Custom Provider                       │
│    Código Python personalizado          │
│    [Seleccionar]                         │
│                                          │
│ [← Volver]                              │
└─────────────────────────────────────────┘
```

### Creación de Custom Provider

**Para desarrolladores: crear provider personalizado**

```python
# providers/my_custom_provider.py

from providers.base import BaseProvider
from typing import List, Dict, Any
from models import CoreItem, CoreDoc

class MyCustomProvider(BaseProvider):
    """
    Custom provider para sistema interno
    """
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_url = config.get('url')
        self.setup_auth(config.get('auth', {}))
    
    async def search(self, query: str, **kwargs) -> List[CoreItem]:
        """
        Implementar búsqueda en tu sistema
        """
        response = await self._api_call(
            'GET', 
            f'/search',
            params={'q': query, **kwargs}
        )
        
        # Normalizar a formato CoreItem
        return [
            self._to_core_item(item) 
            for item in response['results']
        ]
    
    async def get_content(self, item_id: str) -> CoreDoc:
        """
        Obtener contenido completo
        """
        response = await self._api_call(
            'GET',
            f'/documents/{item_id}'
        )
        
        return self._to_core_doc(response)
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Definir herramientas que este provider expone
        """
        return [
            {
                "name": "my_custom_search",
                "description": "Buscar en sistema personalizado",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Términos de búsqueda"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["docs", "code", "tickets"],
                            "description": "Categoría específica"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    
    def _to_core_item(self, raw_data: dict) -> CoreItem:
        """Normalizar respuesta nativa"""
        return CoreItem(
            id=raw_data['id'],
            title=raw_data['title'],
            content_preview=raw_data['snippet'],
            url=raw_data['url'],
            score=raw_data.get('score', 0.0),
            metadata=raw_data,  # Preservar todo
            provider=self.config.get('name', 'custom'),
            timestamp=self._parse_date(raw_data.get('updated'))
        )
```

**Registrar en config.yml:**

```yaml
services:
  my_internal_system:
    enabled: true
    type: my_custom
    url: https://internal.empresa.com/api
    auth:
      type: bearer
      token: ${MY_SYSTEM_TOKEN}
    icon: "fa-cogs"
    color: "#E91E63"

provider_types:
  my_custom:
    class: MyCustomProvider
    module: providers.my_custom_provider
```

### Activación Dinámica de Tools

**En el chat, botón de herramientas:**

```
[🔧] ← Click aquí

┌─────────────────────────────────────┐
│ 🔧 HERRAMIENTAS ACTIVAS             │
│                                      │
│ Activas: 5 / 12 disponibles          │
├─────────────────────────────────────┤
│ ☑️ confluence_search                │
│    🌐 Wiki Corporativa              │
│                                      │
│ ☑️ folder_semantic_search           │
│    📁 Documentos Técnicos           │
│                                      │
│ ☐ jira_create_ticket                │
│    🎫 Sistema Ticketing             │
│                                      │
│ ☑️ custom_erp_query                 │
│    🏢 ERP Corporativo               │
│                                      │
│ ☐ db_query_analytics                │
│    💾 Analytics DB                  │
├─────────────────────────────────────┤
│ [Ver Todas (12)] [Gestionar Tools]  │
└─────────────────────────────────────┘
```

**Comportamiento:**
- **Toggle individual**: Activa/desactiva cada tool
- **Persistente**: Configuración guardada por usuario
- **Por asistente**: Cada asistente puede tener tools específicas
- **Hot-reload**: Cambios sin reiniciar

### Ejecución Visible de Tools

**Cuando SIMBA usa una tool:**

```
🎯 Ejecutando plan (2/4 pasos)  [▼]

├─ ✅ Paso 1: Buscar en Wiki
│   🔧 Tool: confluence_search
│   📊 Encontrados: 5 documentos
│   ⏱️ 1.2s
│   🌐 Servicio: Wiki Corporativa
│
├─ 🔄 Paso 2: Consultar ERP
│   🔧 Tool: custom_erp_query
│   📄 Consultando cliente #12345
│   ⏱️ En progreso...
│   🏢 Servicio: ERP Corporativo
│
└─ ⏳ Pasos 3-4 pendientes
```

### Estado de Servicios en Tiempo Real

**Indicadores en navbar:**

```
[🟢 Wiki] [🟢 Docs] [🔴 Jira] [🟡 ERP]
```

**Estados:**
- 🟢 **Verde**: Servicio activo y respondiendo
- 🟡 **Amarillo**: Servicio lento (>2s respuesta)
- 🔴 **Rojo**: Servicio caído o inaccesible
- ⚪ **Gris**: Servicio deshabilitado

**Polling automático:**
- Verificación cada 30 segundos
- Health check configurable por servicio
- Notificaciones cuando cambia estado
- Logs de disponibilidad

### Importar/Exportar Configuración

**Exportar configuración actual:**

```yaml
# exported_config.yml
# Exportado: 2024-01-15 14:30:00

services:
  confluence_wiki:
    enabled: true
    type: confluence
    url: https://confluence.empresa.com
    # ... configuración completa
  
  technical_docs:
    enabled: true
    type: folder
    # ... configuración completa

# Puede ser compartido con equipo
# Importado en otras instancias
# Versionado en Git
```

**Importar configuración:**
```
📥 IMPORTAR CONFIGURACIÓN

Selecciona archivo: [Examinar...]

O pega YAML directamente:
┌─────────────────────────────────┐
│ services:                       │
│   my_service:                   │
│     enabled: true               │
│     ...                         │
└─────────────────────────────────┘

Opciones:
☑️ Sobrescribir servicios existentes
☐ Solo añadir nuevos servicios
☑️ Validar antes de aplicar

[Validar] [Importar] [Cancelar]
```

### Marketplace de Providers (Futuro)

**Concepto:**

```
🏪 MARKETPLACE DE PROVIDERS

Populares:
┌─────────────────────────────────┐
│ 📧 Gmail Provider               │
│    Buscar en correos            │
│    ⭐⭐⭐⭐⭐ (142)              │
│    [Instalar]                   │
├─────────────────────────────────┤
│ 🐙 GitHub Advanced              │
│    Issues, PRs, Code Search     │
│    ⭐⭐⭐⭐⭐ (89)               │
│    [Instalar]                   │
├─────────────────────────────────┤
│ 📊 Google Sheets                │
│    CRUD en hojas de cálculo     │
│    ⭐⭐⭐⭐ (67)                 │
│    [Instalar]                   │
└─────────────────────────────────┘

Categorías:
• Productividad
• Desarrollo
• Bases de Datos
• Cloud Services
• Comunicación

[Explorar Todos]
[Mis Providers Instalados]
[Crear Provider]
```

---

## 5. 📎 SUBIDA Y PROCESAMIENTO DE ARCHIVOS

### Zona de Dropzone

**Carga de Archivos:**

```
┌─────────────────────────────────────┐
│  📎 Arrastra archivos aquí          │
│     o click para seleccionar        │
│                                      │
│  Formatos soportados:                │
│  📄 PDF, Word, Excel, PowerPoint    │
│  🖼️ Imágenes (JPG, PNG, GIF)       │
│  📊 CSV, JSON, XML                   │
│  📝 TXT, Markdown, HTML              │
└─────────────────────────────────────┘
```

### Procesamiento Inteligente de Documentos

**Cuando subes un archivo:**

1. **Extracción Automática**
   - Texto completo del documento
   - Metadatos (autor, fecha, etc.)
   - Tablas y datos estructurados
   - Imágenes incrustadas

2. **Análisis de Contenido**
   - Resumen automático
   - Temas principales identificados
   - Entidades detectadas (nombres, fechas, lugares)

3. **Indexación para Búsqueda**
   - Añadido al contexto de la conversación
   - Búsqueda semántica disponible
   - Referencias clickeables

### Vista de Archivos Cargados

**Header de Archivos:**

```
📎 ARCHIVOS EN CONTEXTO (3)

┌──────────────────────────────────┐
│ 📄 especificaciones.pdf          │
│    📊 15 páginas · 2.3 MB        │
│    ✅ Procesado                   │
│    [👁️ Ver] [🗑️ Remover]        │
├──────────────────────────────────┤
│ 📊 datos-ventas.xlsx             │
│    📈 5 hojas · 890 KB           │
│    ✅ Procesado                   │
│    [👁️ Ver] [📊 Graficar]       │
├──────────────────────────────────┤
│ 🖼️ diagrama-arquitectura.png     │
│    🎨 1920×1080 · 456 KB         │
│    ✅ Analizado con IA           │
│    [👁️ Ver] [🔍 Re-analizar]    │
└──────────────────────────────────┘
```

### Ubicación del Contexto de Documentos

Puedes elegir DÓNDE se incluye el contenido extraído:

**Opción 1: En el mensaje SYSTEM**
```
🤖 SYSTEM MESSAGE:
   "Eres un asistente técnico..."
   
   === UPLOADED DOCUMENTS ===
   [Contenido de documentos aquí]
   ===========================
```

**Opción 2: En el mensaje USER**
```
👤 USER MESSAGE:
   === REFERENCE DOCUMENTS ===
   [Contenido de documentos aquí]
   === END OF DOCUMENTS ===
   
   === QUESTION ===
   ¿Cuál es la arquitectura descrita?
```

**Configuración:**
- Setting: "Document Context Location"
- Valores: `system` | `user`
- Default: `user`

### Procesamiento de Excel

Capacidades especiales para archivos Excel:

- **Todas las hojas** procesadas
- **Conversión a Markdown** para legibilidad
- **Detección de tablas** estructuradas
- **Generación automática de gráficos** (opcional)
- **Extracción de fórmulas** importantes

---

## 6. 🖼️ ANÁLISIS DE IMÁGENES CON IA

### Vision AI Automático

Cuando subes una imagen, SIMBA la analiza automáticamente:

**Análisis Inicial:**
```
🖼️ imagen-diagrama.png

🔍 Análisis automático:
"Esta imagen muestra un diagrama de arquitectura 
de microservicios. Contiene 5 componentes principales:
API Gateway, Service A, Service B, Base de Datos,
y Message Queue. Las flechas indican..."

[🔍 Re-analizar con contexto específico]
```

### Re-análisis Contextual

Puedes pedirle a SIMBA que analice la imagen de nuevo con un enfoque específico:

**Ejemplo de uso:**
1. Subes diagrama de arquitectura
2. SIMBA lo describe genéricamente
3. Click en "Re-analizar"
4. Escribes: "Identifica solo los componentes de seguridad"
5. SIMBA re-analiza con ese foco específico

### Formato `<simba_image>`

Las imágenes se representan internamente como:

```xml
<simba_image data-filename="diagrama.png">
Este es un diagrama UML que muestra las relaciones 
entre las clases del sistema. La clase principal 
es "UserManager" que hereda de "BaseManager"...
</simba_image>
```

**Ventajas:**
- Contenido textual searchable
- Preserva el nombre original
- Se incluye en el contexto
- Puede ser referenciado en respuestas

### Tipos de Análisis Visual

**Diagramas Técnicos:**
- Diagramas UML
- Arquitecturas de software
- Diagramas de flujo
- Organigramas

**Documentos Escaneados:**
- OCR automático
- Extracción de texto
- Reconocimiento de tablas
- Detección de estructura

**Capturas de Pantalla:**
- Interfaces de usuario
- Mensajes de error
- Configuraciones de sistema
- Logs visuales

**Gráficos y Charts:**
- Extracción de datos
- Interpretación de tendencias
- Identificación de anomalías

---

## 7. 🧠 SISTEMA DE REASONING Y ORQUESTACIÓN

### ¿Qué es Iterative Reasoning?

Reasoning es el proceso donde SIMBA "piensa en voz alta" antes de responder preguntas complejas.

### Activación/Desactivación

**Toggle de Reasoning:**

```
⚙️ Configuración

┌─────────────────────────────────┐
│ 🧠 Reasoning                     │
│    ☑️ Activado                  │
│                                  │
│    Permite a SIMBA razonar      │
│    paso a paso para consultas   │
│    complejas                     │
└─────────────────────────────────┘
```

- **ON**: SIMBA muestra su proceso de pensamiento
- **OFF**: Respuestas directas sin mostrar razonamiento

### Dos Fases de Ejecución

#### **FASE 1: Orchestrator LLM (Planificación)**

El orchestrator crea un plan de ejecución:

```
🎯 PLAN DE EJECUCIÓN

Objetivo: Encontrar información sobre deployment

Pasos planificados:
1. Buscar documentación de deployment en Wiki
2. Buscar scripts de deployment en carpeta técnica
3. Verificar configuración actual en sistema
4. Sintetizar información encontrada
5. Generar respuesta completa

Herramientas a usar:
• wiki_search
• folder_search_semantico
• system_query_config
```

#### **FASE 2: Main LLM (Respuesta)**

Una vez recopilada toda la información:

```
🤖 SIMBA responde:

Basándome en la documentación encontrada [1][2][3],
el proceso de deployment actual sigue estos pasos:

1. Build del código en Jenkins
2. Tests automáticos en staging
3. Aprobación manual requerida
4. Deploy a producción vía Ansible

[Ver 5 fuentes consultadas]
```

### Panel de Ejecución Minimalista

**Vista Compacta:**

```
🎯 Ejecutando plan (3/5 pasos)  [Badge: 3/5]

├─ ✅ Paso 1: Buscar docs Wiki
│   ⏱️ 1.2s · 📊 5 resultados
│
├─ ✅ Paso 2: Buscar scripts locales  
│   ⏱️ 0.8s · 📊 3 archivos
│
├─ 🔄 Paso 3: Verificar configuración
│   ⏱️ En progreso...
│
└─ ⏳ Pasos 4-5 pendientes
```

**Click para expandir detalles:**

```
🎯 Ejecutando plan (3/5 pasos)  [▼]

Step 1: Buscar docs Wiki  ✅
  Tool: wiki_search
  Parámetros:
    • query: "deployment pipeline"
    • spaces: ["TECH", "DEVOPS"]
  Resultado:
    • 5 páginas encontradas
    • Más relevante: "CI/CD Pipeline v2.0"
  [🔗 Ver resultados completos]
  
Step 2: Buscar scripts locales  ✅
  Tool: folder_search_semantico
  Parámetros:
    • query: "ansible deployment scripts"
    • path: "/shared/devops"
  Resultado:
    • 3 scripts encontrados
    • deploy-prod.yml (100% match)
  [🔗 Ver archivos]

Step 3: Verificar configuración  🔄
  Tool: system_query_config
  Parámetros:
    • component: "jenkins"
    • environment: "production"
  Estado: Ejecutando...
```

### Resolución de Dependencias

SIMBA maneja dependencias entre steps automáticamente:

**Ejemplo:**
```
Step 1: "¿Quién es el CEO de Tesla?" 
  → Resultado: "Elon Musk"

Step 2: "¿Cuántos años tiene {{step_1.result}}?"
  → Resuelve a: "¿Cuántos años tiene Elon Musk?"
  → Ejecuta búsqueda con ese contexto
```

**Placeholders soportados:**
- `{{step_N.result}}` - Resultado completo
- `{{step_N.result.field}}` - Campo específico
- `{{step_N.result.items[0]}}` - Arrays
- `{{step_N.result.data.user.name}}` - Paths anidados

### Indicadores Visuales de Estado

**Estados de Steps:**
- ⏳ **Pending** (gris): Esperando ejecución
- 🔄 **Executing** (azul pulsante): En progreso
- ✅ **Completed** (verde): Finalizado exitosamente
- ❌ **Failed** (rojo): Error en ejecución
- ⏭️ **Skipped** (gris oscuro): Saltado por dependencia

### Abortar Ejecución

Si un proceso toma mucho tiempo:

```
⚠️ ¿Deseas abortar el proceso?

[Sí, detener] [No, continuar]

Nota: Los pasos completados hasta ahora
se conservarán para tu referencia.
```

---

## 8. 📊 VISUALIZACIÓN DE DATOS

### Tablas Interactivas

Cuando SIMBA genera tablas de datos:

```
📊 COMPARATIVA DE SERVICIOS

┌──────────────┬─────────┬──────────┬─────────┐
│ Servicio     │ Uptime  │ Latencia │ Errores │
├──────────────┼─────────┼──────────┼─────────┤
│ API Gateway  │ 99.9%   │ 45ms     │ 12      │
│ Auth Service │ 99.7%   │ 120ms    │ 45      │
│ DB Primary   │ 100%    │ 8ms      │ 0       │
│ Cache Redis  │ 99.8%   │ 2ms      │ 3       │
└──────────────┴─────────┴──────────┴─────────┘

[🔍 Filtrar] [↕️ Ordenar] [📈 Crear Gráfico]
```

**Funciones de Tabla:**

**1. Ordenación por Columna**
- Click en encabezado para ordenar
- Click nuevamente para orden inverso
- Indicador visual de columna activa

**2. Filtros Dinámicos**
- Input de búsqueda por columna
- Filtro global en toda la tabla
- Actualización en tiempo real

**3. Exportación**
- CSV
- Excel
- JSON
- Copiar a clipboard

### Generación de Gráficos

**Selector de Tipo de Gráfico:**

```
📈 CREAR GRÁFICO

┌─────────────────────────────────────┐
│ 🎯 Auto (Recomendado)               │
│    El sistema elige el mejor tipo   │
├─────────────────────────────────────┤
│ 📊 Gráfico de Barras                │
│    Comparar categorías visualmente  │
├─────────────────────────────────────┤
│ 📈 Gráfico de Líneas                │
│    Tendencias a lo largo del tiempo │
├─────────────────────────────────────┤
│ 🥧 Gráfico Circular                 │
│    Partes de un total (pie chart)   │
├─────────────────────────────────────┤
│ 🍩 Gráfico Dona                     │
│    Como circular con espacio central│
└─────────────────────────────────────┘

[Cancelar]
```

**Gráfico Generado:**

```
📊 Comparativa de Uptime por Servicio

[Gráfico interactivo de barras aquí]

Controles:
[💾 Descargar PNG]
[📊 Cambiar Tipo]
[🔄 Actualizar Datos]
[📋 Ver Tabla Original]
```

**Características de Gráficos:**
- **Interactivos**: Hover para ver valores
- **Responsive**: Se adaptan al tamaño
- **Colores automáticos**: Paleta inteligente
- **Leyendas**: Siempre visibles y claras
- **Animaciones**: Suaves y profesionales

### Detección Inteligente de Datos

SIMBA detecta automáticamente:

- **Datos temporales**: Gráfico de líneas
- **Comparaciones**: Gráfico de barras
- **Proporciones**: Gráfico circular
- **Múltiples series**: Barras agrupadas
- **Tendencias**: Líneas con proyección

---

## 9. 🔗 GESTIÓN DE REFERENCIAS Y FUENTES

### Referencias Numeradas Clickeables

Cada afirmación en la respuesta tiene referencias:

```
SIMBA: "El sistema usa arquitectura de microservicios [1][2]
con comunicación vía API Gateway [3]. El deployment se 
realiza mediante Kubernetes [1][4] con pipelines CI/CD [5]."

Referencias:
[1] [2] [3] [4] [5]
```

**Click en cualquier referencia:**

```
┌─────────────────────────────────────────────┐
│ [1] Arquitectura de Microservicios          │
│                                              │
│ "El sistema está compuesto por múltiples    │
│ servicios independientes que se comunican   │
│ mediante APIs REST. Cada servicio puede     │
│ ser desplegado independientemente..."       │
│                                              │
│ 📍 Wiki > TECH > Arquitectura               │
│ 👤 Autor: Juan Pérez                        │
│ 📅 Última actualización: 15/10/2024         │
│ 🔗 Ver documento completo                   │
└─────────────────────────────────────────────┘
```

### Agrupación Inteligente de Referencias

Referencias consecutivas se agrupan automáticamente:

```
Antes: "...el sistema [1][2][3][4][5] utiliza..."

Después: "...el sistema [1-5] utiliza..."
```

**Click en grupo expandido:**
```
[1-5] Referencias agrupadas (5)
  ├─ [1] Arquitectura general
  ├─ [2] Componentes core
  ├─ [3] Comunicación servicios
  ├─ [4] Deployment K8s
  └─ [5] Monitoring setup
```

### Panel de Fuentes Completo

**Panel de fuentes expandible:**

```
📚 FUENTES CONSULTADAS (Total: 13)

🌐 Sistema Wiki (5 documentos)
┌─────────────────────────────────────┐
│ Arquitectura de Microservicios      │
│ Score: 95% · 📄 20 páginas          │
│ Sección citada: "Deployment"        │
│ [👁️ Ver] [📎 Citar]                 │
├─────────────────────────────────────┤
│ Guía de APIs REST                   │
│ Score: 87% · 📄 12 páginas          │
│ [👁️ Ver] [📎 Citar]                 │
└─────────────────────────────────────┘

📁 Documentos Locales (3 archivos)
┌─────────────────────────────────────┐
│ arquitectura-2024.pdf                │
│ Score: 92% · 📊 15 páginas          │
│ Extracto: Página 5, sección 2.3     │
│ [👁️ Ver] [📎 Citar]                 │
└─────────────────────────────────────┘

🔧 Sistema ERP (2 resultados)
┌─────────────────────────────────────┐
│ Configuración Producción             │
│ Score: 78% · 🗓️ Actualizado hoy     │
│ [👁️ Ver] [📎 Citar]                 │
└─────────────────────────────────────┘

💾 Base de Datos (3 registros)
┌─────────────────────────────────────┐
│ deployment_history tabla             │
│ Score: 85% · 🔍 Query ejecutada     │
│ [👁️ Ver] [📎 Citar]                 │
└─────────────────────────────────────┘
```

### Acciones por Fuente

**Para cada fuente puedes:**

- 👁️ **Ver**: Abre el documento original
- 📎 **Citar**: Copia referencia formateada
- 📊 **Estadísticas**: Score, caracteres usados, tokens
- 🔗 **Compartir**: URL directa al documento
- 💾 **Guardar**: Añade a favoritos personales

### Estrategias de Visualización

SIMBA adapta cómo muestra los documentos según el tipo:

**Páginas Wiki:**
- Abre en nueva pestaña por defecto
- Navega directo a la sección citada
- Mantiene tu sesión corporativa

**PDFs:**
- Vista en iframe incrustado
- O descarga según preferencia
- Salta a página específica citada

**Archivos Word/Excel:**
- Descarga automática
- O conversión a vista previa web
- Según configuración del usuario

**Código en Repositorios:**
- Link directo a línea específica
- Vista de diff si es relevante
- Blame para ver autor

---

## 10. 🎨 CARACTERÍSTICAS AVANZADAS DE INTERFAZ

### Menciones de Asistentes (@mention)

Escribe `@` en el textarea para invocar asistentes:

```
┌─────────────────────────────────┐
│ 📝 Escribe tu mensaje...        │
│                                  │
│ @                               │
│ ┌─────────────────────────────┐ │
│ │ Asistentes Disponibles      │ │
│ ├─────────────────────────────┤ │
│ │ @tecnico                    │ │
│ │ @analista                   │ │
│ │ @documentador               │ │
│ │ @investigador               │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

**Uso:**
```
@tecnico analiza este error de producción
@documentador crea documentación de esta API
```

### Instrucciones Predefinidas

Cada asistente tiene atajos visuales:

**Botón de Instrucciones:**

```
⚡ ACCIONES RÁPIDAS

┌─────────────────────────────────────┐
│ 🔍 Analizar Logs                    │
│    Busca patrones y errores en logs│
├─────────────────────────────────────┤
│ 📝 Crear Documentación              │
│    Genera docs técnicas de código   │
├─────────────────────────────────────┤
│ 🐛 Debug Error                      │
│    Ayuda a resolver errores         │
├─────────────────────────────────────┤
│ 🎨 Generar Diagrama                 │
│    Crea diagrama de arquitectura    │
└─────────────────────────────────────┘
```

**Dos tipos de instrucciones:**

1. **Sin Selección** (isSelection: 0)
   - Aparecen en el menú de acciones rápidas
   - Click para ejecutar directamente

2. **Con Selección** (isSelection: 1)
   - Aparecen al seleccionar texto
   - Aplican sobre el texto seleccionado

### Popover de Selección de Texto

Selecciona cualquier texto en respuestas:

```
┌─────────────────────────────────┐
│ 🤔 Pregunta a SIMBA             │
│    [Input: "¿Qué significa...?"]│
├─────────────────────────────────┤
│ ✏️ Highlight para reportar      │
│    Resalta para incluir en notas│
├─────────────────────────────────┤
│ 📋 Copiar al portapapeles       │
│    Copia texto seleccionado     │
├─────────────────────────────────┤
│ 🔍 Explicar con más detalle     │
│    Profundiza en este tema      │
└─────────────────────────────────┘
```

### Sistema de Highlighting

**Resalta información importante:**

```
SIMBA: "El deployment requiere tres pasos:
1. Build en Jenkins ← [RESALTADO AMARILLO]
2. Tests automáticos
3. Deploy a producción ← [RESALTADO AMARILLO]"
```

**Gestión de Highlights:**

```
⭐ MIS HIGHLIGHTS (7)

┌─────────────────────────────────────┐
│ 🟡 "Build en Jenkins"               │
│    Conversación: Deploy Pipeline    │
│    Fecha: Hoy a las 10:30           │
│    [📋 Copiar] [🗑️ Eliminar]        │
├─────────────────────────────────────┤
│ 🟡 "Deploy a producción"            │
│    Conversación: Deploy Pipeline    │
│    [📋 Copiar] [🗑️ Eliminar]        │
└─────────────────────────────────────┘

[📤 Exportar Todo] [🗑️ Limpiar Todo]
```

**Exportación de Highlights:**

```json
{
  "highlights": [
    {
      "text": "Build en Jenkins",
      "conversation": "Deploy Pipeline",
      "timestamp": "2024-01-15T10:30:00Z",
      "context": "El deployment requiere..."
    }
  ],
  "export_date": "2024-01-15T14:22:00Z"
}
```

### Auto-scroll Inteligente

**Comportamiento:**
- ✅ Auto-scroll mientras SIMBA escribe
- ⏸️ Se detiene si haces scroll manual
- 🔄 Se reactiva al llegar al final
- 📍 Botón "Ir al final" siempre visible

```
[Contenido del chat]
...
...
...
         [⬇️ Ir al final (3 mensajes nuevos)]
```

### Barra de Progreso de Streaming

Cuando SIMBA está escribiendo:

```
┌────────────────────────────────────┐
│ 🔄 SIMBA está escribiendo...       │
│ ████████████░░░░░░░░░░ 60%        │
│ 1,234 / 2,000 tokens               │
└────────────────────────────────────┘
```

### Selección de Dispositivo

Si el asistente requiere contexto de dispositivo:

```
🎯 SELECCIONA UN DISPOSITIVO

┌─────────────────────────────────┐
│ [ ] Dispositivo A               │
│ [ ] Dispositivo B               │
│ [✓] Dispositivo C               │
│ [ ] Dispositivo D               │
│ [ ] GENERAL                     │
└─────────────────────────────────┘

[💾 Seleccionar]

Nota: Las respuestas se adaptarán 
específicamente a este dispositivo.
```

**Chip de Dispositivo Activo:**
```
┌──────────────────────┐
│ 🎯 Dispositivo C [X] │
└──────────────────────┘
```

---

## 11. ⚙️ PERSONALIZACIÓN Y CONFIGURACIÓN

### Popup de Configuración Principal

**Acceso:** Click en ⚙️ en la barra superior

```
⚙️ CONFIGURACIÓN

┌─────────────────────────────────────┐
│ 🔌 API Configuration                │
│    URLs y credenciales              │
│    [▼ Expandir]                     │
├─────────────────────────────────────┤
│ 🤖 Model Configuration              │
│    Modelos de IA a usar             │
│    [▼ Expandir]                     │
├─────────────────────────────────────┤
│ 🎤 Voice Configuration              │
│    Control de voz                   │
│    [▼ Expandir]                     │
├─────────────────────────────────────┤
│ 📄 Document Configuration           │
│    Gestión de documentos            │
│    [▼ Expandir]                     │
├─────────────────────────────────────┤
│ 🧠 Reasoning Configuration          │
│    Sistema de razonamiento          │
│    [▼ Expandir]                     │
├─────────────────────────────────────┤
│ 🔧 Tools & Services                 │
│    Gestión de herramientas          │
│    [▼ Expandir]                     │
└─────────────────────────────────────┘

[💾 Guardar Cambios] [↩️ Restaurar]
```

### Configuración de Modelos

```
🤖 CONFIGURACIÓN DE MODELOS

┌─────────────────────────────────────┐
│ 💬 Modelo Principal                 │
│    [Dropdown: magistral-2509]       │
│    Para respuestas generales        │
├─────────────────────────────────────┤
│ 📝 Modelo de Resumen                │
│    [Dropdown: mistral-small-24B]    │
│    Para sintetizar documentos       │
├─────────────────────────────────────┤
│ 👁️ Modelo de Visión                │
│    [Dropdown: mistral-vision]       │
│    Para análisis de imágenes        │
├─────────────────────────────────────┤
│ 🎯 Modelo Orchestrator              │
│    [Dropdown: gpt-4o-mini]          │
│    Para planning y reasoning        │
└─────────────────────────────────────┘

⚙️ Parámetros Avanzados
┌─────────────────────────────────────┐
│ 🌡️ Temperature: [Slider: 0.0]      │
│    Creatividad vs. Precisión        │
│                                      │
│ 📊 Max Tokens: [Input: 25000]      │
│    Longitud máxima de respuesta     │
│                                      │
│ ⚡ Tool Temperature: [Slider: 0.1]  │
│    Para ejecución de herramientas   │
└─────────────────────────────────────┘
```

**Detección Dinámica de Modelos:**
- Lista cargada desde el servidor
- Filtrado por categoría (chat, reasoning, vision)
- Fallback a input manual si falla carga
- Indicadores de categoría del modelo activo

### Configuración de Documentos

```
📄 CONFIGURACIÓN DE DOCUMENTOS

┌─────────────────────────────────────┐
│ 📍 Ubicación del Contexto           │
│    ⚪ Sistema (recomendado)         │
│    ⚫ Mensaje de Usuario             │
│                                      │
│    Dónde incluir docs subidos       │
├─────────────────────────────────────┤
│ 🚫 Excluir de Historial             │
│    ☐ No guardar docs en conversación│
│                                      │
│    Útil para docs temporales        │
├─────────────────────────────────────┤
│ 🔧 Dropzone Activa                  │
│    ☑️ Habilitar subida de archivos  │
│                                      │
│    Permite arrastar y soltar docs   │
└─────────────────────────────────────┘
```

### Configuración de Voz

```
🎤 CONFIGURACIÓN DE VOZ

┌─────────────────────────────────────┐
│ ☑️ Activar Control de Voz           │
│                                      │
│ 🌍 Idioma                           │
│    [Dropdown: Español (ES)]         │
│    • Español (ES)                   │
│    • English (US)                   │
│    • Français (FR)                  │
│    • Deutsch (DE)                   │
├─────────────────────────────────────┤
│ ⏱️ Tiempo Máximo de Grabación       │
│    [Slider: 30 segundos]            │
│                                      │
│ 📤 Envío Automático                 │
│    ☐ Enviar al terminar de grabar  │
│                                      │
│ 🔄 Grabación Continua               │
│    ☐ Continuar grabando             │
└─────────────────────────────────────┘

🎛️ Configuración Avanzada de Audio
┌─────────────────────────────────────┐
│ ☑️ Cancelación de Eco               │
│ ☑️ Supresión de Ruido               │
│ ☑️ Control Automático de Ganancia   │
└─────────────────────────────────────┘
```

### Configuración de Reasoning

```
🧠 CONFIGURACIÓN DE REASONING

┌─────────────────────────────────────┐
│ ☑️ Activar Reasoning Iterativo      │
│                                      │
│    Permite razonamiento paso a paso │
│    para consultas complejas          │
├─────────────────────────────────────┤
│ 🔢 Máximo de Iteraciones            │
│    [Input: 5]                        │
│                                      │
│    Número máximo de pasos           │
├─────────────────────────────────────┤
│ 📊 Mostrar Panel de Ejecución       │
│    ⚫ Siempre visible                │
│    ⚪ Solo cuando hay pasos          │
│    ⚪ Oculto (solo badge)            │
└─────────────────────────────────────┘
```

---

## 12. 📤 EXPORTACIÓN E HISTORIAL

### Exportar Conversación Completa

```
📤 EXPORTAR CONVERSACIÓN

Formato: [Dropdown: JSON]
• JSON (completo con metadata)
• Markdown (legible, sin metadata)
• PDF (formato imprimible)
• TXT (solo texto plano)

Incluir:
☑️ Mensajes de usuario y asistente
☑️ Referencias y fuentes consultadas
☑️ Imágenes analizadas
☑️ Archivos adjuntos (links)
☑️ Metadata (timestamps, tokens, etc.)
☐ Highlights personales

[📥 Descargar]
```

### Formato JSON de Exportación

```json
{
  "conversation_id": "conv_abc123",
  "title": "Arquitectura de Microservicios",
  "assistant": {
    "name": "Asistente Técnico",
    "guid": "asst_xyz789"
  },
  "device": "Dispositivo A",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z",
  "messages": [
    {
      "id": "msg_001",
      "role": "user",
      "content": "¿Cuál es nuestra arquitectura actual?",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "id": "msg_002",
      "role": "assistant",
      "content": "La arquitectura actual...",
      "timestamp": "2024-01-15T10:00:15Z",
      "sources": [
        {
          "title": "Arquitectura de Microservicios",
          "url": "https://wiki.../page/123",
          "score": 0.95,
          "references": [...]
        }
      ],
      "tokens_used": 1234
    }
  ],
  "total_messages": 12,
  "total_tokens": 45678,
  "sources_used": [...]
}
```

### Búsqueda en Historial

```
🔍 BUSCAR EN CONVERSACIONES

┌─────────────────────────────────────┐
│ [Input: "kubernetes deployment"]    │
│ 🔎                                   │
└─────────────────────────────────────┘

📊 Resultados (8 conversaciones)

┌─────────────────────────────────────┐
│ 💬 Deploy con Kubernetes            │
│    Hace 2 días · 15 mensajes        │
│    "...pipeline de CI/CD..."        │
│    [🔗 Abrir]                       │
├─────────────────────────────────────┤
│ 💬 Troubleshooting K8s              │
│    La semana pasada · 8 mensajes    │
│    "...pods en estado pending..."   │
│    [🔗 Abrir]                       │
└─────────────────────────────────────┘

Filtros:
☐ Solo con el Asistente Técnico
☐ Con dispositivo específico
☐ Últimos 7 días
```

### Estadísticas de Uso

```
📊 ESTADÍSTICAS DE USO

Este Mes
┌─────────────────────────────────────┐
│ 💬 Conversaciones: 47               │
│ 📨 Mensajes: 583                    │
│ 🔧 Tools Usados: 156 veces          │
│ 📄 Documentos: 89 procesados        │
│ 🖼️ Imágenes: 23 analizadas         │
│ 🪙 Tokens: 2.3M consumidos          │
└─────────────────────────────────────┘

🤖 Asistentes Más Usados
1. Técnico (45%)
2. Analista (30%)
3. Documentador (15%)
4. Otros (10%)

🔧 Herramientas Más Usadas
1. wiki_search (67 veces)
2. folder_search (45 veces)
3. db_query (28 veces)
4. ticket_create (16 veces)

📊 Gráfico de Actividad
[Gráfico de barras por día]
```

---

## 🎯 CASOS DE USO COMPLETOS

### Caso 1: Investigación Técnica Compleja

**Usuario:** "Necesito entender nuestro proceso de deployment completo"

**SIMBA hace:**

1. **Planning** (5 segundos)
   - Identifica 5 fuentes clave a consultar
   - Planifica 7 pasos de búsqueda

2. **Ejecución** (15 segundos)
   ```
   ✅ Buscar "CI/CD pipeline" en Wiki
   ✅ Buscar scripts deployment en carpetas
   ✅ Consultar configuración Jenkins actual
   ✅ Buscar logs de últimos deployments
   ✅ Verificar políticas de aprobación
   ```

3. **Respuesta Final**
   - Diagrama visual del proceso
   - 12 fuentes consultadas
   - Referencias a cada paso
   - Código de ejemplo incluido
   - Sugerencias de mejora

**Tiempo total:** ~20 segundos  
**Fuentes consultadas:** 12 documentos  
**Calidad:** 100% basado en docs reales

### Caso 2: Análisis de Documento Técnico

**Usuario:** [Sube PDF de 50 páginas] "Resume los puntos clave"

**SIMBA hace:**

1. **Procesamiento** (3 segundos)
   - Extrae 15,000 palabras
   - Detecta 8 secciones principales
   - Identifica 12 diagramas

2. **Análisis** (5 segundos)
   ```
   ✅ Analizar estructura del documento
   ✅ Identificar temas principales
   ✅ Extraer puntos clave por sección
   ✅ Procesar diagramas con Vision AI
   ```

3. **Resultado**
   ```
   📄 RESUMEN EJECUTIVO
   
   Puntos Clave:
   • Tema 1 [Ver sección 2.1]
   • Tema 2 [Ver sección 3.4]
   • Tema 3 [Ver sección 5.2]
   
   Diagramas Importantes:
   🖼️ Arquitectura General (pág. 12)
   🖼️ Flujo de Datos (pág. 23)
   
   [📥 Descargar resumen completo]
   ```

### Caso 3: Troubleshooting con Contexto

**Usuario:** "Tengo este error en producción: [pega log de error]"

**SIMBA hace:**

1. **Análisis del Error** (2 segundos)
   - Identifica tipo de error
   - Extrae stack trace
   - Detecta componente afectado

2. **Búsqueda de Casos Similares** (8 segundos)
   ```
   ✅ Buscar error en base de conocimiento
   ✅ Buscar en tickets históricos
   ✅ Consultar runbooks de troubleshooting
   ✅ Verificar configuración actual del sistema
   ```

3. **Respuesta con Solución**
   ```
   🐛 ERROR IDENTIFICADO
   
   Tipo: NullPointerException en AuthService
   Componente: /api/v1/auth/validate
   
   📚 CASOS SIMILARES ENCONTRADOS (3)
   
   ✅ SOLUCIÓN MÁS PROBABLE:
   Este error ocurre cuando el token JWT está 
   malformado [1]. La solución aplicada 
   exitosamente 3 veces fue:
   
   1. Verificar formato del token
   2. Actualizar librería jwt a v3.2
   3. Reiniciar servicio de auth
   
   [Ver procedimiento completo][1]
   [Ver ticket #1234 resuelto][2]
   [Crear ticket de soporte]
   ```

---

## 🎓 TIPS Y MEJORES PRÁCTICAS

### Para Mejores Búsquedas RAG

✅ **SÍ hacer:**
- Sé específico: "Busca en el espacio TECH de la Wiki"
- Usa términos técnicos correctos
- Menciona el contexto: "Para el proyecto X"
- Pide documentos recientes: "Documentación actualizada"

❌ **NO hacer:**
- Preguntas muy genéricas
- Esperar conocimiento de SIMBA fuera de tus docs
- Asumir que SIMBA sabe sobre proyectos sin documentar

### Para Usar Herramientas Efectivamente

✅ **SÍ hacer:**
- Activa solo las tools que necesites
- Revisa los steps de ejecución
- Espera a que complete todos los pasos
- Usa el contexto de respuestas previas

❌ **NO hacer:**
- Activar todas las tools siempre
- Interrumpir procesos complejos
- Repetir la misma pregunta sin esperar

### Para Configurar Nuevos Servicios

✅ **SÍ hacer:**
- Usa nombres descriptivos para servicios
- Configura health checks adecuados
- Documenta qué hace cada tool
- Prueba la conexión antes de activar
- Usa variables de entorno para credenciales

❌ **NO hacer:**
- Hardcodear contraseñas en config
- Crear tools ambiguas o duplicadas
- Omitir timeouts en configuración

### Para Subir Documentos

✅ **SÍ hacer:**
- Documenta claramente lo que subes
- Usa nombres de archivo descriptivos
- Sube documentos en formatos estándar
- Organiza por temas si son múltiples

❌ **NO hacer:**
- Subir archivos sin contexto
- Archivos con nombres genéricos: "documento1.pdf"
- Mezclar temas no relacionados

---

**SIMBA transforma cómo trabajas con información corporativa: de horas buscando manualmente a segundos de respuestas precisas y contextualizadas. Todo el conocimiento de tu empresa, unificado en una conversación inteligente. Completamente configurable y extensible según las necesidades de tu organización.**
