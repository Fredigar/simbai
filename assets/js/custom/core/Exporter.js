/**
 * Exporter.js
 * Export engine for specifications
 *
 * Responsibilities:
 * - Export to Markdown format
 * - Export to JSON format
 * - Export to HTML format
 * - Handle section-specific exporters
 *
 * @module Exporter
 */

class Exporter {
    constructor(templateEngine = null) {
        this.templateEngine = templateEngine;
        this.sectionExporters = new Map();
        this.registerDefaultExporters();
    }

    /**
     * Register default section exporters
     */
    registerDefaultExporters() {
        // Each section type can have custom export logic
        // Default is to use templateEngine.render()
    }

    /**
     * Export specification to Markdown
     * @param {Object} specification - Specification to export
     * @returns {string} Markdown content
     */
    toMarkdown(specification) {
        let markdown = '';

        // Add header
        markdown += this.generateHeader(specification.metadata);
        markdown += '\n\n';

        // Add table of contents
        markdown += this.generateTableOfContents(specification.sections);
        markdown += '\n\n';

        markdown += '---\n\n';

        // Add each section
        specification.sections
            .sort((a, b) => a.order - b.order)
            .forEach(section => {
                markdown += this.exportSection(section);
                markdown += '\n\n';
            });

        return markdown.trim();
    }

    /**
     * Generate header with metadata
     * @param {Object} metadata - Specification metadata
     * @returns {string} Markdown header
     */
    generateHeader(metadata) {
        return `# ${metadata.title || 'Sin Título'}

**Versión**: ${metadata.version || '1.0.0'}
**Autor**: ${metadata.author || 'No especificado'}
**Creado**: ${this.formatDate(metadata.created)}
**Última actualización**: ${this.formatDate(metadata.updated)}`;
    }

    /**
     * Generate table of contents
     * @param {Array} sections - Array of sections
     * @returns {string} Markdown TOC
     */
    generateTableOfContents(sections) {
        if (!sections || sections.length === 0) {
            return '';
        }

        let toc = '## 📋 ÍNDICE DE CONTENIDOS\n\n';

        sections
            .sort((a, b) => a.order - b.order)
            .forEach((section, index) => {
                const number = index + 1;
                const anchor = this.generateAnchor(section.title);
                toc += `${number}. **[${section.title}](#${anchor})**\n`;
            });

        return toc;
    }

    /**
     * Export a single section
     * @param {Object} section - Section to export
     * @returns {string} Markdown content
     */
    exportSection(section) {
        // Check for custom exporter
        if (this.sectionExporters.has(section.type)) {
            const exporter = this.sectionExporters.get(section.type);
            return exporter(section);
        }

        // Use template engine if available
        if (this.templateEngine) {
            try {
                return this.templateEngine.render(section.type, {
                    ...section.content,
                    title: section.title
                });
            } catch (error) {
                console.warn(`Template not found for ${section.type}, using default export`);
            }
        }

        // Default export
        return this.defaultExportSection(section);
    }

    /**
     * Default section export
     * @param {Object} section - Section to export
     * @returns {string} Markdown content
     */
    defaultExportSection(section) {
        let md = `## ${section.title}\n\n`;

        // Export content based on structure
        if (section.content) {
            Object.entries(section.content).forEach(([key, value]) => {
                md += this.exportContentField(key, value);
            });
        }

        return md;
    }

    /**
     * Export a content field
     * @param {string} key - Field name
     * @param {*} value - Field value
     * @returns {string} Markdown content
     */
    exportContentField(key, value) {
        if (value === null || value === undefined) {
            return '';
        }

        // Array (list)
        if (Array.isArray(value)) {
            let md = `### ${this.humanizeKey(key)}\n\n`;
            value.forEach(item => {
                if (typeof item === 'object') {
                    md += this.exportObject(item);
                } else {
                    md += `- ${item}\n`;
                }
            });
            return md + '\n';
        }

        // Object
        if (typeof value === 'object') {
            let md = `### ${this.humanizeKey(key)}\n\n`;
            md += this.exportObject(value);
            return md + '\n';
        }

        // String or primitive
        const heading = `### ${this.humanizeKey(key)}\n\n`;
        return heading + value + '\n\n';
    }

    /**
     * Export object as markdown
     * @param {Object} obj - Object to export
     * @returns {string} Markdown content
     */
    exportObject(obj) {
        let md = '';

        Object.entries(obj).forEach(([key, value]) => {
            if (Array.isArray(value)) {
                md += `**${this.humanizeKey(key)}**:\n`;
                value.forEach(item => {
                    md += `- ${item}\n`;
                });
            } else if (typeof value === 'object') {
                md += `**${this.humanizeKey(key)}**:\n`;
                md += this.exportObject(value);
            } else {
                md += `**${this.humanizeKey(key)}**: ${value}\n`;
            }
        });

        return md;
    }

    /**
     * Export specification to JSON
     * @param {Object} specification - Specification to export
     * @returns {string} JSON string
     */
    toJSON(specification) {
        return JSON.stringify(specification, null, 2);
    }

    /**
     * Export specification to HTML
     * @param {Object} specification - Specification to export
     * @returns {string} HTML content
     */
    toHTML(specification) {
        const markdown = this.toMarkdown(specification);

        // Basic markdown to HTML conversion
        // In production, use a library like marked.js
        let html = `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${specification.metadata.title}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 { border-bottom: 3px solid #667eea; padding-bottom: 10px; }
        h2 { margin-top: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }
        h3 { margin-top: 20px; color: #667eea; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        ul, ol { padding-left: 30px; }
        a { color: #667eea; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
${this.markdownToHTMLBasic(markdown)}
</body>
</html>`;

        return html;
    }

    /**
     * Basic markdown to HTML conversion
     * @param {string} markdown - Markdown content
     * @returns {string} HTML content
     */
    markdownToHTMLBasic(markdown) {
        return markdown
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/^- (.*$)/gim, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
            .replace(/\n/g, '<br>')
            .replace(/^(.+)$/gim, '<p>$1</p>');
    }

    /**
     * Register a custom section exporter
     * @param {string} sectionType - Section type
     * @param {Function} exporterFn - Exporter function
     */
    registerSectionExporter(sectionType, exporterFn) {
        this.sectionExporters.set(sectionType, exporterFn);
    }

    /**
     * Generate anchor for heading
     * @param {string} text - Heading text
     * @returns {string} Anchor slug
     */
    generateAnchor(text) {
        return text
            .toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/--+/g, '-')
            .trim();
    }

    /**
     * Humanize a key name
     * @param {string} key - Key to humanize
     * @returns {string} Humanized key
     */
    humanizeKey(key) {
        return key
            .replace(/([A-Z])/g, ' $1')
            .replace(/^./, str => str.toUpperCase())
            .trim();
    }

    /**
     * Format date
     * @param {string} dateString - ISO date string
     * @returns {string} Formatted date
     */
    formatDate(dateString) {
        if (!dateString) return 'No especificado';

        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    /**
     * Download content as file
     * @param {string} content - File content
     * @param {string} filename - File name
     * @param {string} mimeType - MIME type
     */
    download(content, filename, mimeType = 'text/plain') {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * Export and download as markdown
     * @param {Object} specification - Specification to export
     * @param {string} filename - Optional filename
     */
    downloadMarkdown(specification, filename = 'specifications.md') {
        const content = this.toMarkdown(specification);
        this.download(content, filename, 'text/markdown');
    }

    /**
     * Export and download as JSON
     * @param {Object} specification - Specification to export
     * @param {string} filename - Optional filename
     */
    downloadJSON(specification, filename = 'specification.json') {
        const content = this.toJSON(specification);
        this.download(content, filename, 'application/json');
    }

    /**
     * Export and download as HTML
     * @param {Object} specification - Specification to export
     * @param {string} filename - Optional filename
     */
    downloadHTML(specification, filename = 'specification.html') {
        const content = this.toHTML(specification);
        this.download(content, filename, 'text/html');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Exporter;
}
