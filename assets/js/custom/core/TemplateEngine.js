/**
 * TemplateEngine.js
 * Template rendering engine using Lit HTML patterns
 *
 * Responsibilities:
 * - Load and manage templates
 * - Render templates with data
 * - Register custom templates
 *
 * @module TemplateEngine
 */

class TemplateEngine {
    constructor() {
        this.templates = new Map();
        this.blocks = new Map();
        this.initialized = false;
    }

    /**
     * Initialize and load all templates
     * @returns {Promise<void>}
     */
    async init() {
        if (this.initialized) return;

        // Register default section templates
        this.registerDefaultTemplates();

        // Register default blocks
        this.registerDefaultBlocks();

        this.initialized = true;
    }

    /**
     * Register default section templates
     */
    registerDefaultTemplates() {
        // System Overview Template
        this.registerTemplate('system-overview', {
            id: 'system-overview',
            name: 'Sistema de Asistentes Múltiples',
            icon: '🤖',
            category: 'core',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                description: { type: 'textarea', label: 'Descripción', required: true },
                features: { type: 'list', label: 'Características Principales' }
            }
        });

        // Features Template
        this.registerTemplate('features', {
            id: 'features',
            name: 'Gestión de Conversaciones',
            icon: '💬',
            category: 'core',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                subtitle: { type: 'text', label: 'Subtítulo' },
                features: { type: 'list', label: 'Features' }
            }
        });

        // RAG System Template
        this.registerTemplate('rag-system', {
            id: 'rag-system',
            name: 'Sistema RAG',
            icon: '🔍',
            category: 'ai',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                ragDescription: { type: 'textarea', label: '¿Qué es RAG?' },
                searchSteps: { type: 'list', label: 'Pasos de Búsqueda' },
                sources: { type: 'list', label: 'Fuentes de Datos' }
            }
        });

        // Tools System Template
        this.registerTemplate('tools-dynamic', {
            id: 'tools-dynamic',
            name: 'Sistema de Herramientas',
            icon: '🛠️',
            category: 'system',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                architecture: { type: 'textarea', label: 'Arquitectura' },
                providers: { type: 'list', label: 'Providers Disponibles' },
                configuration: { type: 'code', label: 'Configuración YAML', language: 'yaml' }
            }
        });

        // File Upload Template
        this.registerTemplate('file-upload', {
            id: 'file-upload',
            name: 'Subida de Archivos',
            icon: '📎',
            category: 'features',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                supportedFormats: { type: 'list', label: 'Formatos Soportados' },
                processing: { type: 'textarea', label: 'Procesamiento' }
            }
        });

        // Image Analysis Template
        this.registerTemplate('image-analysis', {
            id: 'image-analysis',
            name: 'Análisis de Imágenes',
            icon: '🖼️',
            category: 'ai',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                visionCapabilities: { type: 'list', label: 'Capacidades Vision AI' },
                analysisTypes: { type: 'list', label: 'Tipos de Análisis' }
            }
        });

        // Reasoning System Template
        this.registerTemplate('reasoning', {
            id: 'reasoning',
            name: 'Sistema de Reasoning',
            icon: '🧠',
            category: 'ai',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                description: { type: 'textarea', label: 'Descripción' },
                phases: { type: 'list', label: 'Fases de Ejecución' },
                features: { type: 'list', label: 'Características' }
            }
        });

        // Data Visualization Template
        this.registerTemplate('data-viz', {
            id: 'data-viz',
            name: 'Visualización de Datos',
            icon: '📊',
            category: 'features',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                tableFeatures: { type: 'list', label: 'Features de Tablas' },
                chartTypes: { type: 'list', label: 'Tipos de Gráficos' }
            }
        });

        // References Template
        this.registerTemplate('references', {
            id: 'references',
            name: 'Gestión de Referencias',
            icon: '🔗',
            category: 'features',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                description: { type: 'textarea', label: 'Descripción' },
                features: { type: 'list', label: 'Características' }
            }
        });

        // UI Features Template
        this.registerTemplate('ui-features', {
            id: 'ui-features',
            name: 'Características de Interfaz',
            icon: '🎨',
            category: 'ui',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                features: { type: 'list', label: 'Features UI' },
                interactions: { type: 'list', label: 'Interacciones' }
            }
        });

        // Configuration Template
        this.registerTemplate('configuration', {
            id: 'configuration',
            name: 'Configuración',
            icon: '⚙️',
            category: 'system',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                settings: { type: 'list', label: 'Configuraciones' },
                advanced: { type: 'textarea', label: 'Opciones Avanzadas' }
            }
        });

        // Export/History Template
        this.registerTemplate('export-history', {
            id: 'export-history',
            name: 'Exportación e Historial',
            icon: '📤',
            category: 'features',
            fields: {
                title: { type: 'text', label: 'Título', required: true },
                exportFormats: { type: 'list', label: 'Formatos de Exportación' },
                historyFeatures: { type: 'list', label: 'Features de Historial' }
            }
        });
    }

    /**
     * Register default reusable blocks
     */
    registerDefaultBlocks() {
        // Code Block
        this.registerBlock('code-block', {
            id: 'code-block',
            name: 'Bloque de Código',
            render: (data) => {
                return `\`\`\`${data.language || 'javascript'}\n${data.code}\n\`\`\``;
            }
        });

        // List Block
        this.registerBlock('list-block', {
            id: 'list-block',
            name: 'Lista',
            render: (data) => {
                const items = data.items || [];
                return items.map(item => `- ${item}`).join('\n');
            }
        });

        // Table Block
        this.registerBlock('table-block', {
            id: 'table-block',
            name: 'Tabla',
            render: (data) => {
                if (!data.headers || !data.rows) return '';

                const headers = `| ${data.headers.join(' | ')} |`;
                const separator = `| ${data.headers.map(() => '---').join(' | ')} |`;
                const rows = data.rows.map(row =>
                    `| ${row.join(' | ')} |`
                ).join('\n');

                return `${headers}\n${separator}\n${rows}`;
            }
        });

        // Diagram Block
        this.registerBlock('diagram-block', {
            id: 'diagram-block',
            name: 'Diagrama',
            render: (data) => {
                return `\`\`\`\n${data.diagram}\n\`\`\``;
            }
        });
    }

    /**
     * Register a template
     * @param {string} id - Template ID
     * @param {Object} template - Template definition
     */
    registerTemplate(id, template) {
        this.templates.set(id, {
            ...template,
            id
        });
    }

    /**
     * Register a block
     * @param {string} id - Block ID
     * @param {Object} block - Block definition
     */
    registerBlock(id, block) {
        this.blocks.set(id, {
            ...block,
            id
        });
    }

    /**
     * Get template by ID
     * @param {string} id - Template ID
     * @returns {Object|null} Template or null
     */
    getTemplate(id) {
        return this.templates.get(id) || null;
    }

    /**
     * Get all templates
     * @param {string} category - Optional category filter
     * @returns {Array} Array of templates
     */
    getAllTemplates(category = null) {
        const templates = Array.from(this.templates.values());

        if (category) {
            return templates.filter(t => t.category === category);
        }

        return templates;
    }

    /**
     * Get template categories
     * @returns {Array} Array of categories
     */
    getCategories() {
        const categories = new Set();
        this.templates.forEach(template => {
            if (template.category) {
                categories.add(template.category);
            }
        });
        return Array.from(categories);
    }

    /**
     * Render a template with data
     * @param {string} templateId - Template ID
     * @param {Object} data - Data to render
     * @returns {string} Rendered content
     */
    render(templateId, data = {}) {
        const template = this.getTemplate(templateId);
        if (!template) {
            throw new Error(`Template not found: ${templateId}`);
        }

        // Custom render function if provided
        if (template.render) {
            return template.render(data);
        }

        // Default rendering logic
        return this.renderDefault(template, data);
    }

    /**
     * Default rendering logic
     * @param {Object} template - Template definition
     * @param {Object} data - Data to render
     * @returns {string} Rendered markdown
     */
    renderDefault(template, data) {
        let output = `## ${data.title || template.name}\n\n`;

        // Render each field based on type
        Object.keys(template.fields).forEach(fieldName => {
            const field = template.fields[fieldName];
            const value = data[fieldName];

            if (!value) return;

            switch (field.type) {
                case 'text':
                    output += `### ${field.label}\n${value}\n\n`;
                    break;

                case 'textarea':
                    output += `### ${field.label}\n${value}\n\n`;
                    break;

                case 'list':
                    output += `### ${field.label}\n`;
                    if (Array.isArray(value)) {
                        value.forEach(item => {
                            output += `- ${item}\n`;
                        });
                    }
                    output += '\n';
                    break;

                case 'code':
                    output += `### ${field.label}\n`;
                    output += `\`\`\`${field.language || 'javascript'}\n${value}\n\`\`\`\n\n`;
                    break;

                default:
                    output += `${value}\n\n`;
            }
        });

        return output;
    }

    /**
     * Render a block with data
     * @param {string} blockId - Block ID
     * @param {Object} data - Block data
     * @returns {string} Rendered content
     */
    renderBlock(blockId, data) {
        const block = this.blocks.get(blockId);
        if (!block) {
            throw new Error(`Block not found: ${blockId}`);
        }

        return block.render(data);
    }

    /**
     * Check if template exists
     * @param {string} id - Template ID
     * @returns {boolean} Exists status
     */
    hasTemplate(id) {
        return this.templates.has(id);
    }

    /**
     * Check if block exists
     * @param {string} id - Block ID
     * @returns {boolean} Exists status
     */
    hasBlock(id) {
        return this.blocks.has(id);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TemplateEngine;
}
