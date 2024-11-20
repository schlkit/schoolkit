document.addEventListener('DOMContentLoaded', function() {
    const chatPreview = document.getElementById('chatPreview');
    const socket = io();

    // Request recent messages when page loads
    socket.emit('get_recent_messages');

    // Handle incoming recent messages
    socket.on('recent messages', function(messages) {
        if (!messages || messages.length === 0) {
            chatPreview.innerHTML = `
                <div class="preview-message">
                    <span class="message">No messages yet. Be the first to chat!</span>
                </div>`;
            return;
        }

        chatPreview.innerHTML = messages.map(msg => `
            <div class="preview-message">
                <div class="message-header">
                    <span class="username">${msg.username}</span>
                    <span class="timestamp">${msg.timestamp}</span>
                </div>
                <div class="message">${msg.message}</div>
            </div>
        `).join('');
    });

    // PWA Installation
    const pwaModal = document.getElementById('pwaModal');
    const installButton = document.getElementById('installPWA');

    function showPwaModal() {
        pwaModal.classList.remove('hidden');
        setTimeout(() => pwaModal.classList.add('show'), 10);
    }

    function closePwaModal() {
        pwaModal.classList.remove('show');
        setTimeout(() => pwaModal.classList.add('hidden'), 300);
    }

    installButton.addEventListener('click', showPwaModal);

    // Close modal when clicking outside
    pwaModal.addEventListener('click', (e) => {
        if (e.target === pwaModal) {
            closePwaModal();
        }
    });

    // Handle actual PWA install prompt if available
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        installButton.style.display = 'flex';
    });

    // If PWA is already installed, hide the install button
    window.addEventListener('appinstalled', () => {
        installButton.style.display = 'none';
    });
}); 