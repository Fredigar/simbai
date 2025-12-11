# SIMBA Specification Builder

**Framework modular para crear y mantener documentos `specifications.md` de manera estructurada, consistente y mantenible.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Framework7](https://img.shields.io/badge/Framework7-8.0-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Tabla de Contenidos

1. [Características](#-características)
2. [Instalación](#-instalación)
3. [Inicio Rápido](#-inicio-rápido)
4. [Guía de Uso](#-guía-de-uso)
5. [Arquitectura](#-arquitectura)
6. [Desarrollo](#-desarrollo)
7. [API Reference](#-api-reference)
8. [Ejemplos](#-ejemplos)
9. [FAQ](#-faq)

---

## 🎯 Características

### Core Features

- ✅ **Modular**: Secciones independientes y reutilizables
- ✅ **Extensible**: Fácil agregar nuevos templates y validadores
- ✅ **Visual**: Editor WYSIWYG con vista previa en tiempo real
- ✅ **Validación**: Reglas automáticas de consistencia y completitud
- ✅ **Multi-formato**: Exportación a Markdown, JSON y HTML
- ✅ **Offline-first**: Funciona sin conexión, guarda en localStorage
- ✅ **Framework7**: UI components consistentes y responsive

### Templates Incluidos

| Template | Descripción | Ícono |
|----------|-------------|-------|
| **System Overview** | Visión general del sistema | 🤖 |
| **Features** | Gestión de funcionalidades | 💬 |
| **RAG System** | Sistema de búsqueda RAG | 🔍 |
| **Tools Dynamic** | Herramientas extensibles | 🛠️ |
| **File Upload** | Subida de archivos | 📎 |
| **Image Analysis** | Análisis con Vision AI | 🖼️ |
| **Reasoning** | Sistema de razonamiento | 🧠 |
| **Data Visualization** | Tablas y gráficos | 📊 |
| **References** | Gestión de referencias | 🔗 |
| **UI Features** | Características de interfaz | 🎨 |
| **Configuration** | Configuración del sistema | ⚙️ |
| **Export/History** | Exportación e historial | 📤 |

---

## 📦 Instalación

### Opción 1: Uso Directo (sin instalación)

Simplemente abre `spec-builder.html` en tu navegador:

```bash
cd simbai
open spec-builder.html
# o
firefox spec-builder.html
# o
chrome spec-builder.html
```

**Nota**: Todos los recursos se cargan desde CDN, no necesitas instalar nada.

### Opción 2: Servidor Local

Si prefieres usar un servidor local (recomendado para desarrollo):

```bash
# Python 3
python3 -m http.server 8000

# Node.js
npx http-server -p 8000

# PHP
php -S localhost:8000
```

Luego abre: `http://localhost:8000/spec-builder.html`

---

## 🚀 Inicio Rápido

### 1. Crear Nueva Especificación

1. Abre `spec-builder.html` en tu navegador
2. Click en el menú (⋮) → **Nueva Especificación**
3. Click en **Editar Metadata** para configurar:
   - Título de la especificación
   - Versión (formato semver: 1.0.0)
   - Autor/equipo

### 2. Agregar Secciones

1. Click en el botón **+** (Agregar Sección)
2. Selecciona un template de la galería
3. Completa los campos del formulario
4. Click en **Guardar**

### 3. Organizar Secciones

- **Reordenar**: Arrastra las secciones usando el ícono de drag (☰)
- **Editar**: Click en el ícono de edición (✏️)
- **Eliminar**: Click en el ícono de eliminar (🗑️)

### 4. Validar y Exportar

1. Click en el ícono de validación (✓) para verificar errores
2. Click en el ícono de descarga (↓) para exportar
3. Selecciona formato:
   - **Markdown** → `specifications.md`
   - **JSON** → `specification.json`
   - **HTML** → `specification.html`

---

## 📖 Guía de Uso

### Gestión de Metadata

La metadata es información sobre la especificación:

```json
{
  "title": "SIMBA - Sistema de Chat",
  "version": "1.0.0",
  "author": "Equipo SIMBA",
  "created": "2024-12-11T00:00:00Z",
  "updated": "2024-12-11T12:00:00Z"
}
```

**Editar metadata:**
1. Click en el menú (⋮) → **Editar Metadata**
2. Completa los campos
3. Los cambios se guardan automáticamente

### Trabajar con Secciones

#### Agregar Sección

```
1. Click en [+] en la tarjeta de Secciones
2. Selecciona template (ej: "Sistema RAG")
3. Se abre el editor de sección
4. Completa campos requeridos
5. Click en "Guardar"
```

#### Editar Sección

```
1. Click en [✏️] en la sección a editar
2. Modifica los campos necesarios
3. Click en "Guardar"
```

#### Campos por Template

Cada template tiene campos específicos. Ejemplo para **RAG System**:

- **Título**: Nombre de la sección
- **Descripción**: ¿Qué es RAG en tu sistema?
- **Pasos de Búsqueda**: Lista de pasos (uno por línea)
- **Fuentes**: Lista de fuentes de datos

### Vista Previa

Ver cómo se verá el markdown final:

1. Click en menú (⋮) → **Vista Previa**
2. Se muestra el markdown generado
3. Click en **Volver al Editor** cuando termines

### Validación

El sistema valida automáticamente:

- ✅ Títulos no vacíos
- ✅ Versión en formato semver (1.0.0)
- ✅ Al menos una sección
- ✅ IDs de sección únicos
- ✅ Contenido completo
- ✅ Orden secuencial

**Tipos de validación:**
- **Error** (❌): Debe corregirse
- **Warning** (⚠️): Recomendado corregir
- **Info** (ℹ️): Informativo

### Guardar y Cargar

#### Auto-guardado Local

El sistema guarda automáticamente en `localStorage` del navegador.

**Guardar manualmente:**
```
Click en [💾] en la barra superior
```

**Cargar guardado:**
```
Menú (⋮) → Cargar Guardada
```

**Nota**: El indicador naranja (●) muestra cambios sin guardar.

### Exportación

#### Exportar a Markdown

```javascript
// Lo que se exporta:
- Metadata como header
- Tabla de contenidos automática
- Todas las secciones ordenadas
- Formato markdown estándar
```

#### Exportar a JSON

```json
{
  "metadata": { ... },
  "sections": [
    {
      "id": "section-1",
      "type": "rag-system",
      "title": "Sistema RAG",
      "order": 0,
      "content": { ... }
    }
  ]
}
```

#### Exportar a HTML

HTML completo con estilos incluidos, listo para compartir o imprimir.

---

## 🏗️ Arquitectura

Ver [ARCHITECTURE.md](./ARCHITECTURE.md) para documentación completa.

### Estructura de Carpetas

```
simbai/
├── spec-builder.html           # Interfaz principal
├── ARCHITECTURE.md             # Documentación arquitectura
├── README.md                   # Este archivo
│
├── assets/
│   ├── css/
│   │   └── spec-builder.css    # Estilos personalizados
│   └── js/
│       └── custom/
│           ├── core/
│           │   ├── SpecBuilder.js      # Orquestador
│           │   ├── TemplateEngine.js   # Templates
│           │   ├── Validator.js        # Validación
│           │   └── Exporter.js         # Exportación
│           ├── ui/                     # (futuro)
│           └── utils/                  # (futuro)
│
├── data/
│   ├── schemas/
│   │   └── specification-schema.json   # JSON Schema
│   └── templates/                      # (futuro)
│
└── examples/
    └── sample-spec.json                # Ejemplo completo
```

### Módulos Core

#### SpecBuilder.js

Orquestador principal del sistema.

```javascript
const specBuilder = new SpecBuilder({
    templateEngine,
    validator,
    exporter
});

// API pública
specBuilder.addSection(type, data);
specBuilder.updateSection(id, updates);
specBuilder.removeSection(id);
specBuilder.validate();
specBuilder.export('markdown');
specBuilder.save();
specBuilder.load();
```

#### TemplateEngine.js

Motor de templates y renderizado.

```javascript
const templateEngine = new TemplateEngine();
await templateEngine.init();

// Obtener templates
const templates = templateEngine.getAllTemplates();
const template = templateEngine.getTemplate('rag-system');

// Renderizar
const markdown = templateEngine.render('rag-system', data);
```

#### Validator.js

Sistema de validación.

```javascript
const validator = new Validator();

// Validar especificación completa
const result = validator.validate(specification);
// { valid: true/false, errors: [...] }

// Validar sección
const sectionResult = validator.validateSection(section);
```

#### Exporter.js

Motor de exportación.

```javascript
const exporter = new Exporter(templateEngine);

// Exportar
const markdown = exporter.toMarkdown(spec);
const json = exporter.toJSON(spec);
const html = exporter.toHTML(spec);

// Descargar
exporter.downloadMarkdown(spec);
exporter.downloadJSON(spec);
exporter.downloadHTML(spec);
```

---

## 🔧 Desarrollo

### Agregar Nuevo Template

**Paso 1**: Registrar template en `TemplateEngine.js`

```javascript
// En registerDefaultTemplates()
this.registerTemplate('mi-seccion', {
    id: 'mi-seccion',
    name: 'Mi Sección Personalizada',
    icon: '⭐',
    category: 'custom',
    fields: {
        titulo: { type: 'text', label: 'Título', required: true },
        descripcion: { type: 'textarea', label: 'Descripción' },
        items: { type: 'list', label: 'Items' }
    }
});
```

**Paso 2**: Crear función de renderizado (opcional)

```javascript
// Si quieres renderizado personalizado
this.registerTemplate('mi-seccion', {
    // ... campos anteriores ...
    render: (data) => {
        return `
## ${data.titulo}

${data.descripcion}

### Items:
${data.items.map(item => `- ${item}`).join('\n')}
        `.trim();
    }
});
```

**Paso 3**: Actualizar schema JSON (opcional)

En `data/schemas/specification-schema.json`:

```json
{
  "sections": {
    "items": {
      "properties": {
        "type": {
          "enum": [
            "system-overview",
            "mi-seccion",  // <- Agregar aquí
            "..."
          ]
        }
      }
    }
  }
}
```

### Agregar Regla de Validación

En `Validator.js`:

```javascript
// En registerDefaultRules()
this.registerRule('mi-regla-custom', (spec) => {
    const errors = [];

    // Tu lógica de validación
    spec.sections.forEach((section, index) => {
        if (section.type === 'mi-seccion') {
            if (!section.content.items || section.content.items.length === 0) {
                errors.push({
                    type: 'warning',
                    field: `sections[${index}].content.items`,
                    message: 'La sección debe tener al menos un item'
                });
            }
        }
    });

    return errors;
});
```

### Agregar Exportador Custom

En `Exporter.js`:

```javascript
// Registrar exportador para sección específica
exporter.registerSectionExporter('mi-seccion', (section) => {
    return `
## ${section.title}

**Descripción**: ${section.content.descripcion}

**Items importantes**:
${section.content.items.map(item => `1. ${item}`).join('\n')}
    `.trim();
});
```

### Estilos Personalizados

En `assets/css/spec-builder.css`:

```css
/* Estilo para tu template */
.section-item[data-type="mi-seccion"] {
    border-left-color: #your-color;
}

.section-item[data-type="mi-seccion"] .item-media {
    color: #your-color;
}
```

---

## 📚 API Reference

### SpecBuilder API

```javascript
// Constructor
new SpecBuilder(options)

// State Management
.getState()                    // Obtener estado actual
.markDirty()                   // Marcar como modificado
.isDirty()                     // Verificar si hay cambios

// Sections
.addSection(type, data)        // Agregar sección
.updateSection(id, updates)    // Actualizar sección
.removeSection(id)             // Eliminar sección
.getSection(id)                // Obtener sección
.getAllSections()              // Obtener todas
.reorderSections(from, to)     // Reordenar

// Metadata
.updateMetadata(metadata)      // Actualizar metadata

// Validation
.validate()                    // Validar todo
                              // Returns: { valid, errors, errorCount, warningCount }

// Export
.export(format)                // Exportar ('markdown' | 'json' | 'html')

// Persistence
.save()                        // Guardar en localStorage
.load(data?)                   // Cargar de localStorage o data
.clear()                       // Limpiar todo

// Events
.on(event, callback)           // Registrar listener
.off(event, callback)          // Quitar listener
.emit(event, data)             // Emitir evento
```

**Eventos disponibles:**

```javascript
specBuilder.on('section-added', (section) => { });
specBuilder.on('section-updated', (section) => { });
specBuilder.on('section-removed', (section) => { });
specBuilder.on('sections-reordered', () => { });
specBuilder.on('metadata-updated', (metadata) => { });
specBuilder.on('validation-complete', (result) => { });
specBuilder.on('exported', ({ format, content }) => { });
specBuilder.on('saved', () => { });
specBuilder.on('loaded', () => { });
```

### TemplateEngine API

```javascript
// Initialization
await templateEngine.init()

// Templates
.registerTemplate(id, template)
.getTemplate(id)
.getAllTemplates(category?)
.getCategories()
.hasTemplate(id)

// Blocks
.registerBlock(id, block)
.renderBlock(blockId, data)
.hasBlock(id)

// Rendering
.render(templateId, data)
```

### Validator API

```javascript
// Rules
.registerRule(name, ruleFn)
.removeRule(name)
.hasRule(name)
.getRules()

// Validation
.validate(specification, rulesToRun?)
.validateSection(section, templateId?)
.validateAgainstTemplate(section, templateId)

// Utilities
.getErrorsByType(errors, type)
.formatErrors(errors)
```

### Exporter API

```javascript
// Export
.toMarkdown(specification)
.toJSON(specification)
.toHTML(specification)

// Download
.download(content, filename, mimeType)
.downloadMarkdown(specification, filename?)
.downloadJSON(specification, filename?)
.downloadHTML(specification, filename?)

// Custom Exporters
.registerSectionExporter(sectionType, exporterFn)
```

---

## 💡 Ejemplos

### Ejemplo 1: Crear Especificación Programáticamente

```javascript
// Inicializar
const templateEngine = new TemplateEngine();
const validator = new Validator();
const exporter = new Exporter(templateEngine);
const builder = new SpecBuilder({ templateEngine, validator, exporter });

await templateEngine.init();

// Configurar metadata
builder.updateMetadata({
    title: 'Mi Proyecto Awesome',
    version: '2.0.0',
    author: 'Juan Pérez'
});

// Agregar secciones
builder.addSection('system-overview', {
    title: 'Visión General',
    content: {
        description: 'Este es un sistema genial...',
        features: [
            'Feature 1',
            'Feature 2',
            'Feature 3'
        ]
    }
});

builder.addSection('rag-system', {
    title: 'Sistema de Búsqueda',
    content: {
        ragDescription: 'Usamos RAG para...',
        searchSteps: [
            'Paso 1: Analizar',
            'Paso 2: Buscar',
            'Paso 3: Responder'
        ]
    }
});

// Validar
const result = builder.validate();
console.log('Válido:', result.valid);
console.log('Errores:', result.errorCount);

// Exportar
const markdown = builder.export('markdown');
console.log(markdown);

// Guardar
builder.save();
```

### Ejemplo 2: Cargar desde JSON

```javascript
// Cargar ejemplo
const response = await fetch('./examples/sample-spec.json');
const specData = await response.json();

// Cargar en builder
builder.load(specData);

// Ya está listo para editar o exportar
```

### Ejemplo 3: Validación Custom

```javascript
// Registrar regla personalizada
validator.registerRule('max-sections', (spec) => {
    const errors = [];
    const MAX_SECTIONS = 15;

    if (spec.sections.length > MAX_SECTIONS) {
        errors.push({
            type: 'warning',
            field: 'sections',
            message: `Tienes ${spec.sections.length} secciones. Considera dividir en múltiples documentos (máx recomendado: ${MAX_SECTIONS})`
        });
    }

    return errors;
});

// Validar con regla custom
const result = validator.validate(specification);
```

### Ejemplo 4: Export Custom

```javascript
// Exportador personalizado para una sección
exporter.registerSectionExporter('rag-system', (section) => {
    let md = `## 🔍 ${section.title}\n\n`;

    md += `> ${section.content.ragDescription}\n\n`;

    md += `### Flujo de Búsqueda\n\n`;
    section.content.searchSteps.forEach((step, i) => {
        md += `${i + 1}. **${step}**\n`;
    });

    md += `\n### Fuentes Disponibles\n\n`;
    section.content.sources.forEach(source => {
        md += `- ✅ ${source}\n`;
    });

    return md;
});

// Ahora al exportar, usará este formato personalizado
const markdown = builder.export('markdown');
```

---

## ❓ FAQ

### ¿Dónde se guardan mis especificaciones?

En `localStorage` del navegador. Cada especificación se guarda con la clave `simba-specification`.

**Importante**: Si limpias el caché del navegador, perderás los datos guardados. Exporta frecuentemente.

### ¿Puedo usar esto sin internet?

Sí, una vez cargada la página por primera vez. Los recursos (Framework7, Lit HTML) se cargan desde CDN pero quedan en caché del navegador.

### ¿Cómo comparto una especificación?

Exporta a JSON y comparte el archivo. Otros pueden importarlo usando:

```javascript
builder.load(jsonData);
```

### ¿Puedo tener múltiples especificaciones?

Actualmente solo una especificación se guarda en localStorage. Para múltiples:

1. Exporta cada una a JSON
2. Guárdalas con nombres diferentes
3. Importa la que necesites trabajar

**Futuro**: Sistema de múltiples especificaciones guardadas.

### ¿Cómo migro mi specifications.md existente?

Actualmente es manual:

1. Crea nueva especificación
2. Agrega secciones según tu MD
3. Copia el contenido campo por campo

**Futuro**: Importador automático desde Markdown.

### ¿Puedo usar mis propios templates?

Sí! Ver sección [Desarrollo → Agregar Nuevo Template](#agregar-nuevo-template).

### ¿Es compatible con móviles?

Sí, Framework7 es mobile-first. Funciona en smartphones y tablets.

### ¿Puedo contribuir templates?

¡Por supuesto! Crea un PR con:
- Template en `TemplateEngine.js`
- Ejemplo en `examples/`
- Documentación en este README

---

## 🤝 Contribución

### Reportar Bugs

Abre un issue con:
- Descripción del problema
- Pasos para reproducir
- Screenshots si aplica
- Console errors (F12 → Console)

### Sugerir Features

Abre un issue con:
- Descripción de la feature
- Caso de uso
- Mockups si aplica

### Pull Requests

1. Fork el proyecto
2. Crea branch: `git checkout -b feature/mi-feature`
3. Commit: `git commit -m 'Add: mi feature'`
4. Push: `git push origin feature/mi-feature`
5. Abre PR

---

## 📄 License

MIT License - ver [LICENSE](LICENSE) para detalles.

---

## 🙏 Créditos

- **Framework7**: https://framework7.io/
- **Lit HTML**: https://lit.dev/
- **Material Icons**: https://fonts.google.com/icons
- **Font Awesome**: https://fontawesome.com/

---

## 📞 Soporte

¿Necesitas ayuda?

- 📧 Email: support@simba.spec
- 💬 Discord: [SIMBA Community](https://discord.gg/simba)
- 📖 Docs: [https://simba.spec/docs](https://simba.spec/docs)

---

**Hecho con ❤️ por el equipo SIMBA**

*Última actualización: 2024-12-11*
