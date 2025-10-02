// Multilingual Healthcare Chatbot - Frontend JavaScript

class HealthcareChatbot {
    constructor() {
        this.currentLanguage = 'en';
        this.isTyping = false;
        this.messageHistory = [];
        this.sessionId = this.generateSessionId();
        
        this.initializeElements();
        this.attachEventListeners();
        this.loadStatistics();
        this.checkHealthStatus();
    }

    initializeElements() {
        // Main elements
        this.chatContainer = document.getElementById('chat-container');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.languageSelect = document.getElementById('language-select');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.loadingOverlay = document.getElementById('loading-overlay');
        
        // Sidebar elements
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebar-toggle');
        this.mobileMenuBtn = document.getElementById('mobile-menu-btn');
        this.refreshStatsBtn = document.getElementById('refresh-stats');
        
        // Statistics elements
        this.totalQueriesSpan = document.getElementById('total-queries');
        this.avgAccuracySpan = document.getElementById('avg-accuracy');
        
        // Quick question buttons
        this.quickQuestionBtns = document.querySelectorAll('.quick-question');
        
        // Character counter
        this.charCounter = document.querySelector('.char-counter');
    }

    attachEventListeners() {
        // Send message events
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Character counter
        this.userInput.addEventListener('input', () => this.updateCharCounter());

        // Language selection
        this.languageSelect.addEventListener('change', (e) => {
            this.currentLanguage = e.target.value;
            this.addSystemMessage(`Language changed to ${this.getLanguageName(this.currentLanguage)}`);
        });

        // Sidebar controls
        this.mobileMenuBtn.addEventListener('click', () => this.toggleSidebar());
        this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());

        // Statistics refresh
        this.refreshStatsBtn.addEventListener('click', () => this.loadStatistics());

        // Quick questions
        this.quickQuestionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.getAttribute('data-question');
                this.userInput.value = question;
                this.sendMessage();
            });
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                if (!this.sidebar.contains(e.target) && 
                    !this.mobileMenuBtn.contains(e.target) && 
                    this.sidebar.classList.contains('open')) {
                    this.toggleSidebar();
                }
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                this.sidebar.classList.remove('open');
            }
        });
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    updateCharCounter() {
        const length = this.userInput.value.length;
        this.charCounter.textContent = `${length}/500`;
        
        if (length > 450) {
            this.charCounter.style.color = '#e74c3c';
        } else if (length > 400) {
            this.charCounter.style.color = '#f39c12';
        } else {
            this.charCounter.style.color = '#999';
        }
    }

    toggleSidebar() {
        this.sidebar.classList.toggle('open');
    }

    getLanguageName(code) {
        const languages = {
            'en': 'English',
            'fr': 'Français',
            'de': 'Deutsch',
            'es': 'Español',
            'hi': 'हिन्दी'
        };
        return languages[code] || code;
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isTyping) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.updateCharCounter();

        // Show typing indicator
        this.showTyping();

        try {
            const response = await this.callChatAPI(message);
            this.hideTyping();
            
            if (response.error) {
                this.addMessage(`Error: ${response.error}`, 'bot', 0);
            } else {
                this.addMessage(response.response, 'bot', response.accuracy, response.query_id);
                this.messageHistory.push({
                    user: message,
                    bot: response.response,
                    language: this.currentLanguage,
                    accuracy: response.accuracy,
                    timestamp: new Date().toISOString()
                });
            }
        } catch (error) {
            this.hideTyping();
            console.error('Chat API Error:', error);
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot', 0);
        }

        // Auto-refresh stats every 10 messages
        if (this.messageHistory.length % 10 === 0) {
            setTimeout(() => this.loadStatistics(), 1000);
        }
    }

    async callChatAPI(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                language: this.currentLanguage,
                session_id: this.sessionId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    addMessage(content, sender, accuracy = null, queryId = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = content;

        // Add message info for bot messages
        if (sender === 'bot' && accuracy !== null) {
            const messageInfo = document.createElement('div');
            messageInfo.className = 'message-info';
            
            const timestamp = new Date().toLocaleTimeString();
            const accuracyBadge = document.createElement('span');
            accuracyBadge.className = 'accuracy-badge';
            accuracyBadge.textContent = `${Math.round(accuracy * 100)}% confidence`;
            
            messageInfo.innerHTML = `<span>${timestamp}</span>`;
            messageInfo.appendChild(accuracyBadge);
            bubble.appendChild(messageInfo);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);

        // Remove welcome message if it exists
        const welcomeMessage = this.chatContainer.querySelector('.welcome-message');
        if (welcomeMessage && sender === 'user') {
            welcomeMessage.remove();
        }

        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addSystemMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system';
        messageDiv.innerHTML = `
            <div class="system-message">
                <i class="fas fa-info-circle"></i>
                ${content}
            </div>
        `;
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTyping() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'flex';
        this.sendButton.disabled = true;
        this.userInput.disabled = true;
    }

    hideTyping() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
        this.sendButton.disabled = false;
        this.userInput.disabled = false;
        this.userInput.focus();
    }

    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    async loadStatistics() {
        try {
            const response = await fetch('/api/stats');
            if (response.ok) {
                const stats = await response.json();
                this.updateStatisticsDisplay(stats);
            }
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }

    updateStatisticsDisplay(stats) {
        if (stats.error) {
            console.error('Statistics error:', stats.error);
            return;
        }

        this.totalQueriesSpan.textContent = stats.total_queries || 0;
        this.avgAccuracySpan.textContent = `${Math.round((stats.average_accuracy || 0) * 100)}%`;

        // Add animation to updated stats
        [this.totalQueriesSpan, this.avgAccuracySpan].forEach(element => {
            element.style.transform = 'scale(1.1)';
            element.style.color = '#74b9ff';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
                element.style.color = '#2c3e50';
            }, 300);
        });
    }

    async checkHealthStatus() {
        try {
            this.loadingOverlay.style.display = 'flex';
            
            const response = await fetch('/api/health');
            const health = await response.json();
            
            setTimeout(() => {
                this.loadingOverlay.style.display = 'none';
                
                if (health.status === 'healthy') {
                    console.log('Healthcare Chatbot is ready!');
                    this.addSystemMessage('Healthcare Assistant is ready to help you!');
                } else {
                    this.addSystemMessage('Some services may be unavailable. Please try again later.');
                }
            }, 2000); // Show loading for at least 2 seconds
            
        } catch (error) {
            console.error('Health check failed:', error);
            setTimeout(() => {
                this.loadingOverlay.style.display = 'none';
                this.addSystemMessage('Connection error. Some features may not work properly.');
            }, 2000);
        }
    }

    // Utility methods
    formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleString();
    }

    exportChatHistory() {
        const dataStr = JSON.stringify(this.messageHistory, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `chat_history_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.chatContainer.innerHTML = '';
            this.messageHistory = [];
            
            // Re-add welcome message
            this.chatContainer.innerHTML = `
                <div class="welcome-message">
                    <div class="bot-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <h3>Welcome back to Healthcare Assistant!</h3>
                        <p>How can I help you today?</p>
                    </div>
                </div>
            `;
        }
    }

    // Voice input (if supported)
    startVoiceInput() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            
            recognition.lang = this.currentLanguage === 'hi' ? 'hi-IN' : 
                             this.currentLanguage === 'fr' ? 'fr-FR' :
                             this.currentLanguage === 'de' ? 'de-DE' :
                             this.currentLanguage === 'es' ? 'es-ES' : 'en-US';
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.userInput.value = transcript;
                this.updateCharCounter();
            };
            
            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.addSystemMessage('Voice input error. Please try typing instead.');
            };
            
            recognition.start();
            this.addSystemMessage('Listening... Please speak now.');
        } else {
            this.addSystemMessage('Voice input is not supported in your browser.');
        }
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new HealthcareChatbot();
});

// Add some global utility functions
window.exportChat = () => window.chatbot.exportChatHistory();
window.clearChat = () => window.chatbot.clearChat();
window.startVoice = () => window.chatbot.startVoiceInput();

// Service Worker registration for offline functionality (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
