document.addEventListener("DOMContentLoaded", function () {
    const sendBtn = document.getElementById("send-btn");
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    async function sendMessage() {
        const message = inputField.value.trim();
        if (!message) return;

        // Display user message
        const userMsg = document.createElement("div");
        userMsg.className = "chat user";
        userMsg.textContent = message;
        chatBox.appendChild(userMsg);

        inputField.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch("https://pbj-server1.onrender.com/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            const reply = data.reply || "There was an error processing your message.";

            const botMsg = document.createElement("div");
            botMsg.className = "chat bot";
            botMsg.textContent = reply;
            chatBox.appendChild(botMsg);
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (err) {
            const errorMsg = document.createElement("div");
            errorMsg.className = "chat bot";
            errorMsg.textContent = "There was an error processing your message.";
            chatBox.appendChild(errorMsg);
        }
    }

    sendBtn?.addEventListener("click", sendMessage);
    inputField?.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});