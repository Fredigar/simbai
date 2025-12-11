/**
 * Validator.js
 * Validation engine for specifications
 *
 * Responsibilities:
 * - Validate specification structure
 * - Validate section content
 * - Manage validation rules
 *
 * @module Validator
 */

class Validator {
    constructor(schema = null) {
        this.schema = schema;
        this.rules = new Map();
        this.registerDefaultRules();
    }

    /**
     * Register default validation rules
     */
    registerDefaultRules() {
        // Rule: Non-empty title
        this.registerRule('non-empty-title', (spec) => {
            const errors = [];

            if (!spec.metadata || !spec.metadata.title || spec.metadata.title.trim() === '') {
                errors.push({
                    type: 'error',
                    field: 'metadata.title',
                    message: 'El título de la especificación no puede estar vacío'
                });
            }

            spec.sections.forEach((section, index) => {
                if (!section.title || section.title.trim() === '') {
                    errors.push({
                        type: 'error',
                        field: `sections[${index}].title`,
                        message: `La sección #${index + 1} necesita un título`
                    });
                }
            });

            return errors;
        });

        // Rule: Valid version format
        this.registerRule('valid-version', (spec) => {
            const errors = [];
            const versionPattern = /^\d+\.\d+\.\d+$/;

            if (spec.metadata && spec.metadata.version) {
                if (!versionPattern.test(spec.metadata.version)) {
                    errors.push({
                        type: 'warning',
                        field: 'metadata.version',
                        message: 'La versión debe seguir el formato semver (ej: 1.0.0)'
                    });
                }
            }

            return errors;
        });

        // Rule: At least one section
        this.registerRule('minimum-sections', (spec) => {
            const errors = [];

            if (!spec.sections || spec.sections.length === 0) {
                errors.push({
                    type: 'warning',
                    field: 'sections',
                    message: 'La especificación debe tener al menos una sección'
                });
            }

            return errors;
        });

        // Rule: Unique section IDs
        this.registerRule('unique-section-ids', (spec) => {
            const errors = [];
            const ids = new Set();

            spec.sections.forEach((section, index) => {
                if (ids.has(section.id)) {
                    errors.push({
                        type: 'error',
                        field: `sections[${index}].id`,
                        message: `ID de sección duplicado: ${section.id}`
                    });
                }
                ids.add(section.id);
            });

            return errors;
        });

        // Rule: Valid code blocks
        this.registerRule('valid-code-blocks', (spec) => {
            const errors = [];

            spec.sections.forEach((section, index) => {
                if (section.content && section.content.codeBlocks) {
                    section.content.codeBlocks.forEach((block, blockIndex) => {
                        if (!block.code || block.code.trim() === '') {
                            errors.push({
                                type: 'warning',
                                field: `sections[${index}].content.codeBlocks[${blockIndex}]`,
                                message: 'Bloque de código vacío'
                            });
                        }

                        if (!block.language) {
                            errors.push({
                                type: 'info',
                                field: `sections[${index}].content.codeBlocks[${blockIndex}].language`,
                                message: 'Bloque de código sin lenguaje especificado'
                            });
                        }
                    });
                }
            });

            return errors;
        });

        // Rule: Non-empty content
        this.registerRule('non-empty-content', (spec) => {
            const errors = [];

            spec.sections.forEach((section, index) => {
                if (!section.content || Object.keys(section.content).length === 0) {
                    errors.push({
                        type: 'warning',
                        field: `sections[${index}].content`,
                        message: `La sección "${section.title}" no tiene contenido`
                    });
                }
            });

            return errors;
        });

        // Rule: Sequential order
        this.registerRule('sequential-order', (spec) => {
            const errors = [];

            spec.sections.forEach((section, index) => {
                if (section.order !== index) {
                    errors.push({
                        type: 'info',
                        field: `sections[${index}].order`,
                        message: 'El orden de las secciones no es secuencial (se puede corregir automáticamente)'
                    });
                }
            });

            return errors;
        });

        // Rule: Valid metadata
        this.registerRule('valid-metadata', (spec) => {
            const errors = [];
            const requiredFields = ['title', 'version', 'author'];

            requiredFields.forEach(field => {
                if (!spec.metadata || !spec.metadata[field]) {
                    errors.push({
                        type: 'warning',
                        field: `metadata.${field}`,
                        message: `Campo requerido en metadata: ${field}`
                    });
                }
            });

            return errors;
        });
    }

    /**
     * Register a validation rule
     * @param {string} name - Rule name
     * @param {Function} ruleFn - Rule function that returns array of errors
     */
    registerRule(name, ruleFn) {
        this.rules.set(name, ruleFn);
    }

    /**
     * Validate entire specification
     * @param {Object} specification - Specification to validate
     * @param {Array<string>} rulesToRun - Optional array of specific rules to run
     * @returns {Object} Validation result { valid: boolean, errors: Array }
     */
    validate(specification, rulesToRun = null) {
        const allErrors = [];

        // Determine which rules to run
        const rules = rulesToRun
            ? rulesToRun.map(name => [name, this.rules.get(name)]).filter(([, fn]) => fn)
            : Array.from(this.rules.entries());

        // Run all rules
        rules.forEach(([name, ruleFn]) => {
            try {
                const errors = ruleFn(specification);
                if (errors && errors.length > 0) {
                    errors.forEach(error => {
                        allErrors.push({
                            ...error,
                            rule: name
                        });
                    });
                }
            } catch (error) {
                console.error(`Error running validation rule ${name}:`, error);
                allErrors.push({
                    type: 'error',
                    rule: name,
                    message: `Error interno en regla de validación: ${error.message}`
                });
            }
        });

        // Separate by type
        const errors = allErrors.filter(e => e.type === 'error');
        const warnings = allErrors.filter(e => e.type === 'warning');
        const info = allErrors.filter(e => e.type === 'info');

        return {
            valid: errors.length === 0,
            errors: allErrors,
            errorCount: errors.length,
            warningCount: warnings.length,
            infoCount: info.length
        };
    }

    /**
     * Validate a specific section
     * @param {Object} section - Section to validate
     * @param {string} templateId - Template ID for section-specific validation
     * @returns {Object} Validation result
     */
    validateSection(section, templateId = null) {
        const errors = [];

        // Basic section validation
        if (!section.id) {
            errors.push({
                type: 'error',
                field: 'id',
                message: 'La sección debe tener un ID'
            });
        }

        if (!section.type) {
            errors.push({
                type: 'error',
                field: 'type',
                message: 'La sección debe tener un tipo'
            });
        }

        if (!section.title || section.title.trim() === '') {
            errors.push({
                type: 'error',
                field: 'title',
                message: 'La sección debe tener un título'
            });
        }

        // Template-specific validation
        if (templateId) {
            const templateErrors = this.validateAgainstTemplate(section, templateId);
            errors.push(...templateErrors);
        }

        return {
            valid: errors.filter(e => e.type === 'error').length === 0,
            errors
        };
    }

    /**
     * Validate section against template requirements
     * @param {Object} section - Section to validate
     * @param {string} templateId - Template ID
     * @returns {Array} Array of errors
     */
    validateAgainstTemplate(section, templateId) {
        // This would integrate with TemplateEngine to validate required fields
        // For now, basic implementation
        const errors = [];

        // Check if content exists
        if (!section.content) {
            errors.push({
                type: 'error',
                field: 'content',
                message: 'La sección debe tener contenido'
            });
        }

        return errors;
    }

    /**
     * Get all registered rules
     * @returns {Array} Array of rule names
     */
    getRules() {
        return Array.from(this.rules.keys());
    }

    /**
     * Remove a rule
     * @param {string} name - Rule name
     * @returns {boolean} Success status
     */
    removeRule(name) {
        return this.rules.delete(name);
    }

    /**
     * Check if rule exists
     * @param {string} name - Rule name
     * @returns {boolean} Exists status
     */
    hasRule(name) {
        return this.rules.has(name);
    }

    /**
     * Get errors of specific type
     * @param {Array} errors - All errors
     * @param {string} type - Error type (error, warning, info)
     * @returns {Array} Filtered errors
     */
    getErrorsByType(errors, type) {
        return errors.filter(e => e.type === type);
    }

    /**
     * Format errors for display
     * @param {Array} errors - Errors to format
     * @returns {string} Formatted error messages
     */
    formatErrors(errors) {
        if (!errors || errors.length === 0) {
            return 'No errors';
        }

        return errors.map(error => {
            const prefix = {
                error: '❌',
                warning: '⚠️',
                info: 'ℹ️'
            }[error.type] || '•';

            return `${prefix} ${error.message}${error.field ? ` (${error.field})` : ''}`;
        }).join('\n');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Validator;
}
