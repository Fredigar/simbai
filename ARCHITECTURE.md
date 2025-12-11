# SIMBA Specification Builder - Architecture

## 📋 ÍNDICE

1. [Visión General](#visión-general)
2. [Principios de Diseño](#principios-de-diseño)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Módulos y Responsabilidades](#módulos-y-responsabilidades)
5. [Flujo de Datos](#flujo-de-datos)
6. [Patrones de Template](#patrones-de-template)
7. [Sistema de Validación](#sistema-de-validación)
8. [Extensibilidad](#extensibilidad)

---

## 1. Visión General

**Specification Builder** es un framework modular para crear, editar y mantener documentos `specifications.md` de manera estructurada y consistente.

### Objetivos

- ✅ **Modularidad**: Cada sección es un componente independiente
- ✅ **Reutilización**: Templates compartidos entre proyectos
- ✅ **Validación**: Garantizar consistencia y completitud
- ✅ **Mantenibilidad**: Código organizado y documentado
- ✅ **Extensibilidad**: Fácil agregar nuevas secciones

### Stack Tecnológico

- **Frontend Framework**: Framework7 (UI components)
- **Template Engine**: Lit HTML (`$h` notation)
- **State Management**: Reactive properties pattern
- **Styling**: Utility CSS + Component styles
- **Build**: Vanilla JS (no build step required)

---

## 2. Principios de Diseño

### Single Responsibility Principle
Cada módulo tiene UNA responsabilidad:
- `SpecBuilder.js` → Orquesta la construcción
- `TemplateEngine.js` → Renderiza templates
- `Validator.js` → Valida contenido
- `Exporter.js` → Exporta a markdown

### Separation of Concerns
```
UI Layer (spec-builder.html)
    ↓
Business Logic (core/*.js)
    ↓
Data Layer (templates/*.json)
```

### Dependency Injection
Los módulos reciben sus dependencias explícitamente:
```javascript
const builder = new SpecBuilder({
    templateEngine: new TemplateEngine(),
    validator: new Validator(),
    exporter: new Exporter()
});
```

### Centralized State
Estado único de la aplicación:
```javascript
state = {
    specification: {},      // Contenido actual
    sections: [],          // Secciones agregadas
    metadata: {},          // Meta información
    validationErrors: [],  // Errores de validación
    isDirty: false        // Cambios sin guardar
}
```

---

## 3. Arquitectura del Sistema

### Estructura de Carpetas

```
simbai/
├── ARCHITECTURE.md              # Este documento
├── README.md                    # Guía de uso
├── specifications.md            # Especificación generada
│
├── spec-builder.html           # Interfaz principal del builder
│
├── assets/
│   ├── css/
│   │   ├── framework7.min.css
│   │   └── spec-builder.css    # Estilos personalizados
│   │
│   ├── js/
│   │   ├── vendor/
│   │   │   ├── framework7.min.js
│   │   │   └── lit-html.js
│   │   │
│   │   └── custom/
│   │       ├── core/
│   │       │   ├── SpecBuilder.js       # Constructor principal
│   │       │   ├── TemplateEngine.js    # Motor de templates
│   │       │   ├── Validator.js         # Validador
│   │       │   └── Exporter.js          # Exportador
│   │       │
│   │       ├── ui/
│   │       │   ├── SectionEditor.js     # Editor de sección
│   │       │   ├── PreviewPane.js       # Vista previa
│   │       │   └── ToolbarActions.js    # Acciones de toolbar
│   │       │
│   │       └── utils/
│   │           ├── markdown.js          # Utilidades MD
│   │           └── storage.js           # Persistencia
│   │
│   └── icons/
│       └── spec-builder-icon.svg
│
├── partials/
│   ├── navbar.html              # Barra de navegación
│   ├── toolbar.html             # Barra de herramientas
│   └── sidebar.html             # Panel lateral
│
├── components/
│   └── templates/
│       ├── sections/
│       │   ├── system-overview.html
│       │   ├── features.html
│       │   ├── rag-system.html
│       │   ├── tools-dynamic.html
│       │   ├── file-upload.html
│       │   ├── image-analysis.html
│       │   ├── reasoning.html
│       │   ├── data-viz.html
│       │   ├── references.html
│       │   ├── ui-features.html
│       │   ├── configuration.html
│       │   └── export-history.html
│       │
│       ├── blocks/
│       │   ├── code-block.html
│       │   ├── diagram-block.html
│       │   ├── list-block.html
│       │   └── table-block.html
│       │
│       └── base-template.html    # Template base
│
├── data/
│   ├── templates/
│   │   └── default-spec.json     # Estructura por defecto
│   │
│   └── schemas/
│       └── specification-schema.json  # JSON Schema para validación
│
└── examples/
    ├── simple-spec.json          # Ejemplo simple
    └── complex-spec.json         # Ejemplo complejo
```

---

## 4. Módulos y Responsabilidades

### Core Modules

#### SpecBuilder.js
**Responsabilidad**: Orquestador principal del sistema

```javascript
class SpecBuilder {
    constructor(options) {
        this.state = {
            specification: {},
            sections: [],
            metadata: {},
            validationErrors: [],
            isDirty: false
        };

        this.templateEngine = options.templateEngine;
        this.validator = options.validator;
        this.exporter = options.exporter;
    }

    // API Pública
    addSection(sectionType, data) { }
    removeSection(sectionId) { }
    updateSection(sectionId, data) { }
    reorderSections(fromIndex, toIndex) { }
    validate() { }
    export(format) { }
    save() { }
    load(data) { }
}
```

**No hace**:
- ❌ Renderizado UI
- ❌ Manipulación DOM directa
- ❌ Lógica de templates

#### TemplateEngine.js
**Responsabilidad**: Renderizar templates con datos

```javascript
class TemplateEngine {
    constructor() {
        this.templates = new Map();
        this.loadTemplates();
    }

    // Cargar templates desde HTML
    async loadTemplates() { }

    // Renderizar template con datos
    render(templateName, data) { }

    // Registrar template personalizado
    registerTemplate(name, template) { }

    // Compilar template a función
    compile(templateString) { }
}
```

**Patrón usado**: Template Literals + Lit HTML

#### Validator.js
**Responsabilidad**: Validar estructura y contenido

```javascript
class Validator {
    constructor(schema) {
        this.schema = schema;
        this.rules = new Map();
        this.registerDefaultRules();
    }

    // Validar especificación completa
    validate(specification) { }

    // Validar sección específica
    validateSection(section) { }

    // Registrar regla personalizada
    registerRule(name, ruleFn) { }

    // Obtener errores
    getErrors() { }
}
```

**Reglas por defecto**:
- ✅ Todas las secciones requeridas presentes
- ✅ Contenido no vacío
- ✅ Formato correcto de código/ejemplos
- ✅ Referencias válidas
- ✅ Estructura de encabezados correcta

#### Exporter.js
**Responsabilidad**: Exportar a diferentes formatos

```javascript
class Exporter {
    // Exportar a Markdown
    toMarkdown(specification) { }

    // Exportar a JSON
    toJSON(specification) { }

    // Exportar a HTML
    toHTML(specification) { }

    // Exportar a PDF (vía HTML)
    toPDF(specification) { }
}
```

### UI Modules

#### SectionEditor.js
**Responsabilidad**: Editar contenido de una sección

```javascript
class SectionEditor extends LitElement {
    static properties = {
        section: { type: Object },
        template: { type: String },
        data: { type: Object }
    };

    render() {
        return $h`
            <div class="section-editor">
                ${this.renderFields()}
            </div>
        `;
    }

    renderFields() { }
    handleInput(field, value) { }
    validate() { }
}
```

#### PreviewPane.js
**Responsabilidad**: Vista previa del markdown generado

```javascript
class PreviewPane extends LitElement {
    static properties = {
        content: { type: String },
        mode: { type: String } // 'raw' | 'rendered'
    };

    render() {
        return $h`
            <div class="preview-pane">
                ${this.mode === 'rendered'
                    ? this.renderMarkdown()
                    : this.renderRaw()}
            </div>
        `;
    }
}
```

---

## 5. Flujo de Datos

### Flujo de Creación de Especificación

```
1. Usuario abre spec-builder.html
   ↓
2. SpecBuilder se inicializa
   ↓
3. TemplateEngine carga templates disponibles
   ↓
4. UI muestra galería de secciones disponibles
   ↓
5. Usuario selecciona sección (ej: "Sistema RAG")
   ↓
6. SectionEditor se abre con template correspondiente
   ↓
7. Usuario completa campos del formulario
   ↓
8. Validator valida datos en tiempo real
   ↓
9. SpecBuilder agrega sección al estado
   ↓
10. PreviewPane actualiza vista previa
    ↓
11. Usuario exporta a specifications.md
    ↓
12. Exporter genera markdown final
```

### Flujo de Estado (Unidireccional)

```
User Action
    ↓
Event Handler
    ↓
Update State (SpecBuilder)
    ↓
Notify Observers
    ↓
Re-render UI
    ↓
Update Preview
```

### Ejemplo de Flujo

```javascript
// 1. Usuario agrega sección
handleAddSection(sectionType) {
    const data = this.collectFormData();

    // 2. Actualizar estado
    this.specBuilder.addSection(sectionType, data);

    // 3. Validar
    const errors = this.specBuilder.validate();

    // 4. Actualizar UI
    this.updateState({
        validationErrors: errors,
        isDirty: true
    });

    // 5. Re-renderizar
    this.requestUpdate();
}
```

---

## 6. Patrones de Template

### Template Base

Todos los templates heredan de `base-template.html`:

```html
<!-- components/templates/base-template.html -->
<template id="base-section">
    <div class="spec-section" data-section-type="${type}">
        <div class="section-header">
            <h2>${title}</h2>
            <div class="section-actions">
                <button @click="${edit}">✏️ Editar</button>
                <button @click="${remove}">🗑️ Eliminar</button>
            </div>
        </div>
        <div class="section-content">
            <!-- Contenido específico aquí -->
        </div>
    </div>
</template>
```

### Template de Sección Específica

```html
<!-- components/templates/sections/rag-system.html -->
<template id="section-rag-system">
    <div class="spec-section-rag">
        <h2>🔍 ${title}</h2>

        <div class="subsection">
            <h3>¿Qué es RAG en ${systemName}?</h3>
            <textarea
                class="item-input-outline"
                @input="${updateField('ragDescription')}"
                placeholder="Describe qué es RAG en tu sistema...">
                ${data.ragDescription || ''}
            </textarea>
        </div>

        <div class="subsection">
            <h3>Búsqueda Semántica Automática</h3>
            <ul class="list">
                ${data.searchSteps.map((step, idx) => $h`
                    <li class="item-content">
                        <input
                            type="text"
                            @input="${updateStep(idx)}"
                            value="${step}"/>
                        <button @click="${removeStep(idx)}">❌</button>
                    </li>
                `)}
            </ul>
            <button @click="${addStep}">➕ Agregar Paso</button>
        </div>

        <!-- Más subsecciones... -->
    </div>
</template>
```

### Lit HTML Patterns

```javascript
// 1. Condicional simple
${showAdvanced ? $h`<div class="advanced">...</div>` : ''}

// 2. Lista
${items.map(item => $h`
    <li>${item.name}</li>
`)}

// 3. Condicional ternario
${isActive
    ? $h`<span class="active">Activo</span>`
    : $h`<span class="inactive">Inactivo</span>`
}

// 4. Event binding
<button @click="${handleClick}">Click</button>

// 5. Atributo dinámico
<input value="${value}" @input="${handleInput}"/>

// 6. Clase condicional
<div class="item ${isSelected ? 'selected' : ''}">
```

---

## 7. Sistema de Validación

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Specification",
  "type": "object",
  "required": ["metadata", "sections"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["title", "version", "author"],
      "properties": {
        "title": { "type": "string", "minLength": 1 },
        "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
        "author": { "type": "string" },
        "created": { "type": "string", "format": "date-time" },
        "updated": { "type": "string", "format": "date-time" }
      }
    },
    "sections": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "type", "title", "content"],
        "properties": {
          "id": { "type": "string" },
          "type": { "type": "string" },
          "title": { "type": "string" },
          "order": { "type": "number" },
          "content": { "type": "object" }
        }
      }
    }
  }
}
```

### Reglas de Validación

```javascript
// Regla: Título no vacío
validator.registerRule('non-empty-title', (section) => {
    if (!section.title || section.title.trim() === '') {
        return {
            valid: false,
            message: 'El título no puede estar vacío'
        };
    }
    return { valid: true };
});

// Regla: Código válido en bloques
validator.registerRule('valid-code-blocks', (section) => {
    const codeBlocks = section.content.codeBlocks || [];
    for (const block of codeBlocks) {
        if (!block.language || !block.code) {
            return {
                valid: false,
                message: 'Bloque de código incompleto'
            };
        }
    }
    return { valid: true };
});

// Regla: Referencias válidas
validator.registerRule('valid-references', (section) => {
    const refs = section.content.references || [];
    for (const ref of refs) {
        if (!ref.url || !ref.title) {
            return {
                valid: false,
                message: `Referencia inválida: ${ref.id}`
            };
        }
    }
    return { valid: true };
});
```

---

## 8. Extensibilidad

### Agregar Nueva Sección

**Paso 1**: Crear template HTML

```html
<!-- components/templates/sections/custom-section.html -->
<template id="section-custom">
    <div class="spec-section-custom">
        <h2>${title}</h2>
        <!-- Tu contenido aquí -->
    </div>
</template>
```

**Paso 2**: Registrar en TemplateEngine

```javascript
templateEngine.registerTemplate('custom-section', {
    id: 'custom-section',
    name: 'Mi Sección Personalizada',
    icon: 'fa-star',
    template: 'section-custom',
    fields: [
        { name: 'title', type: 'text', required: true },
        { name: 'description', type: 'textarea', required: true }
    ]
});
```

**Paso 3**: Crear exportador

```javascript
exporter.registerSectionExporter('custom-section', (section) => {
    return `
## ${section.title}

${section.content.description}
    `.trim();
});
```

### Agregar Validador Personalizado

```javascript
validator.registerRule('custom-validation', (section) => {
    // Tu lógica de validación
    if (section.type === 'custom-section') {
        if (section.content.description.length < 100) {
            return {
                valid: false,
                message: 'La descripción debe tener al menos 100 caracteres'
            };
        }
    }
    return { valid: true };
});
```

### Agregar Bloque Reutilizable

```html
<!-- components/templates/blocks/custom-block.html -->
<template id="block-custom">
    <div class="custom-block">
        ${content}
    </div>
</template>
```

---

## 🎯 Decisiones de Arquitectura

### ¿Por qué Lit HTML?
- ✅ Lightweight (sin framework pesado)
- ✅ Template literals nativos de JS
- ✅ Compatible con Framework7
- ✅ Reactivo y performante

### ¿Por qué Framework7?
- ✅ Ya usado en conversation.html
- ✅ Componentes UI consistentes
- ✅ Mobile-first design
- ✅ Buena documentación

### ¿Por qué NO usar React/Vue?
- ❌ Overhead innecesario para este caso
- ❌ Build step adicional
- ❌ Inconsistente con conversation.html
- ❌ Más complejo de mantener

### ¿Por qué JSON Schema?
- ✅ Estándar de industria
- ✅ Validación declarativa
- ✅ Fácil de extender
- ✅ Compatible con herramientas existentes

---

## 📊 Métricas de Calidad

### Código
- **Max líneas por función**: 50
- **Max líneas por archivo**: 500
- **Cobertura de tests**: 80%+
- **Complejidad ciclomática**: < 10

### Performance
- **Tiempo de carga**: < 2s
- **Renderizado de sección**: < 100ms
- **Exportación a MD**: < 500ms
- **Validación**: < 200ms

### Mantenibilidad
- **Documentación**: JSDoc en todas las funciones públicas
- **ARCHITECTURE.md**: Actualizado con cada cambio mayor
- **README.md**: Ejemplos de uso claros
- **Inline comments**: Solo para lógica no obvia

---

## 🔄 Evolución Futura

### Fase 1 (Actual)
- ✅ Builder básico con templates
- ✅ Exportación a Markdown
- ✅ Validación básica

### Fase 2 (Q1 2025)
- 🔲 Importar specifications.md existente
- 🔲 Versionado de especificaciones
- 🔲 Colaboración multi-usuario
- 🔲 Integración con Git

### Fase 3 (Q2 2025)
- 🔲 AI-assisted content generation
- 🔲 Template marketplace
- 🔲 Multi-idioma
- 🔲 Exportación a PDF/DOCX

---

**Última actualización**: 2024-12-11
**Versión**: 1.0.0
**Autor**: Senior Architect
