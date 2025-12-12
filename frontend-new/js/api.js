/**
 * SIMBA API Client
 * Handles all communication with the SIMBA backend
 */

class SimbaAPI {
    constructor(config) {
        this.baseURL = config.backend.baseURL;
        this.timeout = config.backend.timeout;
        this.endpoints = config.backend.endpoints;
    }

    /**
     * Generic HTTP request handler
     */
    async request(method, endpoint, data = null, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        if (data && method !== 'GET') {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
                throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    /**
     * Health Check
     */
    async healthCheck() {
        return await this.request('GET', this.endpoints.health);
    }

    // ==================== Chat Endpoints ====================

    /**
     * Create a new conversation
     */
    async createConversation(assistantId, title = null, device = null) {
        return await this.request('POST', this.endpoints.chat.conversations, {
            assistant_id: assistantId,
            title,
            device
        });
    }

    /**
     * Get all conversations for a user
     */
    async getConversations(userId = 'testuser', limit = 50) {
        const endpoint = `${this.endpoints.chat.conversations}?user_id=${userId}&limit=${limit}`;
        return await this.request('GET', endpoint);
    }

    /**
     * Get messages for a conversation
     */
    async getMessages(conversationId, limit = 50) {
        const endpoint = `${this.endpoints.chat.messages}/${conversationId}?limit=${limit}`;
        return await this.request('GET', endpoint);
    }

    /**
     * Send a message (non-streaming)
     */
    async sendMessage(conversationId, content, options = {}) {
        return await this.request('POST', this.endpoints.chat.send, {
            conversation_id: conversationId,
            content,
            temperature: options.temperature,
            max_tokens: options.maxTokens
        });
    }

    /**
     * Send a message with streaming response
     */
    async sendMessageStreaming(conversationId, content, onChunk, onComplete, onError, options = {}) {
        const url = `${this.baseURL}${this.endpoints.chat.stream}`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    conversation_id: conversationId,
                    content,
                    temperature: options.temperature,
                    max_tokens: options.maxTokens
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let fullText = '';

            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    if (onComplete) onComplete(fullText);
                    break;
                }

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop(); // Keep incomplete line in buffer

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);

                        if (data === '[DONE]') {
                            if (onComplete) onComplete(fullText);
                            return;
                        }

                        try {
                            const parsed = JSON.parse(data);

                            if (parsed.content) {
                                fullText += parsed.content;
                                if (onChunk) onChunk(parsed.content, fullText);
                            }
                        } catch (e) {
                            console.warn('Failed to parse SSE data:', data);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Streaming error:', error);
            if (onError) onError(error);
            throw error;
        }
    }

    // ==================== Document Endpoints ====================

    /**
     * Upload a document
     */
    async uploadDocument(conversationId, file, autoIndex = true) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('conversation_id', conversationId);
        formData.append('auto_index', autoIndex);

        const url = `${this.baseURL}${this.endpoints.documents.upload}`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
                throw new Error(error.detail);
            }

            return await response.json();
        } catch (error) {
            console.error('Document upload error:', error);
            throw error;
        }
    }

    /**
     * Get documents for a conversation
     */
    async getDocuments(conversationId) {
        const endpoint = `${this.endpoints.documents.list}?conversation_id=${conversationId}`;
        return await this.request('GET', endpoint);
    }

    /**
     * Delete a document
     */
    async deleteDocument(documentId) {
        const endpoint = `${this.endpoints.documents.delete}/${documentId}`;
        return await this.request('DELETE', endpoint);
    }

    // ==================== RAG Endpoints ====================

    /**
     * Search documents using RAG
     */
    async searchDocuments(conversationId, query, nResults = 5) {
        return await this.request('POST', this.endpoints.rag.search, {
            conversation_id: conversationId,
            query,
            n_results: nResults
        });
    }

    /**
     * Index a document for RAG
     */
    async indexDocument(documentId, conversationId, content, chunkSize = 500, chunkOverlap = 50) {
        return await this.request('POST', this.endpoints.rag.index, {
            document_id: documentId,
            conversation_id: conversationId,
            content,
            chunk_size: chunkSize,
            chunk_overlap: chunkOverlap
        });
    }
}

// Create global API instance
const simbaAPI = new SimbaAPI(AppConfig);
