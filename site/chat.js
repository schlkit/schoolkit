let socket;
let username = localStorage.getItem('username');
const modal = document.getElementById('usernameModal');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const userInfo = document.getElementById('userInfo');

// Initialize Socket.IO
function initializeSocket() {
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    socket.on('message_history', (messages) => {
        messages.reverse().forEach(addMessage);
    });
    
    socket.on('new_message', addMessage);
}

// Set username
function setUsername() {
    const newUsername = document.getElementById('usernameInput').value.trim();
    
    if (!newUsername) {
        alert('Please enter a username');
        return;
    }
    
    username = newUsername;
    localStorage.setItem('username', username);
    modal.style.display = 'none';
    userInfo.textContent = `Chatting as: ${username}`;
    initializeSocket();
    enableChat();
}

// Add a message to the chat
function addMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
    const usernameSpan = document.createElement('span');
    usernameSpan.className = 'username';
    usernameSpan.textContent = message.username === username ? 'You' : message.username;
    
    const messageContent = document.createElement('span');
    messageContent.className = 'message-content';
    messageContent.textContent = message.message;
    
    messageDiv.appendChild(usernameSpan);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Enable chat functionality
function enableChat() {
    messageInput.disabled = false;
    sendButton.disabled = false;
    
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}

// Send a message
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    socket.emit('new_message', {
        username: username,
        message: message
    });
    
    messageInput.value = '';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    messageInput.disabled = true;
    sendButton.disabled = true;
    
    if (!username) {
        modal.style.display = 'flex';
    } else {
        userInfo.textContent = `Chatting as: ${username}`;
        initializeSocket();
        enableChat();
    }
});