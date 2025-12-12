/**
 * SIMBA Frontend Configuration
 */

const AppConfig = {
    // Backend API Configuration
    backend: {
        baseURL: 'http://82.223.12.60:8000',
        timeout: 30000, // 30 seconds
        endpoints: {
            chat: {
                send: '/chat/send',
                stream: '/chat/stream',
                conversations: '/chat/conversations',
                messages: '/chat/messages'
            },
            documents: {
                upload: '/documents/upload',
                list: '/documents',
                delete: '/documents'
            },
            rag: {
                search: '/rag/search',
                index: '/rag/index'
            },
            health: '/health'
        }
    },

    // Default Assistant Configuration
    assistant: {
        id: 'simba-assistant',
        name: 'SIMBA',
        greeting: '¡Hola! Soy SIMBA, tu asistente inteligente. ¿En qué puedo ayudarte hoy?',
        placeholder: 'Escribe tu mensaje aquí...',
        avatar: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%232196f3"/%3E%3Ctext x="50" y="50" text-anchor="middle" dominant-baseline="central" font-size="40" fill="white" font-family="Arial"%3ES%3C/text%3E%3C/svg%3E'
    },

    // LLM Configuration
    llm: {
        defaultModel: 'gpt-3.5-turbo',
        defaultTemperature: 0.7,
        defaultMaxTokens: 2000,
        streaming: true,
        models: {
            'gpt-4': { name: 'GPT-4', provider: 'openai' },
            'gpt-3.5-turbo': { name: 'GPT-3.5 Turbo', provider: 'openai' },
            'claude-3-opus': { name: 'Claude 3 Opus', provider: 'anthropic' },
            'claude-3-sonnet': { name: 'Claude 3 Sonnet', provider: 'anthropic' }
        }
    },

    // File Upload Configuration
    fileUpload: {
        maxSize: 50 * 1024 * 1024, // 50 MB
        allowedTypes: [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ],
        allowedExtensions: ['.pdf', '.docx', '.txt'],
        autoIndex: true // Automatically index uploaded documents for RAG
    },

    // UI Configuration
    ui: {
        theme: 'auto', // 'light', 'dark', or 'auto'
        messageDateFormat: 'HH:mm',
        messageTimeFormat: 'DD/MM/YYYY HH:mm',
        loadMessagesLimit: 50,
        scrollToNewMessages: true
    },

    // Storage Keys
    storage: {
        conversations: 'simba_conversations',
        settings: 'simba_settings',
        currentConversation: 'simba_current_conversation'
    }
};

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AppConfig;
}
