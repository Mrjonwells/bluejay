const backendUrl = "https://pbj-server1.onrender.com";  // Adjust if your backend URL changes

const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");

async function sendMessage(message) {
  const userMessageDiv = document.createElement("div");
  userMessageDiv.textContent = "You: " + message;
  userMessageDiv.className = "user-message";
  chatMessages.appendChild(userMessageDiv);

  chatMessages.scrollTop = chatMessages.scrollHeight;
  chatInput.value = "";

  try {
    const response = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    const botMessageDiv = document.createElement("div");
    botMessageDiv.textContent = "BlueJay: " + data.response;
    botMessageDiv.className = "bot-message";
    chatMessages.appendChild(botMessageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
  } catch (error) {
    const errorDiv = document.createElement("div");
    errorDiv.textContent = "Error contacting BlueJay. Please try again.";
    errorDiv.className = "bot-message";
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (message) {
    sendMessage(message);
  }
});