/**
 * SIMBA Frontend Application
 * Framework7 App with Chat Interface
 */

// Initialize Framework7 App
const app = new Framework7({
    el: '#app',
    name: 'SIMBA',
    theme: 'auto',
    colors: {
        primary: '#2196f3'
    },
    routes: [
        {
            path: '/',
            componentUrl: './index.html',
        },
    ],
});

// Main view
const mainView = app.views.create('.view-main');

// App State
const AppState = {
    currentConversation: null,
    conversations: [],
    messages: [],
    settings: {
        backendURL: 'http://82.223.12.60:8000',
        model: 'gpt-3.5-turbo',
        temperature: 0.7,
        streaming: true
    },
    uploadedFiles: [],
    isTyping: false
};

// Initialize Messages Component
let messagesComponent = null;
let messagebarComponent = null;

// DOM Elements
const $ = app.$;

// ==================== Initialization ====================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('SIMBA App Initialized');

    // Load settings from localStorage
    loadSettings();

    // Initialize components
    initializeComponents();

    // Setup event listeners
    setupEventListeners();

    // Check backend health
    await checkBackendHealth();

    // Load conversations
    await loadConversations();
});

// ==================== Component Initialization ====================

function initializeComponents() {
    // Initialize Messages component
    messagesComponent = app.messages.create({
        el: '#messages',
        autoLayout: true,
        newMessagesFirst: false
    });

    // Initialize Messagebar component
    messagebarComponent = app.messagebar.create({
        el: '#messagebar',
        maxHeight: 200
    });
}

// ==================== Event Listeners ====================

function setupEventListeners() {
    // New Conversation Button
    $('#new-conversation-btn').on('click', createNewConversation);
    $('#start-chat-btn').on('click', createNewConversation);

    // Settings Button
    $('#settings-btn').on('click', openSettings);

    // Send Message Button
    $('#send-message-btn').on('click', sendMessage);

    // Enter key to send message
    messagebarComponent.$textareaEl.on('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Attach File Button
    $('#attach-file-btn').on('click', () => {
        $('#file-input').click();
    });

    // File Input Change
    $('#file-input').on('change', handleFileUpload);

    // Settings
    $('#backend-url-input').on('change', (e) => {
        AppState.settings.backendURL = e.target.value;
        saveSettings();
    });

    $('#model-select').on('change', (e) => {
        AppState.settings.model = e.target.value;
        saveSettings();
    });

    $('#temperature-slider').on('input', (e) => {
        const value = parseFloat(e.target.value);
        AppState.settings.temperature = value;
        $('#temperature-value').text(value.toFixed(1));
        saveSettings();
    });

    $('#streaming-toggle').on('change', (e) => {
        AppState.settings.streaming = e.target.checked;
        saveSettings();
    });
}

// ==================== Backend Health Check ====================

async function checkBackendHealth() {
    try {
        const health = await simbaAPI.healthCheck();
        console.log('Backend health:', health);
        app.toast.create({
            text: '✅ Conectado al backend SIMBA',
            position: 'top',
            closeTimeout: 2000,
            cssClass: 'success-toast'
        }).open();
    } catch (error) {
        console.error('Backend health check failed:', error);
        app.dialog.alert(
            'No se pudo conectar con el backend de SIMBA. Verifica la configuración en Ajustes.',
            'Error de Conexión'
        );
    }
}

// ==================== Conversations Management ====================

async function loadConversations() {
    try {
        const conversations = await simbaAPI.getConversations();
        AppState.conversations = conversations;
        renderConversationsList();
    } catch (error) {
        console.error('Error loading conversations:', error);
        $('#no-conversations').show();
    }
}

function renderConversationsList() {
    const $list = $('#conversations-list');
    $list.empty();

    if (AppState.conversations.length === 0) {
        $('#no-conversations').show();
        return;
    }

    $('#no-conversations').hide();

    AppState.conversations.forEach(conv => {
        const isActive = AppState.currentConversation && AppState.currentConversation.id === conv.id;
        const $item = $(`
            <li class="${isActive ? 'active' : ''}">
                <a href="#" class="item-link item-content" data-conversation-id="${conv.id}">
                    <div class="item-media">
                        <img src="${AppConfig.assistant.avatar}" width="44" style="border-radius: 50%;">
                    </div>
                    <div class="item-inner">
                        <div class="item-title-row">
                            <div class="item-title">${conv.title || 'Nueva Conversación'}</div>
                        </div>
                        <div class="item-subtitle">${new Date(conv.created_at).toLocaleDateString()}</div>
                    </div>
                </a>
            </li>
        `);

        $item.on('click', () => {
            loadConversation(conv.id);
            app.panel.close('left');
        });

        $list.append($item);
    });
}

async function createNewConversation() {
    app.preloader.show();

    try {
        const conversation = await simbaAPI.createConversation(
            AppConfig.assistant.id,
            `Conversación ${AppState.conversations.length + 1}`
        );

        AppState.currentConversation = conversation;
        AppState.conversations.unshift(conversation);
        AppState.messages = [];

        renderConversationsList();
        showChatInterface();

        app.toast.create({
            text: '✨ Nueva conversación creada',
            position: 'top',
            closeTimeout: 2000
        }).open();
    } catch (error) {
        console.error('Error creating conversation:', error);
        app.dialog.alert('No se pudo crear la conversación. Por favor, intenta de nuevo.', 'Error');
    } finally {
        app.preloader.hide();
    }
}

async function loadConversation(conversationId) {
    app.preloader.show();

    try {
        const conversation = AppState.conversations.find(c => c.id === conversationId);
        if (!conversation) {
            throw new Error('Conversation not found');
        }

        AppState.currentConversation = conversation;

        // Load messages
        const messages = await simbaAPI.getMessages(conversationId);
        AppState.messages = messages;

        showChatInterface();
        renderMessages();

        $('#conversation-title').text(conversation.title || 'SIMBA Chat');
    } catch (error) {
        console.error('Error loading conversation:', error);
        app.dialog.alert('No se pudo cargar la conversación.', 'Error');
    } finally {
        app.preloader.hide();
    }
}

// ==================== Chat Interface ====================

function showChatInterface() {
    $('#welcome-screen').hide();
    $('#messages-container').show();
    $('#messagebar').show();
}

function hideWelcomeScreen() {
    $('#welcome-screen').hide();
}

function renderMessages() {
    // Clear existing messages
    messagesComponent.clear();

    // Add messages
    AppState.messages.forEach(msg => {
        addMessageToUI(msg);
    });

    // Scroll to bottom
    messagesComponent.scroll();
}

function addMessageToUI(message) {
    const isUser = message.role === 'user';
    const messageData = {
        text: message.content,
        type: isUser ? 'sent' : 'received',
        name: isUser ? 'Tú' : 'SIMBA',
        avatar: isUser ? null : AppConfig.assistant.avatar,
        textHeader: message.timestamp ? new Date(message.timestamp).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) : ''
    };

    messagesComponent.addMessage(messageData);
}

// ==================== Sending Messages ====================

async function sendMessage() {
    const text = messagebarComponent.getValue().trim();

    if (!text) return;

    if (!AppState.currentConversation) {
        await createNewConversation();
    }

    // Clear messagebar
    messagebarComponent.clear();

    // Add user message to UI
    const userMessage = {
        role: 'user',
        content: text,
        timestamp: new Date().toISOString()
    };

    addMessageToUI(userMessage);
    AppState.messages.push(userMessage);

    // Show typing indicator
    showTypingIndicator();

    try {
        if (AppState.settings.streaming) {
            await sendMessageWithStreaming(text);
        } else {
            await sendMessageNonStreaming(text);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        app.toast.create({
            text: '❌ Error al enviar el mensaje',
            position: 'top',
            closeTimeout: 3000
        }).open();
    }
}

async function sendMessageNonStreaming(text) {
    try {
        const response = await simbaAPI.sendMessage(
            AppState.currentConversation.id,
            text,
            {
                temperature: AppState.settings.temperature,
                maxTokens: AppConfig.llm.defaultMaxTokens
            }
        );

        hideTypingIndicator();

        const assistantMessage = response.message;
        addMessageToUI(assistantMessage);
        AppState.messages.push(assistantMessage);

        messagesComponent.scroll();
    } catch (error) {
        throw error;
    }
}

async function sendMessageWithStreaming(text) {
    let streamingMessage = null;
    let fullText = '';

    await simbaAPI.sendMessageStreaming(
        AppState.currentConversation.id,
        text,
        // onChunk
        (chunk, full) => {
            fullText = full;

            if (!streamingMessage) {
                hideTypingIndicator();
                streamingMessage = messagesComponent.addMessage({
                    text: chunk,
                    type: 'received',
                    name: 'SIMBA',
                    avatar: AppConfig.assistant.avatar,
                    textHeader: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
                });
            } else {
                // Update message text
                const $message = $(streamingMessage.el);
                $message.find('.message-text').html(fullText);
            }

            messagesComponent.scroll();
        },
        // onComplete
        (full) => {
            hideTypingIndicator();

            const assistantMessage = {
                role: 'assistant',
                content: full,
                timestamp: new Date().toISOString()
            };

            AppState.messages.push(assistantMessage);
        },
        // onError
        (error) => {
            hideTypingIndicator();
            console.error('Streaming error:', error);
        },
        {
            temperature: AppState.settings.temperature,
            maxTokens: AppConfig.llm.defaultMaxTokens
        }
    );
}

function showTypingIndicator() {
    if (AppState.isTyping) return;

    AppState.isTyping = true;
    const typingMessage = messagesComponent.addMessage({
        text: '<div class="typing-indicator"><span></span><span></span><span></span></div>',
        type: 'received',
        name: 'SIMBA',
        avatar: AppConfig.assistant.avatar
    });

    typingMessage.el.id = 'typing-indicator-message';
}

function hideTypingIndicator() {
    if (!AppState.isTyping) return;

    AppState.isTyping = false;
    const $typing = $('#typing-indicator-message');
    if ($typing.length > 0) {
        $typing.remove();
    }
}

// ==================== File Upload ====================

async function handleFileUpload(e) {
    const files = Array.from(e.target.files);

    if (files.length === 0) return;

    if (!AppState.currentConversation) {
        await createNewConversation();
    }

    for (const file of files) {
        await uploadFile(file);
    }

    // Clear file input
    e.target.value = '';
}

async function uploadFile(file) {
    // Validate file size
    if (file.size > AppConfig.fileUpload.maxSize) {
        app.toast.create({
            text: `❌ El archivo ${file.name} es demasiado grande`,
            position: 'top',
            closeTimeout: 3000
        }).open();
        return;
    }

    app.preloader.show();

    try {
        const result = await simbaAPI.uploadDocument(
            AppState.currentConversation.id,
            file,
            AppConfig.fileUpload.autoIndex
        );

        app.toast.create({
            text: `✅ Archivo subido: ${file.name}`,
            position: 'top',
            closeTimeout: 2000
        }).open();

        AppState.uploadedFiles.push(result);

        // Add system message
        const systemMessage = {
            role: 'system',
            content: `📎 Archivo cargado: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`,
            timestamp: new Date().toISOString()
        };

        addMessageToUI(systemMessage);
    } catch (error) {
        console.error('File upload error:', error);
        app.toast.create({
            text: `❌ Error al subir ${file.name}`,
            position: 'top',
            closeTimeout: 3000
        }).open();
    } finally {
        app.preloader.hide();
    }
}

// ==================== Settings ====================

function openSettings() {
    app.popup.open('#settings-popup');

    // Update UI with current settings
    $('#backend-url-input').val(AppState.settings.backendURL);
    $('#model-select').val(AppState.settings.model);
    $('#temperature-slider').val(AppState.settings.temperature);
    $('#temperature-value').text(AppState.settings.temperature.toFixed(1));
    $('#streaming-toggle').prop('checked', AppState.settings.streaming);
}

function saveSettings() {
    localStorage.setItem(AppConfig.storage.settings, JSON.stringify(AppState.settings));
}

function loadSettings() {
    const saved = localStorage.getItem(AppConfig.storage.settings);
    if (saved) {
        AppState.settings = { ...AppState.settings, ...JSON.parse(saved) };
    }
}

// ==================== Utility Functions ====================

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make app globally accessible for debugging
window.simbaApp = app;
window.AppState = AppState;

console.log('✨ SIMBA Frontend Ready!');
