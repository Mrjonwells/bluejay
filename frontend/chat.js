document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const backendUrl = 'https://pbj-server1.onrender.com/chat';

    // Get or create user ID
    let userId = localStorage.getItem('user_id');
    if (!userId) {
        userId = crypto.randomUUID();
        localStorage.setItem('user_id', userId);
    }

    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const userInput = chatInput.value.trim();
        if (!userInput) return;

        // Add user message
        const userBubble = document.createElement('div');
        userBubble.className = 'chat-bubble user';
        userBubble.innerText = userInput;
        chatMessages.appendChild(userBubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        chatInput.value = '';

        try {
            const response = await fetch(backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-User-Id': userId
                },
                body: JSON.stringify({ user_input: userInput })
            });

            const data = await response.json();

            if (response.ok) {
                const assistantBubble = document.createElement('div');
                assistantBubble.className = 'chat-bubble assistant';
                assistantBubble.innerText = data.assistant;
                chatMessages.appendChild(assistantBubble);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } else {
                const errorBubble = document.createElement('div');
                errorBubble.className = 'chat-bubble error';
                errorBubble.innerText = 'Error: ' + (data.error || 'Something went wrong.');
                chatMessages.appendChild(errorBubble);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        } catch (error) {
            const errorBubble = document.createElement('div');
            errorBubble.className = 'chat-bubble error';
            errorBubble.innerText = 'Error: ' + error.message;
            chatMessages.appendChild(errorBubble);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    });
});