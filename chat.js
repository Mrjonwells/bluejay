document.getElementById("input").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

document.getElementById("send-button").addEventListener("click", function () {
  sendMessage();
});

async function sendMessage() {
  const inputField = document.getElementById("input");
  const message = inputField.value.trim();
  if (!message) return;

  const chatBox = document.getElementById("chat-box");

  // Add user message to chat
  const userMessage = document.createElement("div");
  userMessage.className = "message user-message";
  userMessage.innerText = message;
  chatBox.appendChild(userMessage);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Clear input
  inputField.value = "";

  // Send message to backend
  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    // Add assistant reply to chat
    const botMessage = document.createElement("div");
    botMessage.className = "message bot-message";
    botMessage.innerText = data.reply;
    chatBox.appendChild(botMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    // HubSpot trigger logic
    const lowerMsg = message.toLowerCase();
    const triggerPhrases = ["done", "submit", "that's all", "send it", "ready to submit"];
    if (triggerPhrases.includes(lowerMsg)) {
      await fetch("/submit-to-hubspot", {
        method: "POST",
      });
      const confirmation = document.createElement("div");
      confirmation.className = "message bot-message";
      confirmation.innerText = "Thanks! I've submitted your info.";
      chatBox.appendChild(confirmation);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

  } catch (error) {
    console.error("Error sending message:", error);
    const errorMsg = document.createElement("div");
    errorMsg.className = "message bot-message";
    errorMsg.innerText = "Oops! Something went wrong.";
    chatBox.appendChild(errorMsg);
  }
}
