/**
 * SpecBuilder.js
 * Core orchestrator for building specifications
 *
 * Responsibilities:
 * - Manage specification state
 * - Coordinate template engine, validator, and exporter
 * - Provide public API for spec manipulation
 *
 * @module SpecBuilder
 */

class SpecBuilder {
    /**
     * Initialize the specification builder
     * @param {Object} options - Configuration options
     * @param {TemplateEngine} options.templateEngine - Template rendering engine
     * @param {Validator} options.validator - Content validator
     * @param {Exporter} options.exporter - Export functionality
     */
    constructor(options = {}) {
        this.templateEngine = options.templateEngine;
        this.validator = options.validator;
        this.exporter = options.exporter;

        // State management
        this.state = {
            specification: {
                metadata: {
                    title: '',
                    version: '1.0.0',
                    author: '',
                    created: new Date().toISOString(),
                    updated: new Date().toISOString()
                },
                sections: []
            },
            validationErrors: [],
            isDirty: false,
            selectedSectionId: null
        };

        // Event listeners
        this.listeners = new Map();

        // Section counter for unique IDs
        this.sectionCounter = 0;
    }

    /**
     * Add a new section to the specification
     * @param {string} sectionType - Type of section (e.g., 'rag-system', 'features')
     * @param {Object} data - Section data
     * @returns {Object} The created section
     */
    addSection(sectionType, data = {}) {
        const section = {
            id: `section-${++this.sectionCounter}-${Date.now()}`,
            type: sectionType,
            title: data.title || 'Nueva Sección',
            order: this.state.specification.sections.length,
            content: data.content || {},
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };

        this.state.specification.sections.push(section);
        this.markDirty();
        this.emit('section-added', section);

        return section;
    }

    /**
     * Remove a section from the specification
     * @param {string} sectionId - ID of the section to remove
     * @returns {boolean} Success status
     */
    removeSection(sectionId) {
        const index = this.state.specification.sections.findIndex(
            s => s.id === sectionId
        );

        if (index === -1) return false;

        const removed = this.state.specification.sections.splice(index, 1)[0];
        this.reorderSections();
        this.markDirty();
        this.emit('section-removed', removed);

        return true;
    }

    /**
     * Update an existing section
     * @param {string} sectionId - ID of the section
     * @param {Object} updates - Updated data
     * @returns {Object|null} Updated section or null if not found
     */
    updateSection(sectionId, updates) {
        const section = this.state.specification.sections.find(
            s => s.id === sectionId
        );

        if (!section) return null;

        Object.assign(section, {
            ...updates,
            updatedAt: new Date().toISOString()
        });

        this.markDirty();
        this.emit('section-updated', section);

        return section;
    }

    /**
     * Reorder sections
     * @param {number} fromIndex - Source index
     * @param {number} toIndex - Destination index
     */
    reorderSections(fromIndex = null, toIndex = null) {
        if (fromIndex !== null && toIndex !== null) {
            const sections = this.state.specification.sections;
            const [moved] = sections.splice(fromIndex, 1);
            sections.splice(toIndex, 0, moved);
        }

        // Update order property
        this.state.specification.sections.forEach((section, index) => {
            section.order = index;
        });

        this.markDirty();
        this.emit('sections-reordered');
    }

    /**
     * Get a section by ID
     * @param {string} sectionId - Section ID
     * @returns {Object|null} Section or null
     */
    getSection(sectionId) {
        return this.state.specification.sections.find(s => s.id === sectionId) || null;
    }

    /**
     * Get all sections
     * @returns {Array} Array of sections
     */
    getAllSections() {
        return [...this.state.specification.sections];
    }

    /**
     * Validate the entire specification
     * @returns {Object} Validation result { valid: boolean, errors: Array }
     */
    validate() {
        if (!this.validator) {
            console.warn('No validator configured');
            return { valid: true, errors: [] };
        }

        const result = this.validator.validate(this.state.specification);
        this.state.validationErrors = result.errors || [];
        this.emit('validation-complete', result);

        return result;
    }

    /**
     * Export specification to format
     * @param {string} format - Export format ('markdown', 'json', 'html')
     * @returns {string} Exported content
     */
    export(format = 'markdown') {
        if (!this.exporter) {
            throw new Error('No exporter configured');
        }

        let content;
        switch (format.toLowerCase()) {
            case 'markdown':
            case 'md':
                content = this.exporter.toMarkdown(this.state.specification);
                break;
            case 'json':
                content = this.exporter.toJSON(this.state.specification);
                break;
            case 'html':
                content = this.exporter.toHTML(this.state.specification);
                break;
            default:
                throw new Error(`Unknown export format: ${format}`);
        }

        this.emit('exported', { format, content });
        return content;
    }

    /**
     * Save specification to localStorage
     * @returns {boolean} Success status
     */
    save() {
        try {
            const data = JSON.stringify(this.state.specification);
            localStorage.setItem('simba-specification', data);
            this.state.isDirty = false;
            this.emit('saved');
            return true;
        } catch (error) {
            console.error('Error saving specification:', error);
            this.emit('save-error', error);
            return false;
        }
    }

    /**
     * Load specification from localStorage or data
     * @param {Object} data - Optional data to load
     * @returns {boolean} Success status
     */
    load(data = null) {
        try {
            if (data) {
                this.state.specification = data;
            } else {
                const saved = localStorage.getItem('simba-specification');
                if (saved) {
                    this.state.specification = JSON.parse(saved);
                }
            }

            this.state.isDirty = false;
            this.sectionCounter = this.state.specification.sections.length;
            this.emit('loaded');
            return true;
        } catch (error) {
            console.error('Error loading specification:', error);
            this.emit('load-error', error);
            return false;
        }
    }

    /**
     * Clear the current specification
     */
    clear() {
        this.state.specification = {
            metadata: {
                title: '',
                version: '1.0.0',
                author: '',
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            sections: []
        };
        this.state.validationErrors = [];
        this.state.isDirty = false;
        this.sectionCounter = 0;
        this.emit('cleared');
    }

    /**
     * Update metadata
     * @param {Object} metadata - Metadata updates
     */
    updateMetadata(metadata) {
        Object.assign(this.state.specification.metadata, {
            ...metadata,
            updated: new Date().toISOString()
        });
        this.markDirty();
        this.emit('metadata-updated', this.state.specification.metadata);
    }

    /**
     * Get current state
     * @returns {Object} Current state
     */
    getState() {
        return { ...this.state };
    }

    /**
     * Mark specification as dirty (unsaved changes)
     */
    markDirty() {
        this.state.isDirty = true;
        this.state.specification.metadata.updated = new Date().toISOString();
    }

    /**
     * Check if specification has unsaved changes
     * @returns {boolean} Dirty status
     */
    isDirty() {
        return this.state.isDirty;
    }

    /**
     * Register event listener
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     */
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    /**
     * Unregister event listener
     * @param {string} event - Event name
     * @param {Function} callback - Callback to remove
     */
    off(event, callback) {
        if (!this.listeners.has(event)) return;

        const callbacks = this.listeners.get(event);
        const index = callbacks.indexOf(callback);
        if (index > -1) {
            callbacks.splice(index, 1);
        }
    }

    /**
     * Emit event to listeners
     * @param {string} event - Event name
     * @param {*} data - Event data
     */
    emit(event, data) {
        if (!this.listeners.has(event)) return;

        this.listeners.get(event).forEach(callback => {
            try {
                callback(data);
            } catch (error) {
                console.error(`Error in event listener for ${event}:`, error);
            }
        });
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SpecBuilder;
}
