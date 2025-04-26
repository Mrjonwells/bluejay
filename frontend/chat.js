const backendUrl = "https://bluejay-1.onrender.com"; // Updated to new server

document.addEventListener("DOMContentLoaded", function() {
    const chatContainer = document.getElementById("chat");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    function appendMessage(text, className) {
        const messageDiv = document.createElement("div");
        messageDiv.className = className;
        messageDiv.textContent = text;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    sendButton.addEventListener("click", async function() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage(message, "user-message");
        userInput.value = "";

        try {
            const response = await fetch(`${backendUrl}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });

            if (response.ok) {
                const data = await response.json();
                appendMessage(data.response, "bot-message");
            } else {
                appendMessage("Error: Failed to get a response.", "bot-message");
            }
        } catch (error) {
            appendMessage("Error: Server unreachable.", "bot-message");
        }
    });

    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });
});